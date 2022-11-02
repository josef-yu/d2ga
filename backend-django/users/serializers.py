from rest_framework import serializers
from django.db.models import Count
from .models import MatchStats, Player, Match
from .helpers import calc_matchstats
from .choices import (
    ANCIENT_MAX,
    ARCHON_MAX,
    CHOICE_POSITION, 
    CHOICE_MEDAL, 
    CHOICE_LOBBY_TYPE, 
    CHOICE_STATUS, 
    CHOICE_SIDE,
    CRUSADER_MAX,
    DIVINE_MAX,
    GUARDIAN_MAX,
    HERALD_MAX,
    LEGEND_MAX
)
class PlayerSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    medal = serializers.SerializerMethodField()
    num_matches = serializers.SerializerMethodField()
    class Meta:
        model = Player
        fields = '__all__'
    
    def get_num_matches(self, obj):
        result = Match.objects\
            .filter(player_id=obj.id, fetch_status=Match.FETCH_STATUS.success)\
            .aggregate(count=Count('id'))
        return result['count']

    def get_role(self, obj):
        return CHOICE_POSITION[int(obj.role)]
    
    def get_medal(self, obj):
        m = CHOICE_MEDAL[int(obj.medal)]
        r = None
        h = None
        if obj.medal == 1:
            h = 0
            d = HERALD_MAX / 5            
        elif obj.medal == 2:
            h = HERALD_MAX
            d = (GUARDIAN_MAX - HERALD_MAX) / 5
        elif obj.medal == 3:
            h = GUARDIAN_MAX
            d = (CRUSADER_MAX - GUARDIAN_MAX) / 5
        elif obj.medal == 4:
            h = CRUSADER_MAX
            d = (ARCHON_MAX - CRUSADER_MAX) / 5
        elif obj.medal == 5:
            h = ARCHON_MAX
            d = (LEGEND_MAX - ARCHON_MAX) / 5
        elif obj.medal == 6:
            h = LEGEND_MAX
            d = (ANCIENT_MAX - LEGEND_MAX) / 5
        elif obj.medal == 7:
            h = ANCIENT_MAX
            d = (DIVINE_MAX - ANCIENT_MAX) / 5

        if not h is None:
            r = (obj.mmr - h) / d
            if int(r) == 0:
                r = 1
        return str(m) + ' ' + (str(int(r)) if not r is None else '')

class PlayerPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'

class BaseCountBreakdownSerializer(serializers.Serializer):
    name = serializers.SerializerMethodField()
    count = serializers.IntegerField()

class BaseCountSerializer(serializers.Serializer):
    total = serializers.IntegerField()

class RoleCountBreakdownSerializer(BaseCountBreakdownSerializer):
    def get_name(self, obj):
        return CHOICE_POSITION[int(obj['role'])]

class MedalCountBreakdownSerializer(BaseCountBreakdownSerializer):
    def get_name(self, obj):
        return CHOICE_MEDAL[int(obj['medal'])]
    
class MatchStatsAverageBreakdownSerializer(BaseCountBreakdownSerializer):
    def get_name(self, obj):
        return obj['name']

class PlayerRoleCountSerializer(BaseCountSerializer):
    breakdown = RoleCountBreakdownSerializer(many=True)

class PlayerMedalCountSerializer(BaseCountSerializer):
    breakdown = MedalCountBreakdownSerializer(many=True)

class MatchRoleCountSerializer(PlayerRoleCountSerializer):
    pass

class MatchMedalCountSerializer(PlayerMedalCountSerializer):
    pass

class MatchStatsAverageSerializer(serializers.Serializer):
    breakdown = MatchStatsAverageBreakdownSerializer(many=True)

class SyncSheetsDataSerializer(serializers.Serializer):
    pass

class PlayerMatchesSerializer(serializers.ModelSerializer):
    date_fetched = serializers.SerializerMethodField()
    lobby_type = serializers.SerializerMethodField()
    fetch_status = serializers.SerializerMethodField()
    class Meta:
        model = Match
        fields = '__all__'

    def get_date_fetched(self, obj):
        if obj.created != obj.modified:
            return obj.modified
        
        return None
    
    def get_lobby_type(self, obj):
        return CHOICE_LOBBY_TYPE[int(obj.lobby_type)]

    def get_fetch_status(self, obj):
        return CHOICE_STATUS[obj.fetch_status]

class MatchmakingSerializer(serializers.Serializer):
    elapsed_time = serializers.CharField()
    imbalance = serializers.IntegerField()
    f_mmr = serializers.IntegerField()
    f_behavior_score = serializers.IntegerField()
    f_fantasy = serializers.IntegerField()
    generation = serializers.IntegerField()
    dotaID = serializers.CharField()
    role = serializers.SerializerMethodField()
    mmr = serializers.IntegerField()
    behavior_score = serializers.IntegerField()
    individual_fantasy = serializers.FloatField()
    side = serializers.SerializerMethodField()
    medal = serializers.SerializerMethodField()

    def get_role(self, obj):
        return CHOICE_POSITION[int(obj.role)]

    def get_side(self, obj):
        return CHOICE_SIDE[int(obj.side)]
    
    def get_medal(self, obj):
        m = CHOICE_MEDAL[int(obj.medal)]
        r = None
        h = None
        if obj.medal == 1:
            h = 0
            d = HERALD_MAX / 5            
        elif obj.medal == 2:
            h = HERALD_MAX
            d = (GUARDIAN_MAX - HERALD_MAX) / 5
        elif obj.medal == 3:
            h = GUARDIAN_MAX
            d = (CRUSADER_MAX - GUARDIAN_MAX) / 5
        elif obj.medal == 4:
            h = CRUSADER_MAX
            d = (ARCHON_MAX - CRUSADER_MAX) / 5
        elif obj.medal == 5:
            h = ARCHON_MAX
            d = (LEGEND_MAX - ARCHON_MAX) / 5
        elif obj.medal == 6:
            h = LEGEND_MAX
            d = (ANCIENT_MAX - LEGEND_MAX) / 5
        elif obj.medal == 7:
            h = ANCIENT_MAX
            d = (DIVINE_MAX - ANCIENT_MAX) / 5

        if not h is None:
            r = (obj.mmr - h) / d
            if int(r) == 0:
                r = 1
        return str(m) + ' ' + (str(int(r)) if not r is None else '')

class MatchmakingPoolSerializer(PlayerSerializer):
    fantasy = serializers.SerializerMethodField()
    class Meta:
        model = Player
        exclude = ('id', 'created', 'is_active')
    
    def get_fantasy(self, obj):
        matches = Match.objects\
                    .filter(player__dotaID=obj.dotaID, fetch_status=Match.FETCH_STATUS.success)
        matches_stats = MatchStats.objects.filter(match__in=matches)
        fantasy = calc_matchstats(matches_stats, obj.role)
        return fantasy['score']
        
    
    def get_num_matches(self, obj):
        result = Match.objects\
            .filter(player__dotaID=obj.dotaID, fetch_status=Match.FETCH_STATUS.success)\
            .aggregate(count=Count('id'))
        return result['count']
    
    
    