from django.contrib import admin
from .models import CustomUser, RecipeCategory, Recipe, Comment, Favorite


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type', 'age', 'is_staff')
    list_filter = ('user_type', 'is_staff')
    search_fields = ('username', 'email')
    ordering = ('username',)


class RecipeCategoryAdmin(admin.ModelAdmin):
    list_display = ('category',)
    search_fields = ('category',)
    ordering = ('category',)
    list_filter = ('category',)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')
    list_filter = ('categories', 'author')
    search_fields = ('title', 'author__username')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'author', 'created_at')
    list_filter = ('recipe', 'author')
    search_fields = ('recipe__title', 'author__username')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user')
    list_filter = ('recipe', 'user')
    search_fields = ('recipe__title', 'user__username')
    ordering = ('user',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(RecipeCategory, RecipeCategoryAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Favorite, FavoriteAdmin)
