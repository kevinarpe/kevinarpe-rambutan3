from rambutan3.types.matcher.RAbstractTypeMatcher import RAbstractTypeMatcher


class RAnyTypeMatcher(RAbstractTypeMatcher):

    def __init__(self):
        super().__init__()

    def matches(self, value) -> bool:
        x = value is not None
        return x

    # def contains(self, matcher) -> bool:
    #     x = isinstance(matcher, type(self))
    #     return x
