import pytest
from rambutan3 import RTestUtil
from rambutan3.check_args.RCheckArgsError import RCheckArgsError
from rambutan3.check_args.seq.RRangeSizeSequenceMatcher import RRangeSizeSequenceMatcher
from rambutan3.check_args.seq.RSequenceEnum import RSequenceEnum


def test_ctor():
    pass


def test_check_arg():
    __check_arg(RSequenceEnum.LIST, min_size=1, max_size=3, value=['abc'], is_ok=True)
    __check_arg(RSequenceEnum.LIST, min_size=1, max_size=3, value=('abc',), is_ok=False)
    # Type 'str' is not a seq!
    __check_arg(RSequenceEnum.SEQUENCE, min_size=1, max_size=3, value='abc', is_ok=False)
    __check_arg(RSequenceEnum.SEQUENCE, min_size=1, max_size=3, value=['abc'], is_ok=True)
    __check_arg(RSequenceEnum.SEQUENCE, min_size=7, max_size=8, value=['abc'], is_ok=False)


def __check_arg(seq_enum: RSequenceEnum, min_size: int, max_size: int, value, *, is_ok: bool):
    m = RRangeSizeSequenceMatcher(seq_enum, min_size=min_size, max_size=max_size)
    if is_ok:
        assert value is m.check_arg(value, 'dummy_arg_name')
    else:
        with pytest.raises(RCheckArgsError):
            m.check_arg(value, 'dummy_arg_name')

def test_eq_ne_hash():
    RTestUtil.test_eq_ne_hash(RRangeSizeSequenceMatcher(RSequenceEnum.LIST, min_size=1, max_size=3),
                              'abc',
                              is_equal=False)
    RTestUtil.test_eq_ne_hash(RRangeSizeSequenceMatcher(RSequenceEnum.LIST, min_size=1, max_size=3),
                              RRangeSizeSequenceMatcher(RSequenceEnum.TUPLE, min_size=1, max_size=3),
                              is_equal=False)
    RTestUtil.test_eq_ne_hash(RRangeSizeSequenceMatcher(RSequenceEnum.TUPLE, min_size=1, max_size=3),
                              RRangeSizeSequenceMatcher(RSequenceEnum.TUPLE, min_size=1, max_size=3),
                              is_equal=True)
    RTestUtil.test_eq_ne_hash(RRangeSizeSequenceMatcher(RSequenceEnum.TUPLE, min_size=1, max_size=4),
                              RRangeSizeSequenceMatcher(RSequenceEnum.TUPLE, min_size=1, max_size=3),
                              is_equal=False)
    RTestUtil.test_eq_ne_hash(RRangeSizeSequenceMatcher(RSequenceEnum.TUPLE, min_size=2, max_size=3),
                              RRangeSizeSequenceMatcher(RSequenceEnum.TUPLE, min_size=1, max_size=3),
                              is_equal=False)
    RTestUtil.test_eq_ne_hash(RRangeSizeSequenceMatcher(RSequenceEnum.TUPLE, min_size=2, max_size=3),
                              RRangeSizeSequenceMatcher(RSequenceEnum.TUPLE, min_size=1, max_size=4),
                              is_equal=False)
    RTestUtil.test_eq_ne_hash(RRangeSizeSequenceMatcher(RSequenceEnum.TUPLE, min_size=2, max_size=3),
                              RRangeSizeSequenceMatcher(RSequenceEnum.SEQUENCE, min_size=1, max_size=4),
                              is_equal=False)

def test__str__():
    assert str(RRangeSizeSequenceMatcher(RSequenceEnum.LIST, min_size=1, max_size=3)) \
           == 'list where size >= 1 and size <= 3'