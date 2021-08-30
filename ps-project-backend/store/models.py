from django.db import models
from project_backend.models import BaseModel
# Create your models here.
class ProductItem(BaseModel):
    name = models.CharField(max_length=128, null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    image = models.URLField(max_length=512, null=True, blank=True)
    stock = models.IntegerField(null=True, blank=True)
    is_available = models.BooleanField(default=False, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = 'product_item'

class CartStatus(models.TextChoices):
    NEW = 'new'
    ORDERED = 'ordered'

class Cart(BaseModel):
    status = models.CharField(choices=CartStatus.choices, max_length=32, default=CartStatus.ORDERED)
    hash = models.CharField(max_length=8, unique=True, null=True)

class CartItem(BaseModel):
    item = models.ForeignKey(ProductItem, on_delete=models.PROTECT, related_name='cart_product_item')
    cart = models.ForeignKey(Cart, on_delete=models.PROTECT)
    quantity = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'cart_item'