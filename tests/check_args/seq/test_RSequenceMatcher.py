import pytest

from rambutan3.check_args.seq.RSequenceEnum import RSequenceEnum
from rambutan3.check_args.seq.RSequenceMatcher import RSequenceMatcher


def test_ctor():
    RSequenceMatcher(RSequenceEnum.TUPLE)

    with pytest.raises(TypeError):
        RSequenceMatcher("abc")
