from django.contrib import admin

from .models import Match


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('pk', 'initiator', 'confirmer', 'is_accepted', 'is_declined')
    search_fields = ('initiator', 'confirmer', 'is_accepted', 'is_declined',)
