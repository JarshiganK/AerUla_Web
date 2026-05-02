from django.contrib import admin

from .models import Hut


@admin.register(Hut)
class HutAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'display_order', 'is_active', 'updated_at')
    list_filter = ('status', 'is_active')
    search_fields = ('name', 'short_name', 'summary')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('display_order', 'name')
