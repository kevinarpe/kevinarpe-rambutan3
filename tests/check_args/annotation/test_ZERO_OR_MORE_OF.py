from rambutan3.check_args.annotation.ANY import ANY
from rambutan3.check_args.annotation.INT import INT
from rambutan3.check_args.annotation.ZERO_OR_MORE_OF import ZERO_OR_MORE_OF


def test():
    assert ZERO_OR_MORE_OF(ANY).matches(None)
    assert ZERO_OR_MORE_OF(ANY).matches([None])
    assert ZERO_OR_MORE_OF(INT).matches(123)
    assert not ZERO_OR_MORE_OF(INT).matches('abc')
    assert ZERO_OR_MORE_OF(INT).matches([123])
    assert not ZERO_OR_MORE_OF(INT).matches(['abc'])
    assert ZERO_OR_MORE_OF(INT).matches([])
    assert ZERO_OR_MORE_OF(INT).matches(set())
    assert ZERO_OR_MORE_OF(INT).matches({1,2,3})
