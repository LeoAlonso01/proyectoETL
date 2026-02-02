def flatten_dict(d: dict, parent_key: str = "", sep: str = "_") -> dict:
    """
    Flatten nested dict keys into a single level dict.
    Example: {"a":{"b":1}} -> {"a_b":1}
    """
    items = {}
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.update(flatten_dict(v, new_key, sep=sep))
        else:
            items[new_key] = v
    return items
