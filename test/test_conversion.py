from recepie_scraper.unit_conversion import convert_unit

def test_convert_cups_to_metric():
    # 2 cups should convert to ml
    assert convert_unit(2, "cups", "metric") == "473.176 ml"

def test_convert_grams_to_imperial():
    # 100 grams should convert to oz
    assert convert_unit(100, "grams", "imperial") == "3.5274 oz"

def test_convert_lb_to_metric():
    # 1 lb should convert to kg
    assert convert_unit(1, "lb", "metric") == "0.453592 kg"

def test_convert_ml_to_imperial():
    # 250 ml should convert to cups (abbreviated to cp by pint)
    assert convert_unit(250, "ml", "imperial") == "1.05669 cp"

def test_convert_tsp_to_metric():
    # 3 tsp should convert to ml
    assert convert_unit(3, "tsp", "metric") == "14.7868 ml"

def test_convert_unmapped_unit():
    # 2 liters should remain 2 liters
    assert convert_unit(2, "liters", "metric") == "2 liters"
