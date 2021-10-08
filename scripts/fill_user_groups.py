from django.contrib.auth.models import Group, Permission
from authentication.models import User

USER_GROUP_ADMIN = 'admin'
USER_GROUP_CUSTOMER = 'customer'
USER_GROUP_SUPERUSER = 'superuser'

for it in [USER_GROUP_SUPERUSER, USER_GROUP_ADMIN, USER_GROUP_CUSTOMER]:
    try:
        Group.objects.get(name=it)
    except Group.DoesNotExist:
        Group.objects.create(name=it)

customer_permissions = ['add_cart', 'view_cart', 'add_cartitem', 'view_cartitem', 'change_cartitem', 'delete_cartitem',
                        'view_product', 'add_order', 'view_order', 'add_orderitem', 'view_orderitem']

admin_permissions = ['view_order', 'change_order', 'view_cart', 'view_cartitem', 'add_product', 'view_product',
                     'change_product', 'delete_product', 'view_user', 'view_orderitem']

superuser_permissions = Permission.objects.all()

g_admin = Group.objects.get(name=USER_GROUP_ADMIN)
for it in admin_permissions:
    g_admin.permissions.add(Permission.objects.get(codename=it))

g_customer = Group.objects.get(name=USER_GROUP_CUSTOMER)
for it in customer_permissions:
    g_customer.permissions.add(Permission.objects.get(codename=it))

g_superuser = Group.objects.get(name=USER_GROUP_SUPERUSER)
for it in superuser_permissions:
    g_superuser.permissions.add(it)

for it in User.objects.all():
    if it.is_superuser:
        it.groups.add(g_superuser)
    elif it.is_store_owner:
        it.groups.add(g_admin)
    else:
        it.groups.add(g_customer)

print('Success')