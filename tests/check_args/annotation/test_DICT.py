from rambutan3.check_args.annotation.DICT import DICT


def test():
    assert DICT.matches({})
    assert DICT.matches(dict())
    assert DICT.matches({1: 2, 3: 4})
    assert DICT.matches({"abc": 2, 3.789: 4})
    assert DICT.matches({None: 2, 3: None})
    assert not DICT.matches("abc")
    assert not DICT.matches(None)
    assert not DICT.matches(tuple())
    assert not DICT.matches((1, 2, 3))
