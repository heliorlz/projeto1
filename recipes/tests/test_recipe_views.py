from django.urls import resolve, reverse

from recipes import views
from recipes.tests.test_recipe_base import RecipeTestBase


class RecipeViewsTest(RecipeTestBase):
    """Testes das views do app `recipes`.

    Cada método abaixo verifica um comportamento específico das views:
    - mapeamento de URL para função de view;
    - status HTTP retornado pela view;
    - template carregado pela view;
    - conteúdo e contexto da resposta.
    """

    # Verifica que a URL nomeada `recipes:home` resolve para a função `views.home`.
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse("recipes:home"))
        self.assertIs(view.func, views.home)

    # Garante que a view `home` responde com status HTTP 200 (OK).
    def test_recipe_home_view_returns_status_code_200_ok(self):
        url = reverse("recipes:home")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    # Verifica se a view `home` renderiza o template correto.
    def test_recipe_home_view_loads_correct_template(self):
        url = reverse("recipes:home")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "recipes/pages/home.html")

    # Quando não há receitas publicadas, o template deve conter uma mensagem informando isso.
    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes_published(self):
        url = reverse("recipes:home")
        response = self.client.get(url)
        self.assertIn("<h1>No recipes found!</h1>", str(response.content))

    # Cria uma receita publicada e checa se ela aparece no template da home
    # e se o contexto `recipes` contém exatamente a receita criada.
    def test_recipe_home_template_loads_recipes(self):
        self.make_recipe()
        url = reverse("recipes:home")
        response = self.client.get(url)
        content = response.content.decode("utf-8")
        response_context_recipes = response.context["recipes"]

        # Checar se a receita criada está no conteúdo e contexto
        self.assertIn("Recipe Title", content)
        self.assertEqual(len(response_context_recipes), 1)
        ...

    def test_recipe_home_template_do_not_load_recipes_not_published(self):
        """Testa se receitas não publicadas não aparecem na home."""
        self.make_recipe(is_published=False)
        url = reverse("recipes:home")
        response = self.client.get(url)
        content = response.content.decode("utf-8")

        self.assertIn("<h1>No recipes found!</h1>", content)
        ...

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

    def test_recipe_category_template_loads_recipes(self):
        needed_title = "This is a category test"
        self.make_recipe(title=needed_title, category_data={"name": "Category Test"})
        url = reverse("recipes:category", kwargs={"category_id": 1})
        response = self.client.get(url)
        content = response.content.decode("utf-8")

        # Checar se a category criada está no conteúdo e contexto
        self.assertIn(needed_title, content)
        ...

    def test_recipe_category_template_do_not_load_recipes_not_published(self):
        """Testa se receitas não publicadas não aparecem na home."""
        recipe = self.make_recipe(is_published=False)
        url = reverse("recipes:recipe", kwargs={"id": recipe.category.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        ...

    # Verifica que a URL nomeada `recipes:recipe` resolve para `views.recipe`.
    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse("recipes:recipe", kwargs={"id": 1}))
        self.assertIs(view.func, views.recipe)

    # Quando a receita não existe ou não está publicada, a view de detalhe deve retornar 404.
    def test_recipe_detail_view_returns_status_code_404_if_no_recipies_published(
        self,
    ):
        url = reverse("recipes:recipe", kwargs={"id": 1000})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_loads_the_correct_recipe(self):
        needed_title = "This is a detail page - It loads a recipe"
        recipe = self.make_recipe(title=needed_title)
        response = self.client.get(reverse("recipes:recipe", kwargs={"id": recipe.id}))
        content = response.content.decode("utf-8")

        # Checar se a detail recipe criada está no conteúdo e contexto
        self.assertIn(needed_title, content)

    def test_recipe_detail_template_do_not_load_recipe_not_published(self):
        """Testa se receita não publicada não aparece na detalhe."""
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(reverse("recipes:recipe", kwargs={"id": recipe.id}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_uses_correct_view_function(self):
        view = resolve(reverse("recipes:search"))
        self.assertIs(view.func, views.search)

    def test_recipe_search_loads_correct_template(self):
        url = reverse("recipes:search")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "recipes/pages/search.html")
