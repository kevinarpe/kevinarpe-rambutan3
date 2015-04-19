import operator

from rambutan3.check_args.annotation.FUNC import FUNC


def dummy():
    pass


def test():
    assert FUNC.matches(operator.abs)
    assert FUNC.matches(dummy)
    assert not FUNC.matches(None)
    assert not FUNC.matches(123)
    assert not FUNC.matches("abc")
