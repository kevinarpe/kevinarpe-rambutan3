from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.seq.RRangeSizeSequenceOfMatcher import RRangeSizeSequenceOfMatcher
from rambutan3.check_args.seq.RSequenceEnum import RSequenceEnum


def NON_EMPTY_SEQUENCE_OF(type_matcher: RAbstractTypeMatcher) -> RRangeSizeSequenceOfMatcher:
    x = RRangeSizeSequenceOfMatcher(RSequenceEnum.SEQUENCE, type_matcher, min_size=1)
    return x
