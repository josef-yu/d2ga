from .models import (
    GenerationData, 
    Match, 
    MatchStats, 
    MatchmakingGeneration, 
    Player, 
    MatchmakingMatch,
    MatchmakingPool
)
from d2ga.celery import app
from django.conf import settings
from django.db import transaction, models
from django.db.models import When, Case, Value

from .choices import (
    HERALD_MAX,
    GUARDIAN_MAX,
    CRUSADER_MAX,
    ARCHON_MAX,
    LEGEND_MAX,
    ANCIENT_MAX,
    DIVINE_MAX,
    CHOICE_MEDAL
)

import d2api
import random
import time
import requests
import json
from celery import group
from requests.exceptions import ConnectionError
from d2ga.helpers import Opendota

def fetch_match_stats(match_id, dotaID):
    dota_api = Opendota()
    stats = dota_api.get_match_details(match_id)
    
    for player in stats['players']:
        if str(player['account_id']) == str(dotaID):
            return player

    raise ValueError('Player not found')

def send_notification(payload, is_success):
    template = 'ZFLkCZBj6Z' if is_success else 'HMRyF7qzsA'
    try:
        r = requests.post(
            f'https://api.ravenhub.io/company/dijF5JL6fH/subscribers/d2gaapp/events/{template}',
            json=payload
        )
        r.raise_for_status()
    except Exception as error:
        print(r.text)
        print(error)
        raise error

@app.task(bind=True)
def send_notification_task(self, payload, is_success):
    try:
        send_notification(payload, is_success)
    except Exception as error:
        self.retry(exc=error, countdown=int(random.uniform(2,4) ** self.request.retries))

@app.task(bind=True)
def match_stats_task(self, match_id):
    from .helpers import filter_data
    print(match_id)
    match = Match.objects.get(id=match_id, fetch_status=Match.FETCH_STATUS.pending)
    player_stats = None

    try:
        player_stats = fetch_match_stats(match.identifier, match.player.dotaID)
        match.fetch_status = Match.FETCH_STATUS.success
    except ConnectionError as error:
        self.retry(exc=error, countdown=int(random.uniform(2,4) ** self.request.retries))
    except ValueError as error:
        match.fetch_status = Match.FETCH_STATUS.failed
        match.remarks = error

    try:
        with transaction.atomic():
            if player_stats is not None:
                kwars = filter_data(MatchStats, player_stats)
                kwars['side'] = getattr(MatchStats.SIDE, 'radiant' if player_stats['isRadiant'] else 'dire')
                MatchStats.objects.create(
                    match=match,
                    **kwars
                )
            match.save()
    except Exception:
        match.delete()

@app.task(bind=True)
def parent_match_stats_task(self, match_ids, dotaID):
    job = group(match_stats_task.s(id) for id in match_ids)

    result = job.apply_async()

    while True:
        time.sleep(0.1)

        if result.ready():
            break
    
    player = Player.objects.get(dotaID=dotaID)
    
    send_notification_task.delay({
        'dotaID': str(dotaID),
        'url': f'{settings.SITE_HOST}players/{player.id}'
    }, True)

@app.task(bind=True)
def save_generation_data(self, candidates, generation, matchmaking_id):
    for index, teams in enumerate(candidates):
        gen = MatchmakingGeneration.objects.create(
                generation=generation,
                imbalance=teams['imbalance'],
                matchmaking_match_id=matchmaking_id,
                f_mmr=teams['f_mmr'],
                f_behavior_score=teams['f_behavior'],
                f_fantasy=teams['f_fantasy']
            )

        for player in teams['radiant']:
            GenerationData.objects.create(
                side=GenerationData.SIDE.radiant,
                player=player['player'],
                matchmaking_generation=gen,
                individual_fantasy=player['fantasy']['score']
            )
        
        for player in teams['dire']:
            GenerationData.objects.create(
                side=GenerationData.SIDE.dire,
                player=player['player'],
                matchmaking_generation=gen,
                individual_fantasy=player['fantasy']['score']
            )

@app.task(bind=True)
def save_pool(self, pool, matchmaking_id):
    players = Player.objects.filter(dotaID__in=pool)
    MatchmakingPool.objects.bulk_create([
        MatchmakingPool(
            matchmaking_match_id=matchmaking_id, 
            player=p
        ) for p in players
    ])
    

@app.task(bind=True)
def findmatch_task(self, matchmaking_id):
    from .helpers import GA
    queryset = Player.objects\
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
            )
    choice = random.choice([
        None, HERALD_MAX, GUARDIAN_MAX, 
        CRUSADER_MAX, ARCHON_MAX, LEGEND_MAX
        ])

    if not choice is None:
        queryset = queryset.filter(mmr__gte=choice)
        
    matchmaking = MatchmakingMatch.objects.get(id=matchmaking_id)
    ga = GA(queryset, matchmaking.id)

    remarks = None
    
    found = ga.execute()

    with transaction.atomic():
        matchmaking.status = MatchmakingMatch.STATUS.found if found else MatchmakingMatch.STATUS.failed
        if remarks:
            matchmaking.remarks = remarks
        matchmaking.save()
