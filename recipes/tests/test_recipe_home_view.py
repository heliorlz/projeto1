from django.urls import resolve, reverse

from recipes import views
from recipes.tests.test_recipe_base import RecipeTestBase


class RecipeHomeViewTest(RecipeTestBase):
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

    # Cria uma receita publicada e verifica se ela aparece no template da home
    # e se o contexto `recipes` contém exatamente a receita criada.
    def test_recipe_home_template_loads_recipes(self):
        self.make_recipe()
        url = reverse("recipes:home")
        response = self.client.get(url)
        content = response.content.decode("utf-8")
        response_context_recipes = response.context["recipes"]

        # Verifica se a receita aparece no HTML e se há exatamente 1 receita no contexto
        self.assertIn("Recipe Title", content)
        self.assertEqual(len(response_context_recipes), 1)

    # Cria uma receita não publicada e verifica se ela não aparece na home,
    # confirmando que apenas receitas publicadas são exibidas.
    def test_recipe_home_template_do_not_load_recipes_not_published(self):
        self.make_recipe(is_published=False)
        url = reverse("recipes:home")
        response = self.client.get(url)
        content = response.content.decode("utf-8")

        # Verifica que a mensagem "No recipes found!" aparece quando não há receitas publicadas
        self.assertIn("<h1>No recipes found!</h1>", content)
