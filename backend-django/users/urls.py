from . import views
from django.urls import path
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('count/role', views.PlayerRoleCountView.as_view()),
    path('count/medal', views.PlayerMedalCountView.as_view()),
    path('match/count/role', views.MatchRoleCountView.as_view()),
    path('match/count/medal', views.MatchMedalCountView.as_view()),
    path('average/<role>', views.MatchStatsAverageView.as_view()),
    path('sheets/sync', views.SyncSheetsDataView.as_view()),
    path('matches/<player_id>', views.FetchPlayerMatchView.as_view()),
    path('matchmaking', views.FindMatchView.as_view()),
    path('matchmaking/pool/<matchmaking_id>', views.MatchmakingPoolView.as_view())
]

router = DefaultRouter()

router.register(
    r'players',
    views.PlayerViewSet,
    basename='players'
)

urlpatterns += router.urls