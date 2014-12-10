from django.contrib import admin
from picks.models import Game, Team

class TeamInline(admin.TabularInline):
    model = Team
    extra = 2
    
class GameAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['game']}),
        ('Game information', {'fields': ['kickoff_time',
                                         'weight',
                                         'season'],}),
    ]
    inlines = [TeamInline]

admin.site.register(Game, GameAdmin)
