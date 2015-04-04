from rambutan3.type.matcher.RAbstractTypeMatcher import RAbstractTypeMatcher


RAnyValueOfMatcher = None
class RAnyValueOfMatcher(RAbstractTypeMatcher):

    def __init__(self, *value_tuple):
        super().__init__()
        if not value_tuple:
            raise ValueError("Argument '*value_tuple' is empty")
        self.__value_frozenset = frozenset(value_tuple)

    # @override
    def matches(self, value) -> bool:
        x = value in self.__value_frozenset
        return x

    # @override
    def __eq__(self, other: RAnyValueOfMatcher) -> bool:
        x = isinstance(other, RAnyValueOfMatcher)
        return x

    # @override
    def __str__(self):
        x = "any value of {}".format(self.__value_frozenset)
        return x
