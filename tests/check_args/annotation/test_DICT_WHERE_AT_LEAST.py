from rambutan3.check_args.annotation.BOOL import BOOL
from rambutan3.check_args.annotation.DICT_WHERE_AT_LEAST import DICT_WHERE_AT_LEAST
from rambutan3.check_args.annotation.FLOAT import FLOAT
from rambutan3.check_args.annotation.INT import INT
from rambutan3.check_args.annotation.NONE import NONE
from rambutan3.check_args.annotation.STR import STR


def test():
    assert DICT_WHERE_AT_LEAST({"int_data": INT, "str_data": STR}) \
        .matches({"int_data": 123, "str_data": "abc"})
    assert not DICT_WHERE_AT_LEAST({"int_data": INT, "str_data": STR}) \
        .matches({"int_data": "abc", "str_data": "abc"})
    assert DICT_WHERE_AT_LEAST({"int_data": INT, "str_data": STR}) \
        .matches({"int_data": 123, "str_data": "abc", "bool_data": True})
    assert not DICT_WHERE_AT_LEAST({"int_data": INT, "str_data": STR}) \
        .matches({"int_dataXYZ": 123, "str_data": "abc"})
    assert not DICT_WHERE_AT_LEAST({"int_data": INT, "str_data": STR}) \
        .matches(None)
    assert not DICT_WHERE_AT_LEAST({"int_data": INT, "str_data": STR}) \
        .matches({})
    assert not DICT_WHERE_AT_LEAST({"int_data": INT, "str_data": STR}) \
        .matches([])
    assert not DICT_WHERE_AT_LEAST({"int_data": INT, "str_data": STR}) \
        .matches({"int_data": 123})
    assert not DICT_WHERE_AT_LEAST({"int_data": INT, "str_data": STR}) \
        .matches({"str_data": "abc"})
    assert DICT_WHERE_AT_LEAST({"int_data": INT, "str_or_bool_data": STR | BOOL}) \
        .matches({"int_data": 123, "str_or_bool_data": "abc"})
    assert DICT_WHERE_AT_LEAST({"int_data": INT, "str_or_bool_data": STR | BOOL}) \
        .matches({"int_data": 123, "str_or_bool_data": False})
    assert DICT_WHERE_AT_LEAST({"d": DICT_WHERE_AT_LEAST({"x": FLOAT})}) \
        .matches({"d": {"x": 123.456}})
    assert DICT_WHERE_AT_LEAST({"d": DICT_WHERE_AT_LEAST({"x": FLOAT})}) \
        .matches({"d": {"x": 123.456, "y": None}})
    assert not DICT_WHERE_AT_LEAST({"d": DICT_WHERE_AT_LEAST({"x": FLOAT})}) \
        .matches({"d": {"xyz": 123.456, "y": None}})

    assert DICT_WHERE_AT_LEAST({}) \
        .matches({})

    assert DICT_WHERE_AT_LEAST({}) \
        .matches({"extra_key": 123})

    assert not DICT_WHERE_AT_LEAST({"abc": INT}) \
        .matches({})

    assert not DICT_WHERE_AT_LEAST({"abc": INT}) \
        .matches({"extra_key": 123})

    assert not DICT_WHERE_AT_LEAST({"abc": NONE}) \
        .matches({})

    assert DICT_WHERE_AT_LEAST({"abc": NONE}) \
        .matches({"abc": None})

    assert DICT_WHERE_AT_LEAST({"abc": NONE}) \
        .matches({"abc": None, "extra_key": None})

    assert not DICT_WHERE_AT_LEAST({"abc": NONE}) \
        .matches({"extra_key": None})
