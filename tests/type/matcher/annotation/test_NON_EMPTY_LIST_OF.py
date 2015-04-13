from rambutan3.type.matcher.annotation.INT import INT
from rambutan3.type.matcher.annotation.LIST import LIST
from rambutan3.type.matcher.annotation.NON_EMPTY_LIST_OF import NON_EMPTY_LIST_OF
from rambutan3.type.matcher.annotation.NONE import NONE
from rambutan3.type.matcher.annotation.STR import STR


def test():
    assert not NON_EMPTY_LIST_OF(INT).matches([])
    assert NON_EMPTY_LIST_OF(LIST).matches([[1, 2], [3, 4], []])
    assert NON_EMPTY_LIST_OF(NON_EMPTY_LIST_OF(STR)).matches([["a", "b"], ["d", "e"]])
    assert not NON_EMPTY_LIST_OF(INT).matches(list())
    assert NON_EMPTY_LIST_OF(INT).matches([1, 2, 3])
    assert not NON_EMPTY_LIST_OF(INT).matches([1, 2, 3, "abc"])
    assert NON_EMPTY_LIST_OF(INT | STR).matches([1, 2, 3, "abc"])
    assert not NON_EMPTY_LIST_OF(INT).matches([1, 2, 3, "abc", None])
    assert NON_EMPTY_LIST_OF(INT | STR | NONE).matches([1, 2, 3, "abc", None])
    assert not NON_EMPTY_LIST_OF(INT).matches("abc")
    assert not NON_EMPTY_LIST_OF(INT).matches(None)
    assert not NON_EMPTY_LIST_OF(INT).matches(tuple())
    assert not NON_EMPTY_LIST_OF(INT).matches((1, 2, 3))
