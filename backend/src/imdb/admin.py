from django.contrib import admin

from .models import Title, Episode, Rating


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_filter = ("is_adult", "title_type")
    search_fields = ('primary_title',)

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):

    def has_change_permission(self, request, obj=None):
        return False
