from recepie_scraper.scaling import scale_ingredient

def test_scale_ingredient_integer():
    assert scale_ingredient("2 cups flour", 2) == "4 cup flour"

def test_scale_ingredient_float():
    assert scale_ingredient("1 cup sugar", 1.5) == "1.5 cup sugar"

def test_scale_ingredient_no_unit():
    assert scale_ingredient("2 eggs", 3) == "6 eggs"

def test_scale_ingredient_no_quantity():
    assert scale_ingredient("salt and pepper to taste", 2) == "salt and pepper to taste"

def test_scale_ingredient_fraction():
    assert scale_ingredient("1/2 cup butter", 2) == "1 cup butter"

def test_scale_ingredient_complex():
    assert scale_ingredient("2 cups chopped walnuts, for decoration", 2) == "4 cup chopped walnuts for decoration"
