from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, TemplateView

from .models import Recipe, CustomUser
from .forms import RecipeForm, EditRecipeForm
from .forms import RegistrationForm


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_type = form.cleaned_data.get('user_type')

            # Create the group if it doesn't exist
            group_name = user_type.capitalize() + 's'
            group, created = Group.objects.get_or_create(name=group_name)

            user.groups.add(group)  # Add the user to the chosen group
            login(request, user)
            return redirect("login")
        else:
            for msg in form.error_messages:
                print(form.error_messages[msg])

    form = RegistrationForm
    return render(request=request, template_name="registration/register.html", context={"form": form})


def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, 'homepage/home_with_profile.html', {'recipes': recipes})


def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})


@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            return redirect('profile')
    else:
        form = RecipeForm()
    return render(request, 'recipes/recipe_add.html', {'form': form})


@login_required
def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if request.method == 'POST':
        form = EditRecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('recipe_detail', recipe_id=recipe.id)
    else:
        form = EditRecipeForm(instance=recipe)
    return render(request, 'recipes/recipe_edit.html', {'form': form, 'recipe': recipe})


@login_required
def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if request.method == 'POST':
        recipe.delete()
        return redirect('recipe_list')
    return render(request, 'recipes/recipe_confirm_delete.html', {'recipe': recipe})


@login_required
def user_profile_view(request):
    try:
        profile = request.user.customuser
    except CustomUser.DoesNotExist:
        # If UserProfile does not exist, create a new one
        profile = CustomUser(user=request.user)
        profile.save()
    return render(request, 'homepage/home_with_profile.html', {'profile': profile})


def logout_view(request):
    logout(request)
    # Redirect to a desired page after logout
    return render(request, 'homepage/home_without_profile.html')


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'registration/profile.html'


class MyRecipesView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'recipes/my_recipes.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        return Recipe.objects.filter(author=self.request.user)
