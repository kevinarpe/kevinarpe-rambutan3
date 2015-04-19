from rambutan3.check_args.annotation.INT import INT
from rambutan3.check_args.annotation.LIST import LIST
from rambutan3.check_args.annotation.LIST_OF import LIST_OF
from rambutan3.check_args.annotation.NONE import NONE
from rambutan3.check_args.annotation.STR import STR


def test():
    assert LIST_OF(INT).matches([])
    assert LIST_OF(LIST).matches([[1, 2], [3, 4]])
    assert LIST_OF(LIST_OF(STR)).matches([["a", "b"], ["d", "e"]])
    assert LIST_OF(INT).matches(list())
    assert LIST_OF(INT).matches([1, 2, 3])
    assert not LIST_OF(INT).matches([1, 2, 3, "abc"])
    assert LIST_OF(INT | STR).matches([1, 2, 3, "abc"])
    assert not LIST_OF(INT).matches([1, 2, 3, "abc", None])
    assert LIST_OF(INT | STR | NONE).matches([1, 2, 3, "abc", None])
    assert not LIST_OF(INT).matches("abc")
    assert not LIST_OF(INT).matches(None)
    assert not LIST_OF(INT).matches(tuple())
    assert not LIST_OF(INT).matches((1, 2, 3))
