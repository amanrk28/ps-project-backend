from django.contrib import admin
from .models import ProductItem, Cart, CartItem

# Register your models here.
@admin.register(ProductItem)
class ProductItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('status', 'hash')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('item', 'cart', 'quantity')
