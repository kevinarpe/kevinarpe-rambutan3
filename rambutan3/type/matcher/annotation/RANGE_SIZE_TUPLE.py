from rambutan3.type.matcher.seq.RRangeSizeSequenceMatcher import RRangeSizeSequenceMatcher
from rambutan3.type.matcher.seq.RSequenceEnum import RSequenceEnum


def RANGE_SIZE_TUPLE(*, min_size: int=-1, max_size: int=-1) -> RRangeSizeSequenceMatcher:
    x = RRangeSizeSequenceMatcher(RSequenceEnum.TUPLE, min_size=min_size, max_size=max_size)
    return x