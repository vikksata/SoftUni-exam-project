from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from djangoProject.recipes.views import register


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('djangoProject.recipes.urls')),  # Include recipes app URLs
    path('accounts/', include('django.contrib.auth.urls')),  # Include Django's default authentication URLs
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
]
