from rambutan3.check_args.annotation.INT import INT
from rambutan3.check_args.annotation.ITERABLE import ITERABLE
from rambutan3.check_args.annotation.ITERABLE_OF import ITERABLE_OF
from rambutan3.check_args.annotation.NONE import NONE
from rambutan3.check_args.annotation.STR import STR


def test():
    assert ITERABLE_OF(INT).matches([])
    assert ITERABLE_OF(ITERABLE).matches([[1, 2], [3, 4]])
    assert ITERABLE_OF(ITERABLE_OF(STR)).matches([["a", "b"], ["d", "e"]])
    assert ITERABLE_OF(INT).matches(list())
    assert ITERABLE_OF(INT).matches([1, 2, 3])
    assert not ITERABLE_OF(INT).matches([1, 2, 3, "abc"])
    assert ITERABLE_OF(INT | STR).matches([1, 2, 3, "abc"])
    assert not ITERABLE_OF(INT).matches([1, 2, 3, "abc", None])
    assert ITERABLE_OF(INT | STR | NONE).matches([1, 2, 3, "abc", None])
    assert not ITERABLE_OF(INT).matches("abc")
    assert not ITERABLE_OF(INT).matches(None)
    assert ITERABLE_OF(INT).matches(tuple())
    assert ITERABLE_OF(INT).matches((1, 2, 3))
