from django.urls import resolve, reverse

from recipes import views
from recipes.tests.test_recipe_base import RecipeTestBase


class RecipeSearchViewTest(RecipeTestBase):
    """Testes das views do app `recipes`.

    Cada método abaixo verifica um comportamento específico das views:
    - mapeamento de URL para função de view;
    - status HTTP retornado pela view;
    - template carregado pela view;
    - conteúdo e contexto da resposta.
    """

    # Verifica que a URL nomeada `recipes:search` resolve para `views.search`.
    def test_recipe_search_uses_correct_view_function(self):
        view = resolve(reverse("recipes:search"))
        self.assertIs(view.func, views.search)

    # Garante que a view `search` carrega o template correto quando recebe um termo de busca.
    def test_recipe_search_loads_correct_template(self):
        url = reverse("recipes:search") + "?q=teste"
        response = self.client.get(url)
        self.assertTemplateUsed(response, "recipes/pages/search.html")

    # Verifica que a view retorna 404 quando nenhum termo de busca é fornecido na query.
    def test_recipe_search_raises_404_if_no_query_provided(self):
        url = reverse("recipes:search")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    # Verifica que o termo de busca aparece no título da página e está devidamente escapado
    # (protegido contra XSS) quando contém caracteres especiais como < e >.
    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        url = reverse("recipes:search") + "?q=<teste>"
        response = self.client.get(url)
        content = response.content.decode("utf-8")

        self.assertIn("Search for &quot;&lt;teste&gt;&quot; |  ", content)

    def test_recipe_search_can_find_recipes_by_title(self):
        title_1 = "This is recipe one"
        title_2 = "This is recipe two"

        recipe_1 = self.make_recipe(
            title=title_1, slug="one", author_data={"username": "one"}
        )
        recipe_2 = self.make_recipe(
            title=title_2, slug="two", author_data={"username": "two"}
        )
        url = reverse("recipes:search")
        response1 = self.client.get(f"{url}?q={title_1}")
        response2 = self.client.get(f"{url}?q={title_2}")
        response_both = self.client.get(f"{url}?q=this")

        self.assertIn(recipe_1, response1.context["recipes"])
        self.assertNotIn(recipe_2, response1.context["recipes"])

        self.assertIn(recipe_2, response2.context["recipes"])
        self.assertNotIn(recipe_1, response2.context["recipes"])

        self.assertIn(recipe_1, response_both.context["recipes"])
        self.assertIn(recipe_2, response_both.context["recipes"])
