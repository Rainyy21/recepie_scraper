from unittest.mock import MagicMock

from typer.testing import CliRunner

from recepie_scraper import main
from recepie_scraper.main import app
from recepie_scraper.models import Recipe

runner = CliRunner()


def test_init_command(session_factory):
    result = runner.invoke(app, ["init"])
    assert result.exit_code == 0
    assert "DB initialized" in result.stdout


def test_add_command_invokes_scraper(session_factory, monkeypatch):
    fake_recipe = MagicMock(title="Fake Title")
    monkeypatch.setattr(main, "scrape_and_save", lambda url: fake_recipe)

    result = runner.invoke(app, ["add", "https://example.com/r"])

    assert result.exit_code == 0
    assert "Fake Title" in result.stdout


def test_list_command_renders_saved_recipes(session_factory):
    with session_factory() as session:
        session.add(Recipe(url="https://example.com/a", title="Alpha", source_site="example.com"))
        session.commit()

    result = runner.invoke(app, ["list"])

    assert result.exit_code == 0
    assert "Alpha" in result.stdout
