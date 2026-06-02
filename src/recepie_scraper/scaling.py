from ingredient_parser import parse_ingredient

def scale_ingredient(ingredient_text: str, factor: float) -> str:
    """
    Parses an ingredient string, multiplies the quantity by factor,
    and returns a formatted string.
    """
    parsed = parse_ingredient(ingredient_text)

    parts = []
    has_quantity = False

    for amount in parsed.amount:
        if amount.quantity:
            try:
                new_qty = float(amount.quantity) * factor
                qty_str = f"{new_qty:g}"
                unit_str = str(amount.unit) if amount.unit else ""
                scaled_text = f"{qty_str} {unit_str}".strip()
                parts.append((amount.starting_index, scaled_text))
                has_quantity = True
            except (ValueError, TypeError):
                parts.append((amount.starting_index, amount.text))
        else:
            parts.append((amount.starting_index, amount.text))

    if not has_quantity:
        return ingredient_text

    if parsed.name:
        for name_item in parsed.name:
            parts.append((name_item.starting_index, name_item.text))

    if parsed.size:
        parts.append((parsed.size.starting_index, parsed.size.text))

    if parsed.preparation:
        parts.append((parsed.preparation.starting_index, parsed.preparation.text))

    if parsed.comment:
        parts.append((parsed.comment.starting_index, parsed.comment.text))

    if parsed.purpose:
        parts.append((parsed.purpose.starting_index, parsed.purpose.text))

    parts.sort(key=lambda x: x[0])
    return " ".join(p[1] for p in parts)
