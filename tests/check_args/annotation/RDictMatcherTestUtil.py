import types

from rambutan3.check_args.annotation.BOOL import BOOL
from rambutan3.check_args.annotation.FLOAT import FLOAT
from rambutan3.check_args.annotation.INT import INT
from rambutan3.check_args.annotation.NONE import NONE
from rambutan3.check_args.annotation.STR import STR
from rambutan3.check_args.dict.RDictMatcher import RDictMatcher


def core_test_dict_matcher(dict_matcher: RDictMatcher):
    assert dict_matcher.matches({})
    assert dict_matcher.matches(dict())
    assert dict_matcher.matches({1: 2, 3: 4})
    assert dict_matcher.matches({"abc": 2, 3.789: 4})
    assert dict_matcher.matches({None: 2, 3: None})
    assert not dict_matcher.matches("abc")
    assert not dict_matcher.matches(None)
    assert not dict_matcher.matches(tuple())
    assert not dict_matcher.matches((1, 2, 3))


def core_test_dict_of_matcher(dict_of_matcher: types.FunctionType):
    assert dict_of_matcher(key_matcher=INT, value_matcher=STR).matches({})
    assert dict_of_matcher(key_matcher=INT, value_matcher=STR).matches(dict())
    assert dict_of_matcher(key_matcher=INT, value_matcher=STR).matches({123: "abc"})
    assert not dict_of_matcher(key_matcher=INT, value_matcher=STR).matches({"abc": 123})
    assert dict_of_matcher(key_matcher=STR, value_matcher=INT).matches({"abc": 123})
    assert dict_of_matcher(key_matcher=STR | INT, value_matcher=INT).matches({"abc": 123})
    assert dict_of_matcher(key_matcher=INT | STR, value_matcher=INT).matches({"abc": 123})
    assert not dict_of_matcher(key_matcher=INT, value_matcher=STR).matches({"abc": "def"})
    assert dict_of_matcher(key_matcher=STR | INT, value_matcher=STR).matches({"abc": "def"})
    assert not dict_of_matcher(key_matcher=INT, value_matcher=STR).matches({456: 123})
    assert dict_of_matcher(key_matcher=INT, value_matcher=STR).matches({123: "abc", 456: "xyz"})
    assert dict_of_matcher(key_matcher=INT | STR, value_matcher=STR).matches({123: "abc", 456: "xyz", "q": "kdb"})


def core_test_dict_where_at_least_matcher(dict_where_at_least_matcher: types.FunctionType):
    assert dict_where_at_least_matcher({"int_data": INT, "str_data": STR}) \
        .matches({"int_data": 123, "str_data": "abc"})
    assert not dict_where_at_least_matcher({"int_data": INT, "str_data": STR}) \
        .matches({"int_data": "abc", "str_data": "abc"})
    assert dict_where_at_least_matcher({"int_data": INT, "str_data": STR}) \
        .matches({"int_data": 123, "str_data": "abc", "bool_data": True})
    assert not dict_where_at_least_matcher({"int_data": INT, "str_data": STR}) \
        .matches({"int_dataXYZ": 123, "str_data": "abc"})
    assert not dict_where_at_least_matcher({"int_data": INT, "str_data": STR}) \
        .matches(None)
    assert not dict_where_at_least_matcher({"int_data": INT, "str_data": STR}) \
        .matches({})
    assert not dict_where_at_least_matcher({"int_data": INT, "str_data": STR}) \
        .matches([])
    assert not dict_where_at_least_matcher({"int_data": INT, "str_data": STR}) \
        .matches({"int_data": 123})
    assert not dict_where_at_least_matcher({"int_data": INT, "str_data": STR}) \
        .matches({"str_data": "abc"})
    assert dict_where_at_least_matcher({"int_data": INT, "str_or_bool_data": STR | BOOL}) \
        .matches({"int_data": 123, "str_or_bool_data": "abc"})
    assert dict_where_at_least_matcher({"int_data": INT, "str_or_bool_data": STR | BOOL}) \
        .matches({"int_data": 123, "str_or_bool_data": False})
    assert dict_where_at_least_matcher({"d": dict_where_at_least_matcher({"x": FLOAT})}) \
        .matches({"d": {"x": 123.456}})
    assert dict_where_at_least_matcher({"d": dict_where_at_least_matcher({"x": FLOAT})}) \
        .matches({"d": {"x": 123.456, "y": None}})
    assert not dict_where_at_least_matcher({"d": dict_where_at_least_matcher({"x": FLOAT})}) \
        .matches({"d": {"xyz": 123.456, "y": None}})

    assert dict_where_at_least_matcher({}) \
        .matches({})

    assert dict_where_at_least_matcher({}) \
        .matches({"extra_key": 123})

    assert not dict_where_at_least_matcher({"abc": INT}) \
        .matches({})

    assert not dict_where_at_least_matcher({"abc": INT}) \
        .matches({"extra_key": 123})

    assert not dict_where_at_least_matcher({"abc": NONE}) \
        .matches({})

    assert dict_where_at_least_matcher({"abc": NONE}) \
        .matches({"abc": None})

    assert dict_where_at_least_matcher({"abc": NONE}) \
        .matches({"abc": None, "extra_key": None})

    assert not dict_where_at_least_matcher({"abc": NONE}) \
        .matches({"extra_key": None})


