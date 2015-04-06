from rambutan3.type.matcher.annotation.INT import INT
from rambutan3.type.matcher.annotation.LIST import LIST
from rambutan3.type.matcher.annotation.LIST_OF import LIST_OF
from rambutan3.type.matcher.annotation.OPT import OPT
from rambutan3.type.matcher.annotation.STR import STR


def test():
    assert LIST_OF(INT).matches([])
    assert LIST_OF(LIST).matches([[1, 2], [3, 4]])
    assert LIST_OF(LIST_OF(STR)).matches([["a", "b"], ["d", "e"]])
    assert LIST_OF(INT).matches(list())
    assert LIST_OF(INT).matches([1, 2, 3])
    assert not LIST_OF(INT).matches([1, 2, 3, "abc"])
    assert LIST_OF(INT | STR).matches([1, 2, 3, "abc"])
    assert not LIST_OF(INT).matches([1, 2, 3, "abc", None])
    assert LIST_OF(INT | STR | OPT).matches([1, 2, 3, "abc", None])
    assert not LIST_OF(INT).matches("abc")
    assert not LIST_OF(INT).matches(None)
    assert not LIST_OF(INT).matches(tuple())
    assert not LIST_OF(INT).matches((1, 2, 3))
