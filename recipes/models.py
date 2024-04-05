from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, Group


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('chef', 'Chef'),
        ('viewer', 'Viewer'),
    )
    age = models.IntegerField(null=True, blank=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.is_staff = self.is_superuser or self.user_type == 'chef'
        super().save(*args, **kwargs)

        if self.user_type == 'chef':
            self.groups.set([Group.objects.get(name='Chef')])
        elif self.user_type == 'viewer':
            self.groups.set([Group.objects.get(name='Viewer')])


class Recipe(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ingredients = models.TextField()
    instructions = models.TextField()
    image_url = models.URLField(null=False, blank=False, verbose_name="Image URL:", default='default_url')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Favorite(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
