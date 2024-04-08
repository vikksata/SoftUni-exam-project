from django.shortcuts import render
from recipes.models import Recipe


def home_recipe_list(request):
    if request.user.is_authenticated:
        recipes = Recipe.objects.all()
        return render(request, 'homepage/home_with_profile.html', {'recipes': recipes})
    else:
        return render(request, 'homepage/home_without_profile.html',)
