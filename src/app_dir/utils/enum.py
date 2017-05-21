
def enum(make_choices=False, **enums):
    """
    function for creating enum iterable classes

    Example:

    >> SOME_ENUM = enum(VAL0=0, VAL1=1, VAL2=2)

    >> SOME_ENUM.VALUE0
    >> 0

    >> 1 in SOME_ENUM
    >> True

    >> 5 in SOME_ENUM
    >> False
    """
    def values(self):
        return enums.values()

    def keys(self):
        return enums.keys()

    cls = type('EnumClass', (), {'keys': keys, 'values': values})

    def __iter__(self):
        for _attr, val in enums.items():
            yield val

    def __add__(self, other):
        return self.values() + other

    cls.__iter__ = __iter__
    cls.__radd__ = cls.__add__ = __add__
    enum_object = cls()

    for attr, value in enums.items():
        setattr(enum_object, attr, value)

    if make_choices:
        enum_object.CHOICES = [(x, x) for x in enum_object]

    return enum_object