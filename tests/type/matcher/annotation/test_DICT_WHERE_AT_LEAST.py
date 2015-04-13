from rambutan3.type.matcher.annotation.BOOL import BOOL
from rambutan3.type.matcher.annotation.DICT_WHERE_AT_LEAST import DICT_WHERE_AT_LEAST
from rambutan3.type.matcher.annotation.FLOAT import FLOAT
from rambutan3.type.matcher.annotation.INT import INT
from rambutan3.type.matcher.annotation.STR import STR


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
