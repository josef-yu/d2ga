from django.db import models
from .choices import (
    CHOICE_POSITION, 
    CHOICE_SIDE, 
    CHOICE_LOBBY_TYPE, 
    CHOICE_STATUS, 
    CHOICE_ACTIVE,
    CHOICE_MATCHMAKING_STATUS
)
from model_utils import models as django_model_utils

# Create your models here.

class Player(models.Model):
    ROLE = CHOICE_POSITION
    ACTIVE = CHOICE_ACTIVE
    class Meta:
        unique_together = ('role', 'dotaID')

    created = models.DateTimeField()
    mmr = models.PositiveIntegerField()
    behavior_score = models.PositiveIntegerField()
    dotaID = models.CharField(max_length=255)
    role = models.CharField(max_length=255, choices=ROLE)
    is_active = models.BooleanField(default=True)

class Match(django_model_utils.TimeStampedModel):
    LOBBY_TYPE = CHOICE_LOBBY_TYPE
    FETCH_STATUS = CHOICE_STATUS
    class Meta:
        unique_together = ('identifier', 'player')

    remarks = models.CharField(max_length=255, default='')
    fetch_status = models.SmallIntegerField(choices=FETCH_STATUS, default=FETCH_STATUS.pending)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    lobby_type = models.CharField(max_length=255, choices=LOBBY_TYPE)
    has_extra = models.BooleanField(default=False)
    identifier = models.CharField(max_length=255, editable=False)
    

class MatchStats(models.Model):
    SIDE = CHOICE_SIDE

    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    side = models.CharField(max_length=255, choices=SIDE)
    
    assists = models.PositiveIntegerField()
    deaths = models.PositiveIntegerField()
    kills = models.PositiveIntegerField()

    denies = models.PositiveIntegerField()
    last_hits = models.PositiveIntegerField()

    gold_per_min = models.PositiveIntegerField()
    xp_per_min = models.PositiveIntegerField()
    net_worth = models.PositiveIntegerField()

    hero_damage = models.PositiveIntegerField()
    tower_damage = models.PositiveIntegerField()

    hero_healing = models.PositiveIntegerField()

class MatchmakingMatch(django_model_utils.TimeStampedModel):
    STATUS = CHOICE_MATCHMAKING_STATUS

    status = models.PositiveIntegerField(choices=STATUS, default=STATUS.finding)
    remarks = models.CharField(default='', blank=True, null=True, max_length=255)

class MatchmakingGeneration(django_model_utils.TimeStampedModel):
    
    imbalance = models.PositiveIntegerField()
    matchmaking_match = models.ForeignKey(MatchmakingMatch, on_delete=models.CASCADE)
    generation = models.PositiveIntegerField()

    f_mmr = models.PositiveIntegerField()
    f_behavior_score = models.PositiveIntegerField()
    f_fantasy = models.PositiveIntegerField()

class GenerationData(django_model_utils.TimeStampedModel):
    SIDE = CHOICE_SIDE

    side = models.CharField(max_length=255, choices=SIDE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    matchmaking_generation = models.ForeignKey(MatchmakingGeneration, on_delete=models.CASCADE)
    individual_fantasy = models.FloatField()
    

class MatchmakingPool(django_model_utils.TimeStampedModel):
     matchmaking_match = models.ForeignKey(MatchmakingMatch, on_delete=models.DO_NOTHING)
     player = models.ForeignKey(Player, on_delete=models.DO_NOTHING)