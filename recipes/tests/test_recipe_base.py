from django.test import TestCase

from recipes.models import Category, Recipe, User


class RecipeTestBase(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def make_category(self, name="Category Test") -> Category:
        return Category.objects.create(name=name)

    def make_author(
        self,
        username="testuser",
        password="password123",  # noqa S105
        first_name="Test",
        last_name="User",
        email="username@email.com",
    ) -> User:
        return User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
        )

    def make_recipe(
        self,
        category_data=None,
        author_data=None,
        title="Recipe Title",
        description="Recipe Description",
        slug="recipe-slug",
        preparation_time=10,
        preparation_time_unit="Minutes",
        servings=2,
        servings_unit="People",
        preparation_steps="Recipe Preparation Steps",
        preparation_steps_is_html=False,  # noqa: FBT002
        is_published=True,  # noqa: FBT002
    ) -> Recipe:
        if category_data is None:
            category_data = {}
        if author_data is None:
            author_data = {}

        return Recipe.objects.create(
            category=self.make_category(**category_data),
            author=self.make_author(**author_data),
            title=title,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            servings_unit=servings_unit,
            preparation_steps=preparation_steps,
            preparation_steps_is_html=preparation_steps_is_html,
            is_published=is_published,
        )
