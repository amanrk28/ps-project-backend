from django.db import models
from project_backend.models import BaseModel
from project_backend.settings import AUTH_USER_MODEL


class ProductCategory(models.TextChoices):
    FRUITS_AND_VEGETABLES = 'Fruits & Vegetables'
    FOODGRAINS_OIL_MASALA = 'Foodgrains, Oil & Masala'
    DAIRY = 'Dairy'
    BEVERAGES = 'Beverages'
    CLEANING_AND_HOUSEHOLD = 'Cleaning & Household'
    BEAUTY_AND_HYGIENE = 'Beauty & Hygiene'
    SNACKS = 'Snacks'
    NEW = 'New'


class Product(BaseModel):
    added_by = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.PROTECT)
    name = models.CharField(max_length=128, null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    image = models.URLField(max_length=512, null=True, blank=True)
    stock = models.IntegerField(null=True, blank=True)
    is_available = models.BooleanField(default=False, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    category = models.CharField(choices=ProductCategory.choices, max_length=64, default=ProductCategory.NEW)

    def __str__(self):
        return '%s, %s' % (self.id, self.name)

    class Meta:
        db_table = 'product'


class CartStatus(models.TextChoices):
    NEW = 'new'
    ORDERED = 'ordered'


class Cart(BaseModel):
    status = models.CharField(choices=CartStatus.choices, max_length=32, default=CartStatus.NEW)
    hash = models.CharField(max_length=8, unique=True, null=True)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.PROTECT, null=True)

    class Meta:
        db_table = 'cart'

    def __str__(self):
        return '%s, %s - %s' % (self.id, self.user.first_name, self.status)


class CartItem(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='cart_product')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, null=True, blank=True)

    class Meta:
        db_table = 'cart_item'

    def __str__(self):
        return '%s, %s of user %s' % (self.id, self.product.name, self.cart.user.first_name)