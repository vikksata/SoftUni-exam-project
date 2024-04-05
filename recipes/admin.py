from django.contrib import admin
from .models import Recipe


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    list_filter = ('author', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'ingredients', 'instructions')
    ordering = ('-created_at',)


admin.site.register(Recipe, RecipeAdmin)
