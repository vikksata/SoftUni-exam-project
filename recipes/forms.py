from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Recipe, Comment


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
        fields = ['title', 'categories', 'description', 'ingredients', 'instructions', 'image_url']


class EditRecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = ['title', 'categories', 'description', 'ingredients', 'instructions', 'image_url']


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'age', 'user_type')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.user_type == 'chef':
            self.fields['user_type'].disabled = True


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'cols': 40, 'placeholder': 'Enter your comment here...'})
        }
