from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.base.traverse.RTypeMatcherError import RTypeMatcherError
from rambutan3.check_args.dict.RDictEnum import RDictEnum
from rambutan3.check_args.dict.RDictOfMatcher import RDictOfMatcher
from rambutan3.check_args.dict.RRangeSizeDictMatcher import RRangeSizeDictMatcher


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
    def matches(self, d: dict, matcher_error: RTypeMatcherError=None) -> bool:
        if not super().matches(d, matcher_error):
            return False

        x = RDictOfMatcher.core_matches(d, matcher_error,
                                        key_matcher=self.__key_matcher,
                                        value_matcher=self.__value_matcher)
        return x

    # @override
    def __eq__(self, other) -> bool:
        if not isinstance(other, RRangeSizeDictOfMatcher):
            return False
        if not super().__eq__(other):
            return False
        x = (self.__key_matcher == other.__key_matcher and self.__value_matcher == other.__value_matcher)
        return x

    # @override
    def __hash__(self) -> int:
        # Ref: http://stackoverflow.com/questions/29435556/how-to-combine-hash-codes-in-in-python3
        super_hash = super().__hash__()
        self_hash = hash((self.__key_matcher, self.__value_matcher))
        x = super_hash ^ self_hash
        return x

    # @override
    def __str__(self):
        x = RDictOfMatcher.core__str__(super().__str__(),
                                       key_matcher=self.__key_matcher,
                                       value_matcher=self.__value_matcher)
        return x
