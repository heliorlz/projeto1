from django.core.exceptions import ValidationError
from parameterized import parameterized

from recipes.models import Recipe

from .test_recipe_base import RecipeTestBase


class RecipeModelTest(RecipeTestBase):
    def setUp(self):
        self.recipe = self.make_recipe()
        return super().setUp()

    def make_recipe_no_defaults(self):
        recipe = Recipe(
            category=self.make_category(name="Test Category"),
            author=self.make_author(username="testuser2"),
            title="Recipe Title",
            description="Recipe Description",
            slug="recipe-slug-test",
            preparation_time=10,
            preparation_time_unit="Minutes",
            servings=2,
            servings_unit="People",
            preparation_steps="Recipe Preparation Steps",
        )
        recipe.full_clean()
        recipe.save()
        return recipe

    @parameterized.expand(
        [
            ("title", 65),
            ("description", 165),
            ("preparation_time_unit", 65),
            ("servings_unit", 65),
        ]
    )
    def test_recipe_fields_max_length(self, field, max_length):
        setattr(self.recipe, field, (max_length + 1) * "A")  # type: ignore[arg-type]
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    def test_recipe_preparation_steps_is_html_is_false_by_default(self):
        recipe = self.make_recipe_no_defaults()
        self.assertFalse(
            recipe.preparation_steps_is_html,
            msg="Recipe preparation_steps_is_html is not false",
        )

    def test_recipe_is_published_is_false_by_default(self):
        recipe = self.make_recipe_no_defaults()
        self.assertFalse(recipe.is_published, msg="Recipe is_published is not false")

    def test_recipe_string_representation(self):
        needed_title = "Testing String Representation"
        self.recipe.title = "Testing String Representation"
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual(
            str(self.recipe),
            needed_title,
            msg=f"Recipe string representation must be '{needed_title}' but received '{self.recipe!s}'",
        )
