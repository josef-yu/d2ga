from operator import itemgetter
from .models import Player, Match, MatchStats, MatchmakingGeneration, GenerationData
from django.db.models import Avg, Count
from django.db import transaction

import random
import time
import copy
from collections import defaultdict
import numpy

from itertools import combinations

from .task import save_generation_data, save_pool

def init_kwargs(model, mutablemapping):
    model_fields = [f.name for f in model._meta.get_fields()]
    return {k: mutablemapping[k] for k in mutablemapping if k in model_fields}

def filter_data(model, response):
    model_fields = [f.name for f in model._meta.get_fields()]
    return {k: response[k] for k in response.keys() if k in model_fields}

def calc_pnorm(listA, listB, p):
    sumA = sum([x ** p for x in listA])
    sumB = sum([x ** p for x in listB])
    return abs((sumA ** (1/p)) - (sumB ** (1/p)))

def calc_qnorm(listA, listB, q):
    Z = listA + listB
    if len(Z) == 0:
        return 0
    average_z = sum(Z) / len(Z)
    summation = sum([ abs(x - average_z) ** q for x in Z ])
    return (summation / abs(sum(Z))) ** (1/q)

def calc_matchstats(matches, role):
    if len(matches) == 0:
        return {
            'fantasy': None,
            'score': 0
        }
    summation = matches.aggregate(
        kills=Avg('kills'),
        deaths=Avg('deaths'),
        assists=Avg('assists'),
        gold_per_min=Avg('gold_per_min'),
        xp_per_min=Avg('xp_per_min'),
        net_worth=Avg('net_worth'),
        last_hits=Avg('last_hits'),
        denies=Avg('denies'),
        hero_damage=Avg('hero_damage'),
        tower_damage=Avg('tower_damage'),
        hero_healing=Avg('hero_healing')
    )
    fantasy = {
        'kills': summation['kills'] * 0.3,
        'deaths': summation['deaths'] * -0.3,
        'assists': summation['assists'] * 0.15,
        'last_hits': summation['last_hits'] * 0.003,
        'gold_per_min': summation['gold_per_min'] * 0.002,
        'xp_per_min': summation['xp_per_min'] * 0.002,
        'hero_healing': summation['hero_healing'] * 0.4 / 1000
    }

    role = int(role)

    if role == Player.ROLE.hard_carry:
        fantasy['hero_damage'] = summation['hero_damage'] * 0.5 / 1000
        fantasy['tower_damage'] = summation['tower_damage'] * 0.3 / 1000
        fantasy['deaths'] *= 1.5
        fantasy['net_worth'] = summation['net_worth'] * 0.5 / 1000
        fantasy['last_hits'] *= 1.5
    elif role == Player.ROLE.mid_lane:
        fantasy['denies'] = summation['denies'] * 0.005
        fantasy['last_hits'] *= 1.5
        fantasy['hero_damage'] = summation['hero_damage'] * 0.5 / 1000
        fantasy['tower_damage'] = summation['tower_damage'] * 0.3 / 1000
        fantasy['net_worth'] = summation['net_worth'] * 0.5 / 1000
        fantasy['xp_per_min'] *= 1.5
        fantasy['deaths'] *= 1.5
    elif role == Player.ROLE.off_lane:
        fantasy['xp_per_min'] *= 1.2
        fantasy['deaths'] *= 1.2
        fantasy['hero_damage'] = summation['hero_damage'] * 0.5 / 1000
        fantasy['tower_damage'] = summation['tower_damage'] * 0.3 / 1000
    elif role == Player.ROLE.soft_support:
        fantasy['assists'] *= 2
        fantasy['hero_healing'] *= 1.5
        fantasy['denies'] = summation['denies'] * 0.005
        fantasy['hero_damage'] = summation['hero_damage'] * 0.3 / 1000
    elif role == Player.ROLE.hard_support:
        fantasy['assists'] *= 2
        fantasy['hero_healing'] *= 2
        fantasy['denies'] = summation['denies'] * 0.005
        fantasy['hero_damage'] = summation['hero_damage'] * 0.3 / 1000

    return {
        'breakdown': fantasy, 
        'score': sum([f for f in fantasy.values()])
    }

