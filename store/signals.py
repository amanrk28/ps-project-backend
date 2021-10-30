from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from store.models import Product

@receiver(post_save, sender=Product)
def update_product_availability(sender, instance: Product, **kwargs):
    if instance.stock:
        instance.is_available = True
    else:
        instance.is_available = False
    instance.save()