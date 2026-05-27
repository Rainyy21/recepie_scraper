import typer
from rich.table import Table
from rich.console import Console
from .db import init_db, SessionLocal
from .models import Recipe
from .scraper import scrape_and_save

app = typer.Typer()
console = Console()


@app.command()
def init():
    """create the database"""
    init_db()
    console.print("[green]DB initialized[/green]")


@app.command()
def add(url: str):
    """Scrape a url and save it"""
    recipe = scrape_and_save(url)
    console.print(f"[green]Saved:[/green] {recipe.title}")


@app.command()
def list():
    """list all saved recipes"""
    with SessionLocal() as session:
        recipes = session.query(Recipe).all()
        table = Table(title="Recipes")
        table.add_column("ID")
        table.add_column("Title")
        table.add_column("Site")
        table.add_column("URL")
        for r in recipes:
            table.add_row(str(r.id), r.title, r.source_site or "", r.url)
        console.print(table)


@app.command()
def show(recipe_id: int):
    """Show a recipe with its ingredients and steps"""
    with SessionLocal() as session:
        recipe = session.get(Recipe, recipe_id)
        if recipe is None:
            console.print(f"[red]No recipe with id {recipe_id}[/red]")
            raise typer.Exit(1)
        console.print(f"[bold]{recipe.title}[/bold]  ({recipe.url})")
        console.print("\n[bold]Ingredients[/bold]")
        for ing in sorted(recipe.ingredients, key=lambda i: i.position):
            console.print(f"  - {ing.text}")
        console.print("\n[bold]Steps[/bold]")
        for st in sorted(recipe.steps, key=lambda s: s.position):
            console.print(f"  {st.position}. {st.text}")


if __name__ == "__main__":
    app()
