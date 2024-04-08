from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Recipe


class RegistrationForm(UserCreationForm):
    USER_TYPE_CHOICES = (
        ('chef', 'Chef'),
        ('viewer', 'Viewer'),
    )
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'age', 'password1', 'password2', 'user_type')


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'ingredients', 'instructions', 'image_url']


class EditRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'ingredients', 'instructions', 'image_url']
