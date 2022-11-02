from model_utils import Choices

CHOICE_POSITION = Choices(
    (1, 'hard_carry', 'Hard Carry'),
    (2, 'mid_lane', 'Mid Lane'),
    (3, 'off_lane', 'Off Lane'),
    (4, 'soft_support', 'Soft Support'),
    (5, 'hard_support', 'Hard Support'),
)

CHOICE_MEDAL = Choices(
    (0, 'unranked', 'Unranked'),
    (1, 'herald', 'Herald'),
    (2, 'guardian', 'Guardian'),
    (3, 'crusader', 'Crusader'),
    (4, 'archon', 'Archon'),
    (5, 'legend', 'Legend'),
    (6, 'ancient', 'Ancient'),
    (7, 'divine', 'Divine'),
    (8, 'immortal', 'Immortal'),
)

CHOICE_SIDE = Choices(
    (0, 'radiant', 'Radiant'),
    (1, 'dire', 'Dire')
)

CHOICE_LOBBY_TYPE = Choices(
    (0, 'public_matchmaking', 'Public Matchmaking'),
    (1, 'practice', 'Practice'),
    (2, 'tournament', 'Tournament'),
    (3, 'tutorial', 'Tutorial'),
    (4, 'coop_w_bots', 'Coop with Bots'),
    (5, 'team_match', 'Team Match'),
    (6, 'solo_queue', 'Solo Queue'),
    (7, 'ranked', 'Ranked'),
    (8, '1v1_mid', '1v1 Mid'),

)

CHOICE_STATUS = Choices(
    (0, 'pending', 'Pending'),
    (1, 'success', 'Success'),
    (2, 'failed', 'Failed')
)

CHOICE_ACTIVE = Choices(
    (0, 'inactive', 'Inactive'),
    (1, 'active', 'Active')
)

CHOICE_MATCHMAKING_STATUS = Choices(
    (0, 'finding', 'Finding'),
    (1, 'found', 'Found'),
    (2, 'failed', 'Failed')
)

HERALD_MAX = 616
GUARDIAN_MAX = 1386
CRUSADER_MAX = 2156
ARCHON_MAX = 2926
LEGEND_MAX = 3696
ANCIENT_MAX = 4466
DIVINE_MAX = 5420
