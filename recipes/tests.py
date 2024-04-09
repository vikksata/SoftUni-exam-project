from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import CustomUser, RecipeCategory, Recipe, Comment, Favorite


class CustomUserModelTest(TestCase):
    def test_create_user(self):
        user = CustomUser.objects.create_user(username='testuser', password='12345')
        self.assertEqual(user.username, 'testuser')

    def test_create_superuser(self):
        user = CustomUser.objects.create_superuser(username='testadmin', password='12345')
        self.assertEqual(user.is_superuser, True)


class RecipeCategoryModelTest(TestCase):
    def setUp(self):
        self.category = RecipeCategory.objects.create(category='starter', description='Appetizers')

    def test_category_creation(self):
        self.assertEqual(self.category.category, 'starter')


class RecipeModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='12345')
        self.category = RecipeCategory.objects.create(category='starter', description='Appetizers')
        self.recipe = Recipe.objects.create(title='Test Recipe', description='Delicious', author=self.user, ingredients='Ingredients', instructions='Instructions')

    def test_recipe_creation(self):
        self.assertEqual(self.recipe.title, 'Test Recipe')


class CommentModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='12345')
        self.recipe = Recipe.objects.create(title='Test Recipe', description='Delicious', author=self.user, ingredients='Ingredients', instructions='Instructions')
        self.comment = Comment.objects.create(recipe=self.recipe, author=self.user, content='Great recipe!')

    def test_comment_creation(self):
        self.assertEqual(self.comment.content, 'Great recipe!')


class FavoriteModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='12345')
        self.recipe = Recipe.objects.create(title='Test Recipe', description='Delicious', author=self.user, ingredients='Ingredients', instructions='Instructions')
        self.favorite = Favorite.objects.create(recipe=self.recipe, user=self.user)

    def test_favorite_creation(self):
        self.assertEqual(self.favorite.user, self.user)


class RecipeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='testuser', password='12345')
        self.category = RecipeCategory.objects.create(category='starter', description='Appetizers')
        self.recipe = Recipe.objects.create(title='Test Recipe', description='Delicious', author=self.user, ingredients='Ingredients', instructions='Instructions')

    def test_edit_recipe_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('edit_recipe', args=[str(self.recipe.id)]))
        self.assertEqual(response.status_code, 200)

    def test_delete_recipe_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('delete_recipe', args=[str(self.recipe.id)]))
        self.assertEqual(response.status_code, 200)


class EditProfileViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='testuser', password='12345')

    def test_edit_profile_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('edit_profile'))
        self.assertEqual(response.status_code, 200)


class AddCommentViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='testuser', password='12345')
        self.recipe = Recipe.objects.create(title='Test Recipe', description='Delicious', author=self.user, ingredients='Ingredients', instructions='Instructions')

    def test_add_comment_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('add_comment', args=[str(self.recipe.id)]))
        self.assertEqual(response.status_code, 200)


class ViewRecipeCommentsViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='testuser', password='12345')
        self.recipe = Recipe.objects.create(title='Test Recipe', description='Delicious', author=self.user, ingredients='Ingredients', instructions='Instructions')

    def test_view_recipe_comments_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('view_recipe_comments', args=[str(self.recipe.id)]))
        self.assertEqual(response.status_code, 200)
