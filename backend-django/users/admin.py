from django.contrib import admin
from django.db.models import Count, Case, Value, When
from django.db import models
from .models import Player
from .choices import (
    CHOICE_MEDAL,
    CHOICE_POSITION,
    HERALD_MAX,
    GUARDIAN_MAX,
    CRUSADER_MAX,
    ARCHON_MAX,
    LEGEND_MAX,
    ANCIENT_MAX,
    DIVINE_MAX,
)

# Register your models here.
class PlayersAdmin(admin.ModelAdmin):
    list_display = ('dotaID', 'created', 'position', 'mmr', 'medal', 'behavior_score', 'visibility')
    search_fields = ('dotaID', )

    def visibility(self, obj):
        result = None

        if obj.is_private:
            result = 'Private'
        elif obj.is_private == False:
            result = 'Public'
        
        return result
    visibility.short_description = 'Visibility'

    def medal(self, obj):
        return CHOICE_MEDAL[int(obj.medal)]
    medal.short_description = 'Medal'

    def position(self, obj):
        print(obj.role)
        return CHOICE_POSITION[int(obj.role)]
    position.short_description = 'Role'

    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def get_queryset(self, request):
        queryset = super(PlayersAdmin, self).get_queryset(request)
        return queryset\
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
            ).order_by('id')

admin.site.register(Player, PlayersAdmin)