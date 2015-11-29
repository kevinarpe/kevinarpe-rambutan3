from rambutan3.check_args.annotation.DICT_WHERE_EXACTLY import DICT_WHERE_EXACTLY
from tests.check_args.annotation import RDictMatcherTestUtil


def test():
    RDictMatcherTestUtil.core_test_dict_where_exactly_matcher(DICT_WHERE_EXACTLY)

# def test_check_arg():
#     # try:
#     #     BUILTIN_DICT_WHERE_EXACTLY({}).check_arg({"extra_key": 123}, "user_credentials")
#     #     raise RUnreachableCode()
#     # except RCheckArgsError as e:
#     #     assert e.args[0] == \
#     #            "Argument 'user_credentials': Expected type [dict where EXACTLY {}], but found type [dict]: [{'extra_key': 123}]" \
#     #            "\n\tError: Extra items: {'extra_key': 123}"
#
#     # BUILTIN_DICT_WHERE_EXACTLY({"abc": INT}).check_arg({}, "user_credentials")
#     m = BUILTIN_DICT_WHERE_EXACTLY(
#         {
#             "apps": NON_EMPTY_LIST_OF(BUILTIN_DICT_WHERE_EXACTLY(
#                 {
#                     "name": STR_MESSAGE_TEXT | STR_STRICT_IDENTIFIER,
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
