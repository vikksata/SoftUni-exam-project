from django.urls import path
from . import views
from .views import MyRecipesView, ProfileView, RecipeListView, RecipeDetailView

urlpatterns = [
    path('accounts/profile/', RecipeListView.as_view(), name='recipe_list'),
    path('recipe/<int:pk>/', RecipeDetailView.as_view(), name='recipe_detail'),
    path('recipe/add/', views.add_recipe, name='add_recipe'),
    path('recipe/<int:recipe_id>/edit/', views.edit_recipe, name='edit_recipe'),
    path('recipe/<int:recipe_id>/delete/', views.delete_recipe, name='delete_recipe'),
    path('my_recipes/', MyRecipesView.as_view(), name='my_recipes'),
    path('my_profile/', ProfileView.as_view(), name='my_profile'),
]
