from django.contrib import admin
from .models import Item, Order, Discount, Tax

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'currency']

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['name', 'percent_off']

@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ['name', 'percentage']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'total_price', 'created_at']