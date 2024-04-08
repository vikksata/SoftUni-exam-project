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


class RecipeCategory(models.Model):
    MAIN_STARTER = 'main_starter'
    MAIN_COURSE = 'main_course'
    DESSERT = 'dessert'

    CATEGORY_CHOICES = [
        (MAIN_STARTER, 'Main Starter'),
        (MAIN_COURSE, 'Main Course'),
        (DESSERT, 'Dessert'),
    ]

    name = models.CharField(max_length=100, choices=CATEGORY_CHOICES, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.get_name_display()


class Recipe(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ingredients = models.TextField()
    instructions = models.TextField()
    image_url = models.URLField(null=False, blank=False, verbose_name="Image URL:", default='default_url')
    categories = models.ManyToManyField(RecipeCategory, related_name='recipes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Favorite(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
