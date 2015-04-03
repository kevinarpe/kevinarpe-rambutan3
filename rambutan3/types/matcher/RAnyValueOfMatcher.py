from rambutan3.types.matcher.RAbstractTypeMatcher import RAbstractTypeMatcher


class RAnyValueOfMatcher(RAbstractTypeMatcher):

    def __init__(self, *value_tuple):
        super().__init__()
        if not value_tuple:
            raise ValueError("Argument list is empty")
        self.__set = set(value_tuple)

    def matches(self, value) -> bool:
        x = value in self.__set
        return x

    def contains(self, matcher) -> bool:
        x = isinstance(matcher, type(self)) and self.__set.issuperset(matcher.__set)
        return x

    def _str(self):
        x = str(self.__set)
        return x
