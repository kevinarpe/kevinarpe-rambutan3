from rambutan3.check_args.annotation.DICT_OF import DICT_OF
from rambutan3.check_args.annotation.INT import INT
from rambutan3.check_args.annotation.STR import STR


def test():
    assert DICT_OF(key_matcher=INT, type_matcher=STR).matches({})
    assert DICT_OF(key_matcher=INT, type_matcher=STR).matches(dict())
    assert DICT_OF(key_matcher=INT, type_matcher=STR).matches({123: "abc"})
    assert not DICT_OF(key_matcher=INT, type_matcher=STR).matches({"abc": 123})
    assert DICT_OF(key_matcher=STR, type_matcher=INT).matches({"abc": 123})
    assert DICT_OF(key_matcher=STR | INT, type_matcher=INT).matches({"abc": 123})
    assert DICT_OF(key_matcher=INT | STR, type_matcher=INT).matches({"abc": 123})
    assert not DICT_OF(key_matcher=INT, type_matcher=STR).matches({"abc": "def"})
    assert DICT_OF(key_matcher=STR | INT, type_matcher=STR).matches({"abc": "def"})
    assert not DICT_OF(key_matcher=INT, type_matcher=STR).matches({456: 123})
    assert DICT_OF(key_matcher=INT, type_matcher=STR).matches({123: "abc", 456: "xyz"})
    assert DICT_OF(key_matcher=INT | STR, type_matcher=STR).matches({123: "abc", 456: "xyz", "q": "kdb"})
