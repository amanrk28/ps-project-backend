from django.db import models
from project_backend.models import BaseModel
from project_backend.settings import AUTH_USER_MODEL
from project_backend.utils import compute_hash
# Create your models here.
class OrderStatus(models.TextChoices):
    NEW = 'new'
    DISPATCHED = 'dispatched'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'

# class Order(BaseModel):
#     order_id = models.CharField(max_length=16, null=True, blank=True)
#     added_by = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.PROTECT)
#     status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.NEW)
#     is_delivered = models.BooleanField(default=False)
#     delivered_on = models.DateTimeField(null=True, blank=True)


#     class Meta:
#         db_table = 'order'

#     def save(self, *args, **kwargs):
#         if not self.order_id:
#             self.order_id = compute_hash(hash_length=16)
#         return super().save(*args, **kwargs)
