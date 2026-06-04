from flask import Flask, render_template, request
from recepie_scraper.db import SessionLocal
from recepie_scraper.models import Recipe
from recepie_scraper.scraper import scrape_and_save

app = Flask(__name__)


@app.route("/")
def index():
    with SessionLocal() as session:
        recipes = session.query(Recipe).all()
        return render_template("index.html", recipes=recipes)


@app.route("/add", methods=["POST"])
def add_recipe():
    url = request.form.get("url")
    if url:
        scrape_and_save(url)
    
    with SessionLocal() as session:
        recipes = session.query(Recipe).all()
        return render_template("_recipe_list.html", recipes=recipes)


@app.route("/delete/<int:recipe_id>", methods=["DELETE"])
def delete_recipe(recipe_id):
    with SessionLocal() as session:
        recipe = session.query(Recipe).get(recipe_id)
        if recipe:
            session.delete(recipe)
            session.commit()
    return "", 200


@app.route("/search")
def search():
    query = request.args.get("q", "")
    with SessionLocal() as session:
        recipes = session.query(Recipe).filter(Recipe.title.contains(query)).all()
        return render_template("_recipe_list.html", recipes=recipes)


@app.route("/recipe/<int:recipe_id>")
def recipe_detail(recipe_id):
    with SessionLocal() as session:
        recipe = session.query(Recipe).get(recipe_id)
        if not recipe:
            return "Recipe not found", 404
        return render_template("recipe.html", recipe=recipe)


if __name__ == "__main__":
    app.run(debug=True)
