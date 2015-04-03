import copy

from rambutan3 import RArgs
from rambutan3.types.matcher.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.types.matcher.dict.RDictEnum import RDictEnum
from rambutan3.types.matcher.dict.RDictMatcher import RDictMatcher


class RDictWhereMatcher(RDictMatcher):

    def __init__(self, dict_enum: RDictEnum, matcher_dict: dict, *, is_exact: bool):
        super().__init__(dict_enum)

        for key, value_matcher in matcher_dict.items():
            RArgs.check_is_instance(value_matcher, RAbstractTypeMatcher, "value_matcher for key '{}'", key)

        RArgs.check_is_instance(is_exact, bool, "is_exact")
        self.__matcher_dict = matcher_dict
        self.__is_exact = is_exact

    # @override
    def matches(self, d: dict) -> bool:
        if not super().matches(d):
            return False

        dict_copy = copy.deepcopy(d)
        """:type: dict"""

        for key, value_matcher in self.__matcher_dict.items():
            value = dict_copy.get(key)
            if not value_matcher.matches(value):
                return False
            del dict_copy[key]

        if self.__is_exact and dict_copy:
            return False
        return True

    # @override
    def _str(self):
        where_clause = "exactly" if self.__is_exact else "at least"
        x = "{} where {} {}".format(super()._str(), where_clause, self.__matcher_dict)
        return x
