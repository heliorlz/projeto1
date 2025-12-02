from django.urls import resolve, reverse

from recipes import views
from recipes.tests.test_recipe_base import RecipeTestBase


class RecipeDetailViewTest(RecipeTestBase):
    """Testes das views do app `recipes`.

    Cada método abaixo verifica um comportamento específico das views:
    - mapeamento de URL para função de view;
    - status HTTP retornado pela view;
    - template carregado pela view;
    - conteúdo e contexto da resposta.
    """

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

    # Cria uma receita publicada e verifica se ela aparece corretamente
    # no template de detalhe com o título e conteúdo esperados.
    def test_recipe_detail_template_loads_the_correct_recipe(self):
        needed_title = "This is a detail page - It loads a recipe"
        recipe = self.make_recipe(title=needed_title)
        response = self.client.get(reverse("recipes:recipe", kwargs={"id": recipe.id}))
        content = response.content.decode("utf-8")

        # Verifica se o título da receita aparece no HTML renderizado
        self.assertIn(needed_title, content)

    # Cria uma receita não publicada e verifica se a view retorna 404,
    # garantindo que receitas privadas não podem ser acessadas via detalhe.
    def test_recipe_detail_template_do_not_load_recipe_not_published(self):
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(reverse("recipes:recipe", kwargs={"id": recipe.id}))
        self.assertEqual(response.status_code, 404)