def core_test_dict_where_exactly_matcher(dict_where_exactly_matcher: types.FunctionType):
    assert dict_where_exactly_matcher({"int_data": INT, "str_data": STR}) \
        .matches({"int_data": 123, "str_data": "abc"})
    assert not dict_where_exactly_matcher({"int_data": INT, "str_data": STR}) \
        .matches({"int_data": "abc", "str_data": "abc"})
    assert not dict_where_exactly_matcher({"int_data": INT, "str_data": STR}) \
        .matches({"int_data": 123, "str_data": "abc", "bool_data": True})
    assert not dict_where_exactly_matcher({"int_data": INT, "str_data": STR}) \
        .matches({"int_dataXYZ": 123, "str_data": "abc"})
    assert not dict_where_exactly_matcher({"int_data": INT, "str_data": STR}) \
        .matches(None)
    assert not dict_where_exactly_matcher({"int_data": INT, "str_data": STR}) \
        .matches({})
    assert not dict_where_exactly_matcher({"int_data": INT, "str_data": STR}) \
        .matches([])
    assert not dict_where_exactly_matcher({"int_data": INT, "str_data": STR}) \
        .matches({"int_data": 123})
    assert not dict_where_exactly_matcher({"int_data": INT, "str_data": STR}) \
        .matches({"str_data": "abc"})
    assert dict_where_exactly_matcher({"int_data": INT, "str_or_bool_data": STR | BOOL}) \
        .matches({"int_data": 123, "str_or_bool_data": "abc"})
    assert dict_where_exactly_matcher({"int_data": INT, "str_or_bool_data": STR | BOOL}) \
        .matches({"int_data": 123, "str_or_bool_data": False})
    assert dict_where_exactly_matcher({"d": dict_where_exactly_matcher({"x": FLOAT})}) \
        .matches({"d": {"x": 123.456}})
    assert not dict_where_exactly_matcher({"d": dict_where_exactly_matcher({"x": FLOAT})}) \
        .matches({"d": {"x": 123.456, "y": None}})
    assert not dict_where_exactly_matcher({"d": dict_where_exactly_matcher({"x": FLOAT})}) \
        .matches({"d": {"xyz": 123.456, "y": None}})

    assert dict_where_exactly_matcher({}) \
        .matches({})

    assert not dict_where_exactly_matcher({}) \
        .matches({"extra_key": 123})

    assert not dict_where_exactly_matcher({"abc": INT}) \
        .matches({})

    assert not dict_where_exactly_matcher({"abc": INT}) \
        .matches({"extra_key": 123})

    assert not dict_where_exactly_matcher({"abc": NONE}) \
        .matches({})

    assert dict_where_exactly_matcher({"abc": NONE}) \
        .matches({"abc": None})

    assert not dict_where_exactly_matcher({"abc": NONE}) \
        .matches({"abc": None, "extra_key": None})

    assert not dict_where_exactly_matcher({"abc": NONE}) \
        .matches({"extra_key": None})
