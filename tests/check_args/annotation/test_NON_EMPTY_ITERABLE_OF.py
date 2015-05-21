from rambutan3.check_args.annotation.INT import INT
from rambutan3.check_args.annotation.ITERABLE import ITERABLE
from rambutan3.check_args.annotation.NON_EMPTY_ITERABLE_OF import NON_EMPTY_ITERABLE_OF
from rambutan3.check_args.annotation.NONE import NONE
from rambutan3.check_args.annotation.STR import STR


def test():
    assert not NON_EMPTY_ITERABLE_OF(INT).matches([])
    assert NON_EMPTY_ITERABLE_OF(ITERABLE).matches([[1, 2], [3, 4], []])
    assert NON_EMPTY_ITERABLE_OF(NON_EMPTY_ITERABLE_OF(STR)).matches([["a", "b"], ["d", "e"]])
    assert not NON_EMPTY_ITERABLE_OF(INT).matches(list())
    assert NON_EMPTY_ITERABLE_OF(INT).matches([1, 2, 3])
    assert not NON_EMPTY_ITERABLE_OF(INT).matches([1, 2, 3, "abc"])
    assert NON_EMPTY_ITERABLE_OF(INT | STR).matches([1, 2, 3, "abc"])
    assert not NON_EMPTY_ITERABLE_OF(INT).matches([1, 2, 3, "abc", None])
    assert NON_EMPTY_ITERABLE_OF(INT | STR | NONE).matches([1, 2, 3, "abc", None])
    assert not NON_EMPTY_ITERABLE_OF(INT).matches("abc")
    assert not NON_EMPTY_ITERABLE_OF(INT).matches(None)
    assert not NON_EMPTY_ITERABLE_OF(INT).matches(tuple())
    assert NON_EMPTY_ITERABLE_OF(INT).matches((1, 2, 3))
