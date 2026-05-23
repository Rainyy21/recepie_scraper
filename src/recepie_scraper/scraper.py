from recipe_scrapers import scrape_me

from .db import SessionLocal
from .models import Ingredient, Recipe, Step


def scrape_and_save(url: str) -> Recipe:
    scraper = scrape_me(url)

    with SessionLocal() as session:
        existing = session.query(Recipe).filter_by(url=url).first()
        if existing:
            return existing

        recipe = Recipe(
            url=url,
            title=scraper.title(),
            author=safe(scraper.author),
            servings=safe(scraper.yields),
            total_time=safe(scraper.total_time),
            image_url=safe(scraper.image),
            source_site=safe(scraper.host),
        )
        recipe.ingredients = [
            Ingredient(text=t, position=i)
            for i, t in enumerate(scraper.ingredients())
        ]
        recipe.steps = [
            Step(text=s.strip(), position=i)
            for i, s in enumerate(scraper.instructions().split("\n"))
            if s.strip()
        ]
        session.add(recipe)
        session.commit()
        session.refresh(recipe)
        return recipe


def safe(fn):
    try:
        return fn()
    except Exception:
        return None
