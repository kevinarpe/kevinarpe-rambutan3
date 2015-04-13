from rambutan3.type.matcher.annotation.DICT_OF import DICT_OF
from rambutan3.type.matcher.annotation.INT import INT
from rambutan3.type.matcher.annotation.STR import STR


def test():
    assert DICT_OF(key_matcher=INT, value_matcher=STR).matches({})
    assert DICT_OF(key_matcher=INT, value_matcher=STR).matches(dict())
    assert DICT_OF(key_matcher=INT, value_matcher=STR).matches({123: "abc"})
    assert not DICT_OF(key_matcher=INT, value_matcher=STR).matches({"abc": 123})
    assert DICT_OF(key_matcher=STR, value_matcher=INT).matches({"abc": 123})
    assert DICT_OF(key_matcher=STR | INT, value_matcher=INT).matches({"abc": 123})
    assert DICT_OF(key_matcher=INT | STR, value_matcher=INT).matches({"abc": 123})
    assert not DICT_OF(key_matcher=INT, value_matcher=STR).matches({"abc": "def"})
    assert DICT_OF(key_matcher=STR | INT, value_matcher=STR).matches({"abc": "def"})
    assert not DICT_OF(key_matcher=INT, value_matcher=STR).matches({456: 123})
    assert DICT_OF(key_matcher=INT, value_matcher=STR).matches({123: "abc", 456: "xyz"})
    assert DICT_OF(key_matcher=INT | STR, value_matcher=STR).matches({123: "abc", 456: "xyz", "q": "kdb"})
