from django.contrib import admin

from .models import Order, OrderItem, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'hut', 'status', 'formatted_price', 'stock', 'is_published')
    list_filter = ('status', 'is_published', 'hut')
    search_fields = ('name', 'summary', 'artisan')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('display_order', 'name')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'unit_price')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('reference', 'customer_email', 'formatted_total', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('reference', 'customer_name', 'customer_email')
    readonly_fields = ('reference', 'total', 'created_at')
    inlines = [OrderItemInline]
