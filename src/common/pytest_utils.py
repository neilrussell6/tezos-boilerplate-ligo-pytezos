"""Common PyTest Utils"""


def cached(cache_module, key, f):
    """Return cached value from provided cache module or call provided function and cache."""
    value = cache_module.get(key, None)
    if value is None:
        value = f()
        cache_module.set(key, value)
    return value
