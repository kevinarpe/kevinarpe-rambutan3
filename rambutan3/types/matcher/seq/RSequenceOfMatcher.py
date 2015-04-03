from rambutan3 import RArgs
from rambutan3.types.matcher.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.types.matcher.seq.RSequenceEnum import RSequenceEnum
from rambutan3.types.matcher.seq.RSequenceMatcher import RSequenceMatcher


class RSequenceOfMatcher(RSequenceMatcher):

    def __init__(self, sequence_enum: RSequenceEnum, value_matcher: RAbstractTypeMatcher):
        super().__init__(sequence_enum)
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


# class RSequenceOfMatcher(RSequenceMatcher, RCollectionOfMatcher):
#
#     def __init__(self, sequence_enum: RSequenceEnum, value_matcher: RAbstractTypeMatcher):
#         super(RSequenceMatcher, self).__init__(sequence_enum)
#         super(RCollectionOfMatcher, self).__init__(value_matcher)
#
#     # @override
#     def matches(self, seq) -> bool:
#         if not super(RSequenceMatcher, self).matches(seq):
#             return False
#         x = super(RCollectionOfMatcher, self).matches(seq)
#         return x
#
#     # @override
#     def _str(self):
#         x = "{} of [{}]".format(super()._str(), str(self.__value_matcher))
#         return x
