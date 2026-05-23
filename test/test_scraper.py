from unittest.mock import MagicMock

import pytest

from recepie_scraper import scraper
from recepie_scraper.models import Recipe
from recepie_scraper.scraper import safe, scrape_and_save


@pytest.fixture
def fake_scrape(monkeypatch):
    mock = MagicMock()
    mock.title.return_value = "Test Pancakes"
    mock.author.return_value = "Chef Test"
    mock.yields.return_value = "4 servings"
    mock.total_time.return_value = 30
    mock.image.return_value = "https://example.com/img.jpg"
    mock.host.return_value = "example.com"
    mock.ingredients.return_value = ["200g flour", "300ml milk", "2 eggs"]
    mock.instructions.return_value = "Mix everything.\nCook on a pan.\n\nServe hot."

    monkeypatch.setattr(scraper, "scrape_me", lambda url: mock)
    return mock


def test_scrape_and_save_persists_recipe(session_factory, fake_scrape):
    url = "https://example.com/pancakes"
    scrape_and_save(url)

    with session_factory() as session:
        recipe = session.query(Recipe).filter_by(url=url).one()
        assert recipe.title == "Test Pancakes"
        assert recipe.author == "Chef Test"
        assert recipe.total_time == 30
        assert recipe.source_site == "example.com"
        assert [i.text for i in recipe.ingredients] == ["200g flour", "300ml milk", "2 eggs"]
        assert [i.position for i in recipe.ingredients] == [0, 1, 2]
        assert [s.text for s in recipe.steps] == ["Mix everything.", "Cook on a pan.", "Serve hot."]


def test_scrape_and_save_is_idempotent(session_factory, fake_scrape):
    url = "https://example.com/pancakes"
    first = scrape_and_save(url)
    second = scrape_and_save(url)

    assert first.id == second.id
    with session_factory() as session:
        assert session.query(Recipe).count() == 1


def test_scrape_and_save_handles_scraper_errors(session_factory, monkeypatch):
    mock = MagicMock()
    mock.title.return_value = "Broken"
    mock.author.side_effect = RuntimeError("no author")
    mock.yields.side_effect = RuntimeError("no yield")
    mock.total_time.side_effect = RuntimeError("no time")
    mock.image.side_effect = RuntimeError("no image")
    mock.host.side_effect = RuntimeError("no host")
    mock.ingredients.return_value = []
    mock.instructions.return_value = ""
    monkeypatch.setattr(scraper, "scrape_me", lambda url: mock)

    url = "https://example.com/broken"
    scrape_and_save(url)

    with session_factory() as session:
        recipe = session.query(Recipe).filter_by(url=url).one()
        assert recipe.title == "Broken"
        assert recipe.author is None
        assert recipe.servings is None
        assert recipe.total_time is None
        assert recipe.image_url is None
        assert recipe.source_site is None
        assert recipe.ingredients == []
        assert recipe.steps == []


def test_safe_returns_value_on_success():
    assert safe(lambda: "ok") == "ok"


def test_safe_returns_none_on_exception():
    def boom():
        raise ValueError("nope")

    assert safe(boom) is None
