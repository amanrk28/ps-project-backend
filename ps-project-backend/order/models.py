from django.db import models
# from datetime import date
from project_backend.models import BaseModel, BaseManager
from project_backend.settings import AUTH_USER_MODEL
from project_backend.utils import compute_hash
from store.models import Product
from authentication.models import get_address


# class OrderBaseManager(BaseManager):
#     def __init__(self, *args, **kwargs):
#         self.with_closed = kwargs.pop('closed', False)
#         super(OrderBaseManager, self).__init__(*args, **kwargs)

#     def get_queryset(self):
#         qs = super(OrderBaseManager, self).get_queryset()
#         if not self.with_closed:
#             qs = qs.filter(closed=False)
#         return qs

class OrderStatus(models.TextChoices):
    NEW = 'new'
    DISPATCHED = 'dispatched'
    CLOSED = 'closed'

# class Order(BaseModel):
#     placed_by = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.PROTECT)
#     status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.NEW)
#     hash = models.CharField(max_length=32, null=True, blank=True, unique=True)
#     order_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
#     delivery_address = models.JSONField(default=get_address)
#     delivery_date = models.DateField(null=True, blank=True)
#     expected_delivery_date = models.DateField(null=True, blank=True)
#     dispatch_date = models.DateField(null=True, blank=True)
#     expected_dispatch_date = models.DateField(null=True, blank=True)
#     closed = models.BooleanField(default=False)
#     payment_details = models.ForeignKey('Payment', on_delete=models.PROTECT)
#     objects = OrderBaseManager()
#     with_closed_objects = OrderBaseManager(closed=True)
#     all_objects = OrderBaseManager(deleted=True, closed=True)

#     class Meta:
#         db_table = 'order'

#     def __str__(self):
#         return '%s | For %s | %s' % (self.id, self.placed_by.first_name, self.status)

#     def save(self, *args, **kwargs):
#         if not self.hash:
#             self.hash = compute_hash(hash_length=32)
#         return super().save(*args, **kwargs)


# class OrderItem(BaseModel):
#     product = models.ForeignKey(Product, on_delete=models.PROTECT)
#     order = models.ForeignKey(Order, on_delete=models.PROTECT)
#     quantity = models.IntegerField(default=1)

#     class Meta:
#         db_table = 'order_details'

#     @property
#     def amount(self):
#         return self.product.price * self.quantity


# class PaymentOptions(models.TextChoices):
#     COD = 'cash on delivery'
#     CARD = 'debit/credit card'

# class Payment(BaseModel):
#     mode_of_payment = models.CharField(max_length=30, choices=PaymentOptions, default=PaymentOptions.COD)
#     total_amount = models.FloatField(null=True, blank=True)
#     is_payment_by_card = models.BooleanField(default=False)
#     card_details = models.ForeignKey('authentication.CardDetails', on_delete=models.PROTECT, null=True, blank=True)

#     class Meta:
#         db_table = 'payment'



# # # Invoice generated after delivery completion and on-demand from user
# # class Invoice(BaseModel):
# #     order = models.ForeignKey(Order, on_delete=models.PROTECT)
# #     invoice_number = models.IntegerField(null=True, blank=True)
# #     invoice_date = models.DateTimeField(null=True, blank=True)
# #     payment_received = models.BooleanField(default=False)
# #     payment_received_on = models.DateField(null=True, blank=True)

# #     class Meta:
# #         db_table = 'invoice'

# #     def __str__(self):
# #         return '%s, %s, %s' % self.id, self.order.id, self.invoice_number

# #     @property
# #     def formatted_invoice_number(self):
# #         if self.invoice_number:
# #             # e.g.: INV-202100024-s5n1xo
# #             return 'INV-{}000{}-{}'.format(date.today().year, str(self.invoice_number), compute_hash(6))
# #         return None