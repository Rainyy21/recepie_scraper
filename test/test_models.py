from recepie_scraper.models import Ingredient, Recipe, Step


def test_recipe_persists_with_children(session_factory):
    with session_factory() as session:
        recipe = Recipe(
            url="https://example.com/pancakes",
            title="Pancakes",
            author="Anon",
            servings="4",
            total_time=20,
            image_url=None,
            source_site="example.com",
        )
        recipe.ingredients = [
            Ingredient(text="flour", position=0),
            Ingredient(text="milk", position=1),
        ]
        recipe.steps = [Step(text="mix", position=0), Step(text="cook", position=1)]
        session.add(recipe)
        session.commit()

        loaded = session.query(Recipe).filter_by(url=recipe.url).one()
        assert loaded.title == "Pancakes"
        assert [i.text for i in loaded.ingredients] == ["flour", "milk"]
        assert [s.text for s in loaded.steps] == ["mix", "cook"]
        assert loaded.scraped_at is not None


def test_cascade_delete_removes_children(session_factory):
    with session_factory() as session:
        recipe = Recipe(url="https://example.com/x", title="X")
        recipe.ingredients = [Ingredient(text="salt", position=0)]
        recipe.steps = [Step(text="taste", position=0)]
        session.add(recipe)
        session.commit()

        session.delete(recipe)
        session.commit()

        assert session.query(Ingredient).count() == 0
        assert session.query(Step).count() == 0
