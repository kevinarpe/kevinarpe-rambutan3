from rambutan3.types.matcher.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.types.matcher.dict.RDictOfMatcher import RDictOfMatcher
from rambutan3.types.matcher.dict.RRangeSizeDictMatcher import RRangeSizeDictMatcher
from rambutan3.types.matcher.dict.RDictEnum import RDictEnum


class RRangeSizeDictOfMatcher(RRangeSizeDictMatcher):

    def __init__(self,
                 dict_enum: RDictEnum,
                 *,
                 key_matcher: RAbstractTypeMatcher=None,
                 value_matcher: RAbstractTypeMatcher=None,
                 min_size: int=-1,
                 max_size: int=-1):
        super().__init__(dict_enum, min_size=min_size, max_size=max_size)
        RDictOfMatcher.check_init_args(key_matcher=key_matcher, value_matcher=value_matcher)
        self.__key_matcher = key_matcher
        self.__value_matcher = value_matcher

    # @override
    def matches(self, d) -> bool:
        if not super().matches(d):
            return False
        x = RDictOfMatcher.core_matches(d, key_matcher=self.__key_matcher, value_matcher=self.__value_matcher)
        return x

    # @override
    def _str(self):
        x = RDictOfMatcher.core_str(super()._str(), key_matcher=self.__key_matcher, value_matcher=self.__value_matcher)
        return x
