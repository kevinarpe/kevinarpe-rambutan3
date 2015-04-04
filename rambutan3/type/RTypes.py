import re
import types

__REGEX_PATTERN_TYPE = type(re.compile(''))


def REGEX_PATTERN_TYPE():
    return __REGEX_PATTERN_TYPE


__REGEX_MATCH_TYPE = type(re.compile('').match(''))


def REGEX_MATCH_TYPE():
    return __REGEX_MATCH_TYPE


__FUNCTION_TYPE_TUPLE = (types.FunctionType, types.BuiltinFunctionType)


def FUNCTION_TYPE_TUPLE():
    return __FUNCTION_TYPE_TUPLE


__NUMBER_TYPE_TUPLE = (int, float)


def NUMBER_TYPE_TUPLE():
    return __NUMBER_TYPE_TUPLE
