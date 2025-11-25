from django.core.exceptions import ValidationError
from parameterized import parameterized

from .test_recipe_base import RecipeTestBase


class RecipeCategoryModelTest(RecipeTestBase):
    def setUp(self):
        self.category = self.make_category(name="Category Test")
        return super().setUp()

    def test_recipe_category_model_string_representation_is_name_field(self):
        needed_name = "Category Test"
        self.category.name = needed_name
        self.category.full_clean()
        self.category.save()
        self.assertEqual(
            str(self.category),
            needed_name,
            msg="Category model string representation is not the name field",
        )

    @parameterized.expand(
        [
            ("name", 65),
        ]
    )
    def test_recipe_fields_max_length(self, field, max_length):
        setattr(self.category, field, (max_length + 1) * "A")  # type: ignore[arg-type]
        with self.assertRaises(ValidationError):
            self.category.full_clean()
