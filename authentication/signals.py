import random
import uuid
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from .models import AuthToken, User

@receiver(pre_save, sender=User)
def fill_admin(sender, instance, **kwargs):
    if not instance.username:
        if instance.first_name and instance.last_name:
            instance.username = '{}{}_{}'.format(instance.first_name[0].lower(), instance.last_name.lower(),
                                                 random.randint(1, 10000))
        elif instance.first_name:
            instance.username = '{}_{}'.format(instance.first_name.lower(),
                                               random.randint(1, 10000))
        elif instance.last_name:
            instance.username = '{}_{}'.format(instance.last_name.lower(),
                                               random.randint(1, 10000))
        else:
            instance.username = uuid.uuid4().hex
    if not instance.is_active:
        instance.is_active = True