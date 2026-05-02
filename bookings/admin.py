from django.contrib import admin

from .models import BookingRequest, Experience


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('title', 'hut', 'host', 'status', 'formatted_price', 'is_published')
    list_filter = ('status', 'is_published', 'hut')
    search_fields = ('title', 'host', 'summary')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('display_order', 'title')


@admin.register(BookingRequest)
class BookingRequestAdmin(admin.ModelAdmin):
    list_display = ('experience', 'preferred_date', 'guests', 'status', 'created_at')
    list_filter = ('status', 'preferred_date')
    search_fields = ('experience__title', 'user__username', 'user__email', 'notes')
