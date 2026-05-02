from django.db import models
from django.conf import settings

from village.models import Hut


class Experience(models.Model):
    STATUS_TAKING_REQUESTS = 'taking_requests'
    STATUS_PREVIEW = 'preview'
    STATUS_CHOICES = [
        (STATUS_TAKING_REQUESTS, 'Taking requests'),
        (STATUS_PREVIEW, 'Preview'),
    ]

    hut = models.ForeignKey(Hut, on_delete=models.PROTECT, related_name='experiences')
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=150)
    host = models.CharField(max_length=140)
    duration = models.CharField(max_length=80)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=8, default='LKR')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default=STATUS_TAKING_REQUESTS)
    summary = models.TextField()
    includes = models.JSONField(default=list)
    is_published = models.BooleanField(default=True)
    display_order = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'title']

    def __str__(self):
        return self.title

    @property
    def formatted_price(self):
        return f'{self.currency} {self.price:,.0f}'

    @property
    def status_label(self):
        return self.get_status_display()

    @property
    def hut_slug(self):
        return self.hut.slug

    @property
    def hut_name(self):
        return self.hut.name


class BookingRequest(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_CONFIRMED, 'Confirmed'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]

    experience = models.ForeignKey(Experience, on_delete=models.PROTECT, related_name='booking_requests')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    preferred_date = models.DateField()
    guests = models.PositiveSmallIntegerField()
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.experience} request for {self.preferred_date}'
