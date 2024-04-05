import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')
application = get_wsgi_application()

# Now you can import your models and use them
from django.contrib.auth.models import Group, Permission


def create_groups():

    # Create a group
    chef_group = Group.objects.create(name='Chef')

    # Add permissions to the group
    permissions = Permission.objects.filter(codename__in=['add_recipe', 'change_recipe', 'delete_recipe', 'view_recipe'])
    chef_group.permissions.set(permissions)
    chef_group.save()

    viewer_group = Group.objects.create(name='Viewer')

    # Add permission to the group
    permission = Permission.objects.get(codename='view_recipe')
    viewer_group.permissions.add(permission)
    viewer_group.save()


if __name__ == '__main__':
    create_groups()