class GA:

    def __init__(self, queryset, matchmaking_id):
        self.queryset = queryset
        self.matchmaking_id = matchmaking_id
        self.generation = 1
        self.found = False
        self.optimal_generation = 1
        self.pop_size = 0
        self.toleration = 25
    
    def form_teams(self, matchmaking_pool):
        teams = []
        picked = []
        # Two teams
        for a in range(0, 2):
            team = []
            # 5 players in one team
            for n in range(1, 6):
                loop = True
                temp = []
                available_players = self.queryset.filter(role=n)
                for p in available_players:
                    matches = Match.objects\
                        .filter(player=p, fetch_status=Match.FETCH_STATUS.success)
                    
                    num_matches = matches.aggregate(count=Count('id'))
                    matches_stats = []
                    if num_matches['count'] > 0:
                        matches_stats = MatchStats.objects.filter(match__in=matches)

                    temp.append({
                        'player': p,
                        'matches': matches_stats
                    })
                
                while loop:
                    player = random.choice(list(temp))
                    if player['player'].dotaID in picked:
                        continue


                    if len(player['matches']) > 0:
                        fantasy = calc_matchstats(player['matches'], player['player'].role)
                        player['fantasy'] = fantasy
                        picked.append(player['player'].dotaID)
                        matchmaking_pool.append(player['player'].dotaID)
                        team.append(player)
                        loop = False

                
            if len(team) < 5:
                print([p['player'].role for p in team])
                return []
            teams.append(team)
        return teams

    
    def init_population(self):
        players = []
        matchmaking_pool = []

        for n in range(0, len(list(self.queryset))):
            teams = self.form_teams(matchmaking_pool)

            if len(teams) == 2:
                players.append(teams)
        
        self.pop_size = len(players)
        save_pool.delay(matchmaking_pool, self.matchmaking_id)

        return players

    def evaluate(self, teams):
        teamA_mmr = [p['player'].mmr for p in teams[0]]
        teamB_mmr = [p['player'].mmr for p in teams[1]]

        # Calculates per team mmr fairness and uniformity
        mmr_fairness = calc_pnorm(
            listA=teamA_mmr, 
            listB=teamB_mmr, 
            p=2
        )
        mmr_uniformity = calc_qnorm(
            listA=teamA_mmr, 
            listB=teamB_mmr, 
            q=2
        )

        role_mmr_fairness = []
        role_mmr_uniformity = []

        # Calculates per role mmr fairness and uniformity
        # 
        for n in range(5):
            for radiant, dire in zip(teamA_mmr, teamB_mmr):
                mmr_f = calc_pnorm([radiant], [dire], p=2)
                mmr_u = calc_qnorm([radiant], [dire], q=2)

                role_mmr_fairness.append(mmr_f)
                role_mmr_uniformity.append(mmr_u)
                
        role_mmr_fairness.append(mmr_fairness)
        role_mmr_uniformity.append(mmr_uniformity)

        teamA_behavior = [p['player'].behavior_score for p in teams[0]]
        teamB_behavior = [p['player'].behavior_score for p in teams[1]]
        behavior_fairness = calc_pnorm(
            listA=teamA_behavior, 
            listB=teamB_behavior, 
            p=2
        )
        behavior_uniformity = calc_qnorm(
            listA=teamA_behavior, 
            listB=teamB_behavior, 
            q=2
        )

        teamA_stats = [p['fantasy'] for p in teams[0]]
        teamB_stats = [p['fantasy'] for p in teams[1]]
        stats_fairness = calc_pnorm(
            listA=[f['score'] for f in teamA_stats],
            listB=[f['score'] for f in teamB_stats],
            p=2
        )
        stats_uniformity = calc_qnorm(
            listA=[f['score'] for f in teamA_stats],
            listB=[f['score'] for f in teamB_stats],
            q=2
        )

        f_mmr = 0
        for f, u in zip(role_mmr_fairness, role_mmr_uniformity):
            f_mmr += (0.2 * f) + (0.8 * u)

        f_behavior = (0.5 * behavior_fairness) + (0.5 * behavior_uniformity)
        f_fantasy = (0.7 * stats_fairness) + (0.3 * stats_uniformity)

        imbalance = (0.5 * f_mmr) + (0.15 * f_behavior) - (0.35 * f_fantasy)

        radiant = [{
            'dotaID': p['player'].dotaID,
            'mmr': p['player'].mmr,
            'behavior_score': p['player'].behavior_score,
            'role': p['player'].role,
            'fantasy': p['fantasy'],
            'player': p['player'],
            'matches': p['matches']
        } for p in teams[0]]

        dire = [{
            'dotaID': p['player'].dotaID,
            'mmr': p['player'].mmr,
            'behavior_score': p['player'].behavior_score,
            'role': p['player'].role,
            'fantasy': p['fantasy'],
            'player': p['player'],
            'matches': p['matches'],
            
        } for p in teams[1]]

        return {
            'imbalance': imbalance,
            'f_mmr': f_mmr,
            'f_behavior': f_behavior,
            'f_fantasy': f_fantasy,
            'radiant': radiant,
            'dire': dire
        }
    
    def mutate(self, offsprings):
        for n in range(2):
            rand_int = random.randint(1,100)
            if rand_int <= 25:
                role_to_swap = random.randint(0,4)

                temp = offsprings[n]['radiant'][role_to_swap]
                offsprings[n]['radiant'][role_to_swap] = offsprings[n]['dire'][role_to_swap]
                offsprings[n]['dire'][role_to_swap] = temp

        return offsprings
    
    def crossover_and_mutation(self, parents):
        choice = random.choice(['radiant', 'dire'])
        gene_side = 'dire' if choice == 'radiant' else 'radiant'

        offsprings = [
            {'radiant': [], 'dire': []}, 
            {'radiant': [], 'dire': []}
        ]
        
        offsprings[0][choice] = parents[1][choice][:]
        offsprings[1][choice] = parents[0][choice][:]

        offsprings[0][gene_side] = parents[0][gene_side][:]
        offsprings[1][gene_side] = parents[1][gene_side][:]

        loop = True

        # Swap duplicate players to other offspring
        # Loop until duplicates are not found
        while loop:
            loop = False
            to_swap = []
            for offspring in offsprings:
                choice_players = [p['dotaID'] for p in offspring[choice]]
                gene_players = [p['dotaID'] for p in offspring[gene_side]]

                for index, p in enumerate(gene_players):
                    if p in choice_players and not index in to_swap:
                        loop = True
                        to_swap.append(index)

            for index in to_swap:
                temp = offsprings[1][gene_side][index]
                offsprings[1][gene_side][index] = offsprings[0][gene_side][index]
                offsprings[0][gene_side][index] = temp
        
        offsprings = self.mutate(offsprings)

        offsprings[0]['radiant'].sort(key=lambda x: x['role'])
        offsprings[0]['dire'].sort(key=lambda x: x['role'])

        offsprings[1]['radiant'].sort(key=lambda x: x['role'])
        offsprings[1]['dire'].sort(key=lambda x: x['role'])

        return offsprings

    def dominates(self, obj1, obj2, sign=[-1, -1]):
        indicator = False
        for a, b, sign in zip(obj1, obj2, sign):
            if a * sign > b * sign:
                indicator = True
            # if one of the objectives is dominated, then return False
            elif a * sign < b * sign:
                return False
        return indicator
    
    def sortNondominated(self, fitness, k=None, first_front_only=False):
        """
        Fast Nondominated Sorting Approach" proposed by Deb et al.,
        see [Deb2002]_. Credits to https://medium.com/@rossleecooloh
        """
        if k is None:
            k = len(fitness)

        # Use objectives as keys to make python dictionary
        map_fit_ind = defaultdict(list)
        for i, f_value in enumerate(fitness):  # fitness = [(1, 2), (2, 2), (3, 1), (1, 4), (1, 1)...]
            map_fit_ind[f_value].append(i)
        fits = list(map_fit_ind.keys())  # fitness values

        current_front = []
        next_front = []
        dominating_fits = defaultdict(int)  # n (The number of people dominate you)
        dominated_fits = defaultdict(list)  # Sp (The people you dominate)

        # Rank first Pareto front
        # *fits* is a iterable list of chromosomes. Each has multiple objectives.
        for i, fit_i in enumerate(fits):
            for fit_j in fits[i + 1:]:
                # Eventhougn equals or empty list, n & Sp won't be affected
                if self.dominates(fit_i, fit_j):
                    dominating_fits[fit_j] += 1  
                    dominated_fits[fit_i].append(fit_j)  
                elif self.dominates(fit_j, fit_i):  
                    dominating_fits[fit_i] += 1
                    dominated_fits[fit_j].append(fit_i)
            if dominating_fits[fit_i] == 0: 
                current_front.append(fit_i)

        fronts = [[]]  # The first front
        for fit in current_front:
            fronts[-1].extend(map_fit_ind[fit])
        pareto_sorted = len(fronts[-1])

        # Rank the next front until all individuals are sorted or
        # the given number of individual are sorted.
        # If Sn=0 then the set of objectives belongs to the next front
        if not first_front_only:  # first front only
            N = min(len(fitness), k)
            while pareto_sorted < N:
                fronts.append([])
                for fit_p in current_front:
                    # Iterate Sn in current fronts
                    for fit_d in dominated_fits[fit_p]: 
                        dominating_fits[fit_d] -= 1  # Next front -> Sn - 1
                        if dominating_fits[fit_d] == 0:  # Sn=0 -> next front
                            next_front.append(fit_d)
                            # Count and append chromosomes with same objectives
                            pareto_sorted += len(map_fit_ind[fit_d]) 
                            fronts[-1].extend(map_fit_ind[fit_d])
                current_front = next_front
                next_front = []

        return fronts
    
    def crowding_distance(self, fitness):
        """
        Credits to https://medium.com/@rossleecooloh
        """
        distances = [0.0] * len(fitness)
        crowd = [(f_value, i) for i, f_value in enumerate(fitness)]  # create keys for fitness values

        n_obj = len(fitness[0])

        for i in range(n_obj):  # calculate for each objective
            crowd.sort(key=lambda element: element[0][i])
            # After sorting,  boundary solutions are assigned Inf 
            # crowd: [([obj_1, obj_2, ...], i_0), ([obj_1, obj_2, ...], i_1), ...]
            distances[crowd[0][1]] = float("Inf")
            distances[crowd[-1][1]] = float("inf")
            if crowd[-1][0][i] == crowd[0][0][i]:  # If objective values are same, skip this loop
                continue
            # normalization (max - min) as Denominator
            norm = float(crowd[-1][0][i] - crowd[0][0][i])
            # crowd: [([obj_1, obj_2, ...], i_0), ([obj_1, obj_2, ...], i_1), ...]
            # calculate each individual's Crowding Distance of i th objective
            # technique: shift the list and zip
            for prev, cur, next in zip(crowd[:-2], crowd[1:-1], crowd[2:]):
                distances[cur[1]] += (next[0][i] - prev[0][i]) / norm  # sum up the distance of ith individual along each of the objectives

        return distances
    
    @transaction.atomic()
    def select(self, candidates):
        candidates = sorted(candidates, key=itemgetter('f_mmr', 'f_behavior', 'f_fantasy'))

        fitness = [(int(c['f_mmr']), int(c['f_behavior']), int(c['f_fantasy'])) for c in candidates]
        nondominated = self.sortNondominated(fitness)
        cd = self.crowding_distance(fitness)

        for index, c in enumerate(candidates):
            for rank, n in enumerate(nondominated):
                if index in n:
                    candidates[index]['rank'] = rank+1
            
            candidates[index]['cd'] = cd[index]
        
        candidates = sorted(candidates, key=lambda x: (x['rank'], -x['cd']))

        g_parents = []
        picked = []
        for n in range(int(len(candidates)/2)):
            while True:
                aspirants = [random.choice(candidates) for i in range(random.randint(5, 10))]
                aspirants = sorted(aspirants, key=lambda x: (x['rank'], -x['cd']))

                parents = [aspirants[0], aspirants[1]]

                p1 = []
                p1 += [p['dotaID'] for p in aspirants[0]['radiant']]
                p1 += [p['dotaID'] for p in aspirants[0]['dire']]

                p2 = []
                p2 += [p['dotaID'] for p in aspirants[1]['radiant']]
                p2 += [p['dotaID'] for p in aspirants[1]['dire']]


                if not [p1,p2] in picked:
                    g_parents.append(parents)
                    picked.append([p1, p2])
                    break

        for index, teams in enumerate(candidates):
            gen = MatchmakingGeneration.objects.create(
                    generation=self.generation,
                    imbalance=teams['imbalance'],
                    matchmaking_match_id=self.matchmaking_id,
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

        return g_parents, candidates
    
    
    def execute(self):
        population = self.init_population()
        candidates = []
        
        for teams in population:
            offspring_pair = self.evaluate(teams)
            candidates.append(offspring_pair)
            

        candidates.sort(key=lambda x: x['imbalance'])
        minimal_imbalance = candidates[0]['imbalance']
        optimal = copy.deepcopy(candidates[0])

        iteration = 1
        loop = True

        while iteration <= self.toleration and minimal_imbalance > 0 and loop:
            print(f'Generation: {self.generation}')
            g_parents, candidates = self.select(candidates)

            new_population = []
            for parents in g_parents:
                offsprings = self.crossover_and_mutation(parents)
                
                offspring_pair = []

                for offspring in offsprings:
                    offspring_pair.append(
                        self.evaluate([offspring['radiant'], offspring['dire']])
                    )


                new_population += offspring_pair

                if offspring_pair[0]['imbalance'] < minimal_imbalance:
                    minimal_imbalance = int(offspring_pair[0]['imbalance'])
                    optimal = copy.deepcopy(offspring_pair[0])
                    self.optimal_generation = self.generation
                    iteration = 1
                    continue
                elif offspring_pair[1]['imbalance'] < minimal_imbalance:
                    minimal_imbalance = int(offspring_pair[1]['imbalance'])
                    optimal = copy.deepcopy(offspring_pair[1])
                    self.optimal_generation = self.generation
                    iteration = 1
                    continue
            
            candidates = new_population
            
            self.generation += 1
            iteration += 1


        optimal = self.evaluate([optimal['radiant'], optimal['dire']])    

        if len(optimal['radiant']) == 0 or len(optimal['dire']) == 0:
            return self.found
        
        self.found = True

        optimal['radiant'].sort(key=lambda x: x['role'])
        optimal['dire'].sort(key=lambda x: x['role'])

        for player in optimal['radiant']:
            player['role'] = Player.ROLE[int(player['role'])]
        
        for player in optimal['dire']:
            player['role'] = Player.ROLE[int(player['role'])]
        
        
        gen = MatchmakingGeneration.objects.create(
            generation=self.optimal_generation,
            imbalance=optimal['imbalance'],
            matchmaking_match_id=self.matchmaking_id,
            f_mmr=optimal['f_mmr'],
            f_behavior_score=optimal['f_behavior'],
            f_fantasy=optimal['f_fantasy']
        )

        for player in optimal['radiant']:
            GenerationData.objects.create(
                side=GenerationData.SIDE.radiant,
                player=player['player'],
                matchmaking_generation=gen,
                individual_fantasy=player['fantasy']['score']
            )
        
        for player in optimal['dire']:
            GenerationData.objects.create(
                side=GenerationData.SIDE.dire,
                player=player['player'],
                matchmaking_generation=gen,
                individual_fantasy=player['fantasy']['score']
            )
            

        
        print(f'Final minimum is: {minimal_imbalance}')
        return self.found