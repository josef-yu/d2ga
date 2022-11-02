from rest_framework import mixins, permissions, generics, status, viewsets, filters, exceptions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count, F, Case, Value, When, Avg
from django.db import transaction, models
from d2ga.pagination import DefaultResultPagination
from .models import GenerationData, MatchmakingPool, Player, Match, MatchStats, MatchmakingMatch
from .choices import (
    CHOICE_MEDAL,
    HERALD_MAX,
    GUARDIAN_MAX,
    CRUSADER_MAX,
    ARCHON_MAX,
    LEGEND_MAX,
    ANCIENT_MAX,
    DIVINE_MAX,
    CHOICE_SIDE
)
from .serializers import (
    MatchStatsAverageSerializer,
    MatchmakingPoolSerializer,
    MatchmakingSerializer,
    PlayerSerializer,
    PlayerMatchesSerializer, 
    PlayerPostSerializer,
    PlayerRoleCountSerializer, 
    PlayerMedalCountSerializer,
    SyncSheetsDataSerializer
)
from d2ga.helpers import get_gcloud_creds, Opendota
from .helpers import GA

from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from datetime import datetime
import re

import math
import random
import time
import copy
from .task import findmatch_task, parent_match_stats_task, send_notification_task

from rest_framework.schemas.inspectors import AutoSchema
import coreapi

SURVEY_SPREADSHEET_ID = '19LzNbpWq1tt9PLERt8U7t3NiGO8vK4-HQCsf3ZCZX54'

class PlayerViewSet(viewsets.ModelViewSet):
    """
    list: Use this endpoint to retrieve list of players.

    create: Use this endpoint to create a new player.

    retrieve: Use this endpoint to retrieve list of player with specified ID.

    update: Use this endpoint to update player information.

    partial_update: Use this endpoint to partially update a player.

    destroy: Use this endpoint to delete a player.
    """

    permission_classes = (
        permissions.IsAuthenticated, permissions.IsAdminUser
    )
    filter_backends = [filters.OrderingFilter]
    ordering_fields = '__all__'
    ordering = ['created']

    def get_queryset(self):
        return Player.objects.all()\
            .annotate(
                medal=Case(
                    When(mmr__lte=HERALD_MAX, then=Value(1)),
                    When(mmr__lte=GUARDIAN_MAX, then=Value(2)),
                    When(mmr__lte=CRUSADER_MAX, then=Value(3)),
                    When(mmr__lte=ARCHON_MAX, then=Value(4)),
                    When(mmr__lte=LEGEND_MAX, then=Value(5)),
                    When(mmr__lte=ANCIENT_MAX, then=Value(6)),
                    When(mmr__lte=DIVINE_MAX, then=Value(7)),
                    When(mmr__gt=DIVINE_MAX, then=Value(8)),
                    default=Value(0),
                    output_field=models.PositiveIntegerField()
                )
            )

    def get_serializer_class(self, *args, **kwargs):
        """
        Swagger passes request=None. Return create serializer because
        GET requests don't have request body fields.
        See get_serializer_fields()
        """
        if self.request is None:
            return PlayerPostSerializer
        
        if self.request.method == 'POST':
            return PlayerPostSerializer

        return PlayerSerializer
    

class BaseCountView(generics.GenericAPIView):
    permission_classes = (
        permissions.IsAuthenticated, permissions.IsAdminUser
    )
    
    def get(self, request):
        queryset = self.get_queryset()
        data = {'breakdown': list(queryset), 'total': sum([x['count'] for x in list(queryset)])}
        serializer = self.get_serializer(instance=data)
        return Response(serializer.data)

class MatchRoleCountView(BaseCountView):
    """
    Use this endpoint to get breakdown of matches by role
    """
    serializer_class = PlayerRoleCountSerializer

    def get_queryset(self):
        return Match.objects\
            .filter(fetch_status=Match.FETCH_STATUS.success)\
            .values(role=F('player__role'))\
            .annotate(count=Count('role'))\
            .order_by('role')

class MatchMedalCountView(BaseCountView):
    """
    Use this endpoint to get breakdown of matches by medal
    """
    serializer_class = PlayerMedalCountSerializer

    def get_queryset(self):
        return Match.objects\
            .filter(fetch_status=Match.FETCH_STATUS.success)\
            .annotate(
                medal=Case(
                    When(player__mmr__lte=HERALD_MAX, then=Value(1)),
                    When(player__mmr__lte=GUARDIAN_MAX, then=Value(2)),
                    When(player__mmr__lte=CRUSADER_MAX, then=Value(3)),
                    When(player__mmr__lte=ARCHON_MAX, then=Value(4)),
                    When(player__mmr__lte=LEGEND_MAX, then=Value(5)),
                    When(player__mmr__lte=ANCIENT_MAX, then=Value(6)),
                    When(player__mmr__lte=DIVINE_MAX, then=Value(7)),
                    When(player__mmr__gt=DIVINE_MAX, then=Value(8)),
                    default=Value(0),
                    output_field=models.PositiveIntegerField()
                ),
            ).values('medal')\
            .annotate(count=Count('medal'))\
            .order_by('medal')

class PlayerRoleCountView(BaseCountView):
    """
    Use this endpoint to get breakdown of players by role
    """
    serializer_class = PlayerRoleCountSerializer

    def get_queryset(self):
        return Player.objects.filter(is_active=Player.ACTIVE.active)\
            .values('role')\
            .annotate(count=Count('role'))\
            .order_by('role')

class PlayerMedalCountView(BaseCountView):
    """
    Use this endpoint to get breakdown of players by medal
    """
    serializer_class = PlayerMedalCountSerializer

    def get_queryset(self):
        return Player.objects.filter(is_active=Player.ACTIVE.active)\
            .annotate(
                medal=Case(
                    When(mmr__lte=HERALD_MAX, then=Value(1)),
                    When(mmr__lte=GUARDIAN_MAX, then=Value(2)),
                    When(mmr__lte=CRUSADER_MAX, then=Value(3)),
                    When(mmr__lte=ARCHON_MAX, then=Value(4)),
                    When(mmr__lte=LEGEND_MAX, then=Value(5)),
                    When(mmr__lte=ANCIENT_MAX, then=Value(6)),
                    When(mmr__lte=DIVINE_MAX, then=Value(7)),
                    When(mmr__gt=DIVINE_MAX, then=Value(8)),
                    default=Value(0),
                    output_field=models.PositiveIntegerField()
                ),
            ).values('medal').annotate(count=Count('medal')).order_by('medal')

class SyncSheetsDataView(generics.GenericAPIView):
    """
    Use this endpoint to sync survey data from google sheets
    """
    permission_classes = (
        permissions.IsAuthenticated, permissions.IsAdminUser
    )
    serializer_class = SyncSheetsDataSerializer

    def post(self, request):
        creds = get_gcloud_creds()
        values = []
        try:
            service = build('sheets', 'v4', credentials=creds)

            sheet = service.spreadsheets()
            result = sheet.values()\
                .get(spreadsheetId=SURVEY_SPREADSHEET_ID, range='Form Responses 1!A2:E')\
                .execute()
            
            values = result.get('values', [])
        except HttpError as err:
            print(err)
        
        with transaction.atomic():
            for row in values:

                Player.objects.get_or_create(
                    defaults={
                        'created':datetime.strptime(row[0], '%m/%d/%Y %H:%M:%S').isoformat(),
                        'mmr':int(row[2].replace(',', '')),
                        'behavior_score':int(row[3].replace(',', ''))
                    },
                    dotaID=row[1],
                    role=int(re.match('Position (.+?)\(', row[4]).group(1))
                )
        return Response(status=status.HTTP_201_CREATED)

