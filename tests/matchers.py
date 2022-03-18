class Matcher:
    def __eq__(self, other):
        raise NotImplementedError("subclasses should provide an __eq__ method")

    def __ne__(self, other):
        return not self.__eq__(other)


class instance_of(Matcher):
    """Matches any object which is an instance of `expected_type`."""

    def __init__(self, expected_type):
        self.expected_type = expected_type

    def __eq__(self, other):
        return isinstance(other, self.expected_type)

    def __repr__(self):
        return f"<instance of {self.expected_type}>"


class has_attrs(Matcher):
    """Matches an object with the specified attributes."""

    def __init__(self, **attrs):
        self.expected_attrs = attrs

    def __eq__(self, other):
        return all(
            getattr(other, attr) == value for attr, value in self.expected_attrs.items()
        )

    def __repr__(self):
        return f"<object with attrs {self.expected_attrs}>"


class has_entries(Matcher):
    """Matches a dict with the specified items."""

    def __init__(self, **entries):
        self.expected_entries = entries

    def __eq__(self, other):
        return all(
            other[attr] == value for attr, value in self.expected_entries.items()
        )

    def __repr__(self):
        return f"<dict with entries {self.expected_entries}>"
