from rambutan3.check_args.annotation.ANY import ANY
from rambutan3.check_args.annotation.INT import INT
from rambutan3.check_args.annotation.ONE_OR_MORE_OF import ONE_OR_MORE_OF


def test():
    assert ONE_OR_MORE_OF(ANY).matches(None)
    assert ONE_OR_MORE_OF(ANY).matches([None])
    assert ONE_OR_MORE_OF(INT).matches(123)
    assert not ONE_OR_MORE_OF(INT).matches('abc')
    assert ONE_OR_MORE_OF(INT).matches([123])
    assert not ONE_OR_MORE_OF(INT).matches(['abc'])
    assert not ONE_OR_MORE_OF(INT).matches([])
    assert not ONE_OR_MORE_OF(INT).matches(set())
    assert ONE_OR_MORE_OF(INT).matches({1,2,3})