class FetchPlayerMatchView(generics.GenericAPIView):
    """
    post: Use this endpoint to fetch last 100 matches of player specified by dotaID

    get: Use this endpoint to get last 100 matches of player specified by dotaID
    """
    permission_classes = (
        permissions.IsAuthenticated, permissions.IsAdminUser
    )
    pagination_class = DefaultResultPagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = '__all__'
    ordering = ['id']

    def get_serializer_class(self, *args, **kwargs):
        """
        Swagger passes request=None. Return create serializer because
        GET requests don't have request body fields.
        See get_serializer_fields()
        """
        if self.request is None:
            return SyncSheetsDataSerializer
        
        if self.request.method == 'POST':
            return SyncSheetsDataSerializer

        return PlayerMatchesSerializer
    
    def get_queryset(self):
        return Match.objects.filter(
            player__id=int(self.kwargs['player_id'])
        )

    @transaction.atomic
    def post(self, request, player_id):
        player = Player.objects.select_for_update().get(id=player_id)
        
        dota_api = Opendota()
        match_history = dota_api.get_player_matches(
            player_id=player.dotaID, 
            lobby_type=Opendota.LOBBY_TYPE.ranked
        )

        if len(match_history) < 1:
            reason = 'Player has no matches or is private'
            send_notification_task.delay({
                'dotaID': player.dotaID,
                'reason': reason
            }, False)
            return Response(
                data={'detail': reason}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        

        count = 0
        matches_to_add = []


        for match in match_history:
            if match['lobby_type'] == 7 and count < 100 and match['leaver_status'] < 1:
                m, created = Match.objects.get_or_create(
                    defaults={'lobby_type': match['lobby_type']},
                    player=player,
                    identifier=match['match_id']
                )
                if created == True:
                    matches_to_add.append(m)
                count += 1
            elif count >= 100:
                break
        
        parent_match_stats_task.delay([m.id for m in matches_to_add], player.dotaID)

        return Response(status=status.HTTP_201_CREATED)
    
    def get(self, request, player_id):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(instance=queryset, many=True)
        return self.get_paginated_response(
            self.paginate_queryset(serializer.data)
        )

class MatchStatsAverageView(generics.GenericAPIView):
    """
    get: Use this endpoint to get average match stats per role
    """
    permission_classes = (
        permissions.IsAuthenticated, permissions.IsAdminUser
    )
    queryset = MatchStats.objects.all()
    serializer_class = MatchStatsAverageSerializer

    def filter_average(self, role):
        if role == 'all':
            return self.get_queryset()\
                .aggregate(
                    assists=Avg('assists'),
                    deaths=Avg('deaths'),
                    kills=Avg('kills'),
                    denies=Avg('denies'),
                    last_hits=Avg('last_hits'),
                    gold_per_min=Avg('gold_per_min'),
                    xp_per_min=Avg('xp_per_min'),
                    net_worth=Avg('net_worth'),
                    hero_damage=Avg('hero_damage'),
                    tower_damage=Avg('tower_damage'),
                    hero_healing=Avg('hero_healing')
                )
        else:
            return self.get_queryset()\
                .filter(match__player__role=role)\
                .aggregate(
                    assists=Avg('assists'),
                    deaths=Avg('deaths'),
                    kills=Avg('kills'),
                    denies=Avg('denies'),
                    last_hits=Avg('last_hits'),
                    gold_per_min=Avg('gold_per_min'),
                    xp_per_min=Avg('xp_per_min'),
                    net_worth=Avg('net_worth'),
                    hero_damage=Avg('hero_damage'),
                    tower_damage=Avg('tower_damage'),
                    hero_healing=Avg('hero_healing')
                )

    def get(self, request, role):
        queryset = self.filter_average(role)
        data = {'breakdown': [{'name': k, 'count': v} for k,v in queryset.items()]}
        serializer = self.get_serializer(instance=data)
        return Response(serializer.data)

class FindMatchView(generics.GenericAPIView):
    """
    post: Use this endpoint to start matchmaking on current players in database
    """
    permission_classes = (
        permissions.IsAuthenticated, permissions.IsAdminUser
    )

    schema = AutoSchema(
        manual_fields=[
            coreapi.Field(
                "id",
                required=False,
                location='query'
            )
        ]
    )

    def get_serializer_class(self, *args, **kwargs):
        """
        Swagger passes request=None. Return create serializer because
        GET requests don't have request body fields.
        See get_serializer_fields()
        """
        if self.request is None:
            return MatchmakingSerializer
        
        if self.request.method == 'POST':
            return MatchmakingSerializer

        return MatchmakingSerializer

    def get_queryset(self, matchmaking_id):
        return GenerationData.objects\
            .select_related('player', 'matchmaking_generation')\
            .filter(
                matchmaking_generation__matchmaking_match_id = matchmaking_id
            ).order_by(
                '-matchmaking_generation__created',
                'matchmaking_generation__imbalance',
                '-matchmaking_generation__id',
                'side',
                'player__role'
            ).annotate(
                elapsed_time=F('matchmaking_generation__matchmaking_match__modified') - \
                    F('matchmaking_generation__matchmaking_match__created'),
                imbalance=F('matchmaking_generation__imbalance'),
                f_mmr=F('matchmaking_generation__f_mmr'),
                f_behavior_score=F('matchmaking_generation__f_behavior_score'),
                f_fantasy=F('matchmaking_generation__f_fantasy'),
                generation=F('matchmaking_generation__generation'),
                dotaID=F('player__dotaID'),
                mmr=F('player__mmr'),
                role=F('player__role'),
                behavior_score=F('player__behavior_score'),
                medal=Case(
                    When(mmr__lte=HERALD_MAX, then=Value(1)),
                    When(mmr__lte=GUARDIAN_MAX, then=Value(2)),
                    When(mmr__lte=CRUSADER_MAX, then=Value(3)),
                    When(mmr__lte=ARCHON_MAX, then=Value(4)),
                    When(mmr__lte=LEGEND_MAX, then=Value(5)),
                    When(mmr__lte=ANCIENT_MAX, then=Value(6)),
                    When(mmr__lte=DIVINE_MAX, then=Value(7)),
                    When(mmr__gt=DIVINE_MAX, then=Value(8)),
                    default=Value(0),
                    output_field=models.PositiveIntegerField()
                )
            )
            

    def post(self, request):
        
        matchmaking = MatchmakingMatch.objects.create()

        findmatch_task.delay(matchmaking.id)

        return Response({
            'matchmaking_id': matchmaking.id
        })
    
    def get(self, request):
        if request.query_params.get('id', None) is None:
            return Response({'detail': 'Invalid matchmaking id'}, status=status.HTTP_400_BAD_REQUEST)
        matchmaking_id = request.query_params.get('id')

        try:
            matchmaking = MatchmakingMatch.objects.get(id=matchmaking_id)
        except MatchmakingMatch.DoesNotExist:
            return Response({'detail': 'Invalid matchmaking id'}, status=status.HTTP_400_BAD_REQUEST)

        queryset = self.get_queryset(matchmaking_id)
        serializer = self.get_serializer(list(queryset)[:10], many=True)


        return Response({
            'status': MatchmakingMatch.STATUS[matchmaking.status],
            'remarks': matchmaking.remarks,
            'optimal': serializer.data
            })

class MatchmakingPoolView(generics.GenericAPIView):
    """
    get: Use this endpoint to get player pool for matchmaking by id
    """
    permission_classes = (
        permissions.IsAuthenticated, permissions.IsAdminUser
    )
    serializer_class = MatchmakingPoolSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = '__all__'
    ordering = ['role']

    def get_queryset(self, id):
        return MatchmakingPool.objects.filter(matchmaking_match_id=id)\
            .annotate(
                dotaID=F('player__dotaID'),
                mmr=F('player__mmr'),
                role=F('player__role'),
                behavior_score=F('player__behavior_score'),
                medal=Case(
                    When(mmr__lte=HERALD_MAX, then=Value(1)),
                    When(mmr__lte=GUARDIAN_MAX, then=Value(2)),
                    When(mmr__lte=CRUSADER_MAX, then=Value(3)),
                    When(mmr__lte=ARCHON_MAX, then=Value(4)),
                    When(mmr__lte=LEGEND_MAX, then=Value(5)),
                    When(mmr__lte=ANCIENT_MAX, then=Value(6)),
                    When(mmr__lte=DIVINE_MAX, then=Value(7)),
                    When(mmr__gt=DIVINE_MAX, then=Value(8)),
                    default=Value(0),
                    output_field=models.PositiveIntegerField()
                )
            )

    def get(self, request, matchmaking_id):
        queryset = self.filter_queryset(self.get_queryset(matchmaking_id))
        serializer = self.get_serializer(queryset, many=True)

        return self.get_paginated_response(
            self.paginate_queryset(serializer.data)
        )
    