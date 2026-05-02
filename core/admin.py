from django.contrib import admin

from .models import SiteViewerSettings


@admin.register(SiteViewerSettings)
class SiteViewerSettingsAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'public_show_virtual_village',
        'public_show_marketplace',
        'public_show_experience_bookings',
        'public_show_cultural_guide',
        'updated_at',
    )

    def has_add_permission(self, request):
        return not SiteViewerSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
