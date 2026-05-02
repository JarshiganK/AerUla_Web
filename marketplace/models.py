from django.db import models
from django.conf import settings

from village.models import Hut


class Product(models.Model):
    STATUS_AVAILABLE = 'available'
    STATUS_LIMITED = 'limited'
    STATUS_PREVIEW = 'preview'
    STATUS_CHOICES = [
        (STATUS_AVAILABLE, 'Available'),
        (STATUS_LIMITED, 'Limited'),
        (STATUS_PREVIEW, 'Preview'),
    ]

    hut = models.ForeignKey(Hut, on_delete=models.PROTECT, related_name='products')
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=140)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=8, default='LKR')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_AVAILABLE)
    summary = models.TextField()
    artisan = models.CharField(max_length=140)
    materials = models.CharField(max_length=180)
    stock = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    display_order = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name

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


class Order(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_PLACED = 'placed'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_PLACED, 'Placed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    reference = models.CharField(max_length=24, unique=True)
    customer_name = models.CharField(max_length=140)
    customer_email = models.EmailField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PLACED)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.reference

    @property
    def formatted_total(self):
        return f'LKR {self.total:,.0f}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.product.name} x {self.quantity}'

    @property
    def line_total(self):
        return self.quantity * self.unit_price
