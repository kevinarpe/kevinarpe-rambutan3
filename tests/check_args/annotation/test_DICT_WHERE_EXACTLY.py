from rambutan3.check_args.annotation.BOOL import BOOL
from rambutan3.check_args.annotation.BUILTIN_DICT_WHERE_EXACTLY import BUILTIN_DICT_WHERE_EXACTLY
from rambutan3.check_args.annotation.DICT_WHERE_EXACTLY import DICT_WHERE_EXACTLY
from rambutan3.check_args.annotation.FLOAT import FLOAT
from rambutan3.check_args.annotation.INT import INT
from rambutan3.check_args.annotation.NONE import NONE
from rambutan3.check_args.annotation.NON_EMPTY_LIST_OF import NON_EMPTY_LIST_OF
from rambutan3.check_args.annotation.POSITIVE_INT import POSITIVE_INT
from rambutan3.check_args.annotation.STR import STR
from rambutan3.check_args.annotation.STR_IDENTIFIER import STR_IDENTIFIER
from rambutan3.check_args.annotation.STR_MESSAGE_TEXT import STR_MESSAGE_TEXT


def test():
    assert DICT_WHERE_EXACTLY({"int_data": INT, "str_data": STR}) \
        .matches({"int_data": 123, "str_data": "abc"})
    assert not DICT_WHERE_EXACTLY({"int_data": INT, "str_data": STR}) \
        .matches({"int_data": "abc", "str_data": "abc"})
    assert not DICT_WHERE_EXACTLY({"int_data": INT, "str_data": STR}) \
        .matches({"int_data": 123, "str_data": "abc", "bool_data": True})
    assert not DICT_WHERE_EXACTLY({"int_data": INT, "str_data": STR}) \
        .matches({"int_dataXYZ": 123, "str_data": "abc"})
    assert not DICT_WHERE_EXACTLY({"int_data": INT, "str_data": STR}) \
        .matches(None)
    assert not DICT_WHERE_EXACTLY({"int_data": INT, "str_data": STR}) \
        .matches({})
    assert not DICT_WHERE_EXACTLY({"int_data": INT, "str_data": STR}) \
        .matches([])
    assert not DICT_WHERE_EXACTLY({"int_data": INT, "str_data": STR}) \
        .matches({"int_data": 123})
    assert not DICT_WHERE_EXACTLY({"int_data": INT, "str_data": STR}) \
        .matches({"str_data": "abc"})
    assert DICT_WHERE_EXACTLY({"int_data": INT, "str_or_bool_data": STR | BOOL}) \
        .matches({"int_data": 123, "str_or_bool_data": "abc"})
    assert DICT_WHERE_EXACTLY({"int_data": INT, "str_or_bool_data": STR | BOOL}) \
        .matches({"int_data": 123, "str_or_bool_data": False})
    assert DICT_WHERE_EXACTLY({"d": DICT_WHERE_EXACTLY({"x": FLOAT})}) \
        .matches({"d": {"x": 123.456}})
    assert not DICT_WHERE_EXACTLY({"d": DICT_WHERE_EXACTLY({"x": FLOAT})}) \
        .matches({"d": {"x": 123.456, "y": None}})
    assert not DICT_WHERE_EXACTLY({"d": DICT_WHERE_EXACTLY({"x": FLOAT})}) \
        .matches({"d": {"xyz": 123.456, "y": None}})

    assert DICT_WHERE_EXACTLY({}) \
        .matches({})

    assert not DICT_WHERE_EXACTLY({}) \
        .matches({"extra_key": 123})

    assert not DICT_WHERE_EXACTLY({"abc": INT}) \
        .matches({})

    assert not DICT_WHERE_EXACTLY({"abc": INT}) \
        .matches({"extra_key": 123})

    assert not DICT_WHERE_EXACTLY({"abc": NONE}) \
        .matches({})

    assert DICT_WHERE_EXACTLY({"abc": NONE}) \
        .matches({"abc": None})

    assert not DICT_WHERE_EXACTLY({"abc": NONE}) \
        .matches({"abc": None, "extra_key": None})

    assert not DICT_WHERE_EXACTLY({"abc": NONE}) \
        .matches({"extra_key": None})

# def test_check_arg():
#     # try:
#     #     BUILTIN_DICT_WHERE_EXACTLY({}).check_arg({"extra_key": 123}, "user_credentials")
#     #     raise RUnreachableCode()
#     # except RCheckArgsError as e:
#     #     assert e.args[0] == \
#     #            "Argument 'user_credentials': Expected type [dict where EXACTLY {}], but found type [dict]: [{'extra_key': 123}]" \
#     #            "\n\tError: Extra items: {'extra_key': 123}"
#
#     # TODO: LAST
#     # BUILTIN_DICT_WHERE_EXACTLY({"abc": INT}).check_arg({}, "user_credentials")
#     m = BUILTIN_DICT_WHERE_EXACTLY(
#         {
#             "apps": NON_EMPTY_LIST_OF(BUILTIN_DICT_WHERE_EXACTLY(
#                 {
#                     "name": STR_MESSAGE_TEXT | STR_IDENTIFIER,
#                     "size": POSITIVE_INT
#                 }
#             ))
#         })
#     v = {
#         "apps": [
#             {
#                 "name": "blah",
#                 "size": 123
#             },
#             {
#                 "name": " ",
#                 "size": 123
#             }
#         ]
#     }
#     m.check_arg(v, "arg_name_is_v")
