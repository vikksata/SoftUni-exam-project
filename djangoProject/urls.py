from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from recipes.views import register, user_profile_view, logout_view
from homepage.views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('recipes.urls')),  # Include recipes app URLs
    path('accounts/', include('django.contrib.auth.urls')),  # Include Django's default authentication URLs
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/profile/', user_profile_view, name='profile'),
    path('', HomeView.as_view(), name='home'),
    path('logout/', logout_view, name='logout'),
]
