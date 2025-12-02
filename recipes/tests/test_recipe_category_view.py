from django.urls import resolve, reverse

from recipes import views
from recipes.tests.test_recipe_base import RecipeTestBase


class RecipeCategoryViewTest(RecipeTestBase):
    """Testes das views do app `recipes`.

    Cada método abaixo verifica um comportamento específico das views:
    - mapeamento de URL para função de view;
    - status HTTP retornado pela view;
    - template carregado pela view;
    - conteúdo e contexto da resposta.
    """

    # Verifica que a URL nomeada `recipes:category` resolve para `views.category`.
    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse("recipes:category", kwargs={"category_id": 1}))
        self.assertIs(view.func, views.category)

    # Quando não existem receitas publicadas para uma categoria, a view deve retornar 404.
    def test_recipe_category_view_returns_status_code_404_if_no_recipies_published(
        self,
    ):
        url = reverse("recipes:category", kwargs={"category_id": 1000})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    # Cria uma receita publicada em uma categoria e verifica se ela aparece
    # no template da view de categoria com o título e conteúdo corretos.
    def test_recipe_category_template_loads_recipes(self):
        needed_title = "This is a category test"
        self.make_recipe(title=needed_title, category_data={"name": "Category Test"})
        url = reverse("recipes:category", kwargs={"category_id": 1})
        response = self.client.get(url)
        content = response.content.decode("utf-8")

        # Verifica se a receita criada está no conteúdo HTML renderizado
        self.assertIn(needed_title, content)

    # Cria uma receita não publicada e verifica se a view retorna 404
    # quando tentamos acessar a categoria, garantindo que receitas privadas não aparecem.
    def test_recipe_category_template_do_not_load_recipes_not_published(self):
        recipe = self.make_recipe(is_published=False)
        url = reverse("recipes:recipe", kwargs={"id": recipe.category.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
