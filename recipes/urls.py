from django.urls import path
from . import views
from .views import MyRecipesView, ProfileView, RecipeListView, RecipeDetailView, add_favourite, \
    FavoritesRecipeDetailView, edit_profile, add_comment, view_recipe_comments, StarterRecipesView, \
    MainCourseRecipesView, DessertRecipesView, delete_favourite, UserFavoritesView

urlpatterns = [
    path('accounts/profile/', RecipeListView.as_view(), name='recipe_list'),
    path('recipe/<int:pk>/', RecipeDetailView.as_view(), name='recipe_detail'),
    path('recipe/add/', views.add_recipe, name='add_recipe'),
    path('recipe/<int:recipe_id>/edit/', views.edit_recipe, name='edit_recipe'),
    path('recipe/<int:recipe_id>/delete/', views.delete_recipe, name='delete_recipe'),
    path('my_recipes/', MyRecipesView.as_view(), name='my_recipes'),
    path('my_profile/', ProfileView.as_view(), name='my_profile'),
    path('recipe/<int:recipe_id>/add_favourite/', add_favourite, name='add_favourite'),
    path('user/<int:user_id>/favourites/', UserFavoritesView.as_view(), name='user_favourites'),
    path('favorites/recipe/<int:pk>/', FavoritesRecipeDetailView.as_view(), name='favorite_recipe_details'),
    path('delete_favourite/<int:recipe_id>/', delete_favourite, name='delete_favourite'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('recipes/<int:recipe_id>/add_comment/', add_comment, name='add_comment'),
    path('recipes/<int:recipe_id>/comments/', view_recipe_comments, name='view_recipe_comments'),
    path('accounts/profile/starters', StarterRecipesView.as_view(), name='starters_list'),
    path('accounts/profile/main_courses', MainCourseRecipesView.as_view(), name='main_courses_list'),
    path('accounts/profile/desserts', DessertRecipesView.as_view(), name='desserts_list'),
]
