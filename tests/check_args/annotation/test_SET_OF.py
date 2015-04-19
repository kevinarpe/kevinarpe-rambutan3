from rambutan3.check_args.annotation.INT import INT
from rambutan3.check_args.annotation.SET_OF import SET_OF
from rambutan3.check_args.annotation.NONE import NONE
from rambutan3.check_args.annotation.STR import STR
from rambutan3.check_args.annotation.TUPLE import TUPLE
from rambutan3.check_args.annotation.TUPLE_OF import TUPLE_OF


def test():
    assert SET_OF(INT).matches(set())
    assert SET_OF(TUPLE).matches({(1, 2), (3, 4)})
    assert SET_OF(TUPLE_OF(STR)).matches({("a", "b"), ("d", "e")})
    assert SET_OF(INT).matches({1, 2, 3})
    assert not SET_OF(INT).matches({1, 2, 3, "abc"})
    assert SET_OF(INT | STR).matches({1, 2, 3, "abc"})
    assert not SET_OF(INT).matches({1, 2, 3, "abc", None})
    assert SET_OF(INT | STR | NONE).matches({1, 2, 3, "abc", None})
    assert not SET_OF(INT).matches("abc")
    assert not SET_OF(INT).matches(None)
    assert not SET_OF(INT).matches(tuple())
    assert not SET_OF(INT).matches((1, 2, 3))
