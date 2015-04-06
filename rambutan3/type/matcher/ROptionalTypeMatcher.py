from rambutan3.type.matcher.RAbstractTypeMatcher import RAbstractTypeMatcher


ROptionalTypeMatcher = None
class ROptionalTypeMatcher(RAbstractTypeMatcher):

    def __init__(self):
        super().__init__()

    # @override
    def matches(self, value) -> bool:
        x = value is None
        return x

    # @override
    def __eq__(self, other: ROptionalTypeMatcher) -> bool:
        x = isinstance(other, ROptionalTypeMatcher)
        return x

    # @override
    def __hash__(self) -> int:
        x = super(object, self).__hash__()
        return x

    # @override
    def __str__(self):
        return "None"
