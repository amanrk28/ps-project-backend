from django.contrib import admin
from order.models import Order, OrderItem
# Register your models here.
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('placed_by', 'status', 'order_date', 'expected_delivery_date')
    list_filter = ('closed', 'status')
    readonly_fields = ('created_on',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')