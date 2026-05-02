from django.contrib import admin

from .models import SimulationStep, UserProgress


@admin.register(SimulationStep)
class SimulationStepAdmin(admin.ModelAdmin):
    list_display = ('hut', 'correct_order', 'preview_order', 'text')
    list_filter = ('hut',)
    search_fields = ('text', 'hut__name')
    ordering = ('hut', 'correct_order')


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'hut', 'completed', 'score', 'completed_at')
    list_filter = ('completed', 'hut')
    search_fields = ('user__username', 'user__email', 'hut__name')
