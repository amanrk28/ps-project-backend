from django.db import models

# Create your models here.
class OrderStatus(models.TextChoices):
    NEW = 'new'
    DISPATCHED = 'dispatched'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'