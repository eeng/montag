def find_by(predicate, iterable):
    """Returns the first element of iterable that matches the predicate. Throws otherwise."""
    return next(item for item in iterable if predicate(item))
