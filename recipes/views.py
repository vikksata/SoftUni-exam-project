from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, TemplateView, DetailView

from .models import Recipe, CustomUser, Favorite, Comment, RecipeCategory
from .forms import RecipeForm, EditRecipeForm, CustomUserChangeForm, CommentForm
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


class RecipeListView(ListView):
    model = Recipe
    template_name = 'homepage/home_with_profile.html'
    context_object_name = 'recipes'


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipes/recipe_detail.html'
    context_object_name = 'recipe'


@login_required
def add_recipe(request):
    if not request.user.groups.filter(name='Chef').exists():
        return HttpResponseForbidden("You are not allowed to perform this action.")

    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            form.save_m2m()
            return redirect('recipe_list')
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
            return redirect('recipe_detail', pk=recipe_id)
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


@login_required
def add_favourite(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    # Check if the favourite already exists
    existing_favourite = Favorite.objects.filter(user=request.user, recipe=recipe)
    if existing_favourite.exists():
        return HttpResponse("This recipe is already in your favourites.")

    # If the favourite does not exist, create a new one
    favourite = Favorite(user=request.user, recipe=recipe)
    favourite.save()
    return redirect('home')


@login_required
def user_favourites(request, user_id):
    favorites = Favorite.objects.filter(user__id=user_id)
    return render(request, 'recipes/user_favourites.html', {'favorites': favorites})


class FavoritesRecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipes/favorite_recipe_details.html'


@login_required
def delete_favourite(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    # Check if the favourite exists
    favourite = Favorite.objects.filter(user=request.user, recipe=recipe)
    if favourite.exists():
        # If the favourite exists, delete it
        favourite.delete()
        return redirect(reverse('user_favourites', args=[request.user.id]))
    else:
        # If the favourite does not exist, inform the user
        return HttpResponse("This apartment is not in your favourites.")


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('my_profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'registration/edit_profile.html', {'form': form})


@login_required
def add_comment(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.recipe = recipe  # Associate comment with the recipe
            comment.author = request.user  # Set the comment's author to the current user
            comment.save()
            return redirect('recipe_detail', pk=recipe_id)  # Redirect to recipe detail page
    else:
        form = CommentForm()

    return render(request, 'recipes/add_comment.html', {'form': form})


def view_recipe_comments(request, recipe_id):
    recipe_comments = Comment.objects.filter(recipe_id=recipe_id)
    recipe = Recipe.objects.get(id=recipe_id)

    return render(request, 'recipes/view_recipe_comments.html', {'recipe_comments': recipe_comments, 'recipe': recipe})


class StarterRecipesView(View):

    def get(self, request, *args, **kwargs):
        starter_category = RecipeCategory.objects.get(category=RecipeCategory.STARTER)
        recipes = Recipe.objects.filter(categories=starter_category)
        return render(request, 'recipes/recipe_categories.html', {'recipes': recipes})


class MainCourseRecipesView(View):

    def get(self, request, *args, **kwargs):
        main_course_category = RecipeCategory.objects.get(category=RecipeCategory.MAIN_COURSE)
        recipes = Recipe.objects.filter(categories=main_course_category)
        return render(request, 'recipes/recipe_categories.html', {'recipes': recipes})


class DessertRecipesView(View):

    def get(self, request, *args, **kwargs):
        dessert_category = RecipeCategory.objects.get(category=RecipeCategory.DESSERT)
        recipes = Recipe.objects.filter(categories=dessert_category)
        return render(request, 'recipes/recipe_categories.html', {'recipes': recipes})
