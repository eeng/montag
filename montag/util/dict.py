def select_keys(d: dict, *keys) -> dict:
    return {k: d[k] for k in keys}
