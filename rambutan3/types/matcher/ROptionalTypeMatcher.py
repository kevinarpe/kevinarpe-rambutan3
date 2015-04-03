from rambutan3.types.matcher.RAbstractTypeMatcher import RAbstractTypeMatcher


class ROptionalTypeMatcher(RAbstractTypeMatcher):

    def __init__(self):
        super().__init__()

    # @override
    def matches(self, value) -> bool:
        x = value is None
        return x

    def contains(self, matcher) -> bool:
        x = isinstance(matcher, type(self))
        return x

    # @override
    def _str(self):
        return "None"
