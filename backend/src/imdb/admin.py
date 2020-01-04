from django.contrib import admin

from .models import IMDbBasics


@admin.register(IMDbBasics)
class IMDbBasicsAdmin(admin.ModelAdmin):
    list_filter = ("is_adult", "title_type")
    search_fields = ('primary_title',)