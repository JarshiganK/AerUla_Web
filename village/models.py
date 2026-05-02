from django.db import models


class Hut(models.Model):
    STATUS_AVAILABLE = 'available'
    STATUS_LOCKED = 'locked'
    STATUS_CHOICES = [
        (STATUS_AVAILABLE, 'Available'),
        (STATUS_LOCKED, 'Locked'),
    ]

    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=120)
    short_name = models.CharField(max_length=60)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_AVAILABLE)
    position_class = models.CharField(max_length=80)
    summary = models.TextField()
    activity = models.CharField(max_length=180)
    badge_title = models.CharField(max_length=120)
    story = models.TextField()
    display_order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name

    @property
    def badge(self):
        return self.badge_title
