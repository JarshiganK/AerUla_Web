from django.db import models


class SiteViewerSettings(models.Model):
    """Singleton (pk=1). Controls what public visitors see; staff/users with operator role bypass gates."""

    public_show_virtual_village = models.BooleanField(default=True)
    public_show_marketplace = models.BooleanField(default=True)
    public_show_experience_bookings = models.BooleanField(default=True)
    public_show_cultural_guide = models.BooleanField(default=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Site viewer settings'
        verbose_name_plural = 'Site viewer settings'

    def __str__(self):
        return 'Public visitor controls'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(
            pk=1,
            defaults={
                'public_show_virtual_village': True,
                'public_show_marketplace': True,
                'public_show_experience_bookings': True,
                'public_show_cultural_guide': True,
            },
        )
        return obj
