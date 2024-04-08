from django.urls import path
from . import views
from .views import MyRecipesView, ProfileView

urlpatterns = [
    path('accounts/profile/', views.recipe_list, name='recipe_list'),
    path('recipe/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('recipe/add/', views.add_recipe, name='add_recipe'),
    path('recipe/<int:recipe_id>/edit/', views.edit_recipe, name='edit_recipe'),
    path('recipe/<int:recipe_id>/delete/', views.delete_recipe, name='delete_recipe'),
    path('my_recipes/', MyRecipesView.as_view(), name='my_recipes'),
    path('my_profile/', ProfileView.as_view(), name='my_profile'),
]
