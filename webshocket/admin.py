from django.contrib import admin
from user.models import User
# Register your models here.
from django.contrib.auth.models import Group

admin_group, created = Group.objects.get_or_create(name='Admin')


from django.contrib.auth.models import Permission

admin_permissions = [
    'view_user',
    'add_user',
    'change_user',
    'delete_user',
    # ... any other permissions you want to assign
]

for permission in admin_permissions:
    perm = Permission.objects.get(codename=permission)
    admin_group.permissions.add(perm)



admin_user = User.objects.get(username='anurag')
admin_user.groups.add(admin_group)