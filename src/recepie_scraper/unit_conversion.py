from pint import UnitRegistry

ureg = UnitRegistry()


def convert_unit(quantity: float, from_unit: str, to_system: str = "metric") -> str:
    """
    Converts a quantity from one unit to the target system.
    """
    TARGETS = {
        "metric": {
            "cup": "ml",
            "ounce": "grams",
            "pound": "kg",
            "teaspoon": "ml",
            "tablespoon": "ml",
        },
        "imperial": {
            "milliliter": "cup",
            "gram": "oz",
            "kilogram": "lb",
        },
    }

    try:
        q = quantity * ureg(from_unit)
        from_unit_norm = str(ureg(from_unit).units)

        target_unit = TARGETS.get(to_system, {}).get(from_unit_norm)
        if target_unit:
            converted = q.to(target_unit)
            return f"{converted.magnitude:g} {converted.units:~}"
        return f"{quantity:g} {from_unit}"
    except Exception:
        return f"{quantity:g} {from_unit}"
