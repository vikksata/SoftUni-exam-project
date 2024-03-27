from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('djangoProject.recipes.urls')),  # Include recipes app URLs
]
