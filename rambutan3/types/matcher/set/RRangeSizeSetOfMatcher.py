from rambutan3 import RArgs
from rambutan3.types.matcher.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.types.matcher.set.RRangeSizeSetMatcher import RRangeSizeSetMatcher
from rambutan3.types.matcher.set.RSetEnum import RSetEnum


class RRangeSizeSetOfMatcher(RRangeSizeSetMatcher):

    def __init__(self,
                 set_enum: RSetEnum,
                 value_matcher: RAbstractTypeMatcher,
                 *,
                 min_size: int=-1,
                 max_size: int=-1):
        super().__init__(set_enum, min_size=min_size, max_size=max_size)
        RArgs.check_is_instance(value_matcher, RAbstractTypeMatcher, "value_matcher")
        self.__value_matcher = value_matcher

    # @override
    def matches(self, seq) -> bool:
        if not super().matches(seq):
            return False
        x = all(self.__value_matcher.matches(y) for y in seq)
        return x

    # @override
    def _str(self):
        x = "{} of [{}]".format(super()._str(), self.__value_matcher)
        return x
