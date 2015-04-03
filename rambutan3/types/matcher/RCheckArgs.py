from functools import lru_cache
import importlib
import inspect
import types
import collections

from rambutan3 import RArgs
from rambutan3.types import RTypes
from rambutan3.types.matcher.RAbstractTypeMatcher import RAbstractTypeMatcher, RLogicalOrTypeMatcher
from rambutan3.types.matcher.RAnyValueOfMatcher import RAnyValueOfMatcher
from rambutan3.types.matcher.RSubclassMatcher import RSubclassMatcher
from rambutan3.types.matcher.RAnyTypeMatcher import RAnyTypeMatcher
from rambutan3.types.matcher.ROptionalTypeMatcher import ROptionalTypeMatcher
from rambutan3.types.matcher.RInstanceMatcher import RInstanceMatcher
from rambutan3.types.matcher.cls_or_self.RClassInstanceMatcher import RClassInstanceMatcher
from rambutan3.types.matcher.cls_or_self.RSelfInstanceMatcher import RSelfInstanceMatcher
from rambutan3.types.matcher.dict.RDictEnum import RDictEnum
from rambutan3.types.matcher.dict.RDictMatcher import RDictMatcher
from rambutan3.types.matcher.dict.RDictOfMatcher import RDictOfMatcher
from rambutan3.types.matcher.dict.RDictWhereMatcher import RDictWhereMatcher
from rambutan3.types.matcher.dict.RRangeSizeDictMatcher import RRangeSizeDictMatcher
from rambutan3.types.matcher.dict.RRangeSizeDictOfMatcher import RRangeSizeDictOfMatcher
from rambutan3.types.matcher.errfmt.RCheckArgsErrorFormatterWithPrefix import RCheckArgsErrorFormatterWithPrefix
from rambutan3.types.matcher.func.RFunctionSignatureMatcherBuilder import RFunctionSignatureMatcherBuilder
from rambutan3.types.matcher.range.RFloatRangeMatcher import RFloatRangeMatcher
from rambutan3.types.matcher.range.RIntRangeMatcher import RIntRangeMatcher
from rambutan3.types.matcher.range.RNumberRangeMatcher import RNumberRangeMatcher
from rambutan3.types.matcher.range.RRangeBoundFunctionEnumData_ import RRangeBoundFunctionEnumData_
from rambutan3.types.matcher.seq.RRangeSizeSequenceMatcher import RRangeSizeSequenceMatcher
from rambutan3.types.matcher.seq.RRangeSizeSequenceOfMatcher import RRangeSizeSequenceOfMatcher
from rambutan3.types.matcher.seq.RSequenceEnum import RSequenceEnum
from rambutan3.types.matcher.seq.RSequenceMatcher import RSequenceMatcher
from rambutan3.types.matcher.seq.RSequenceOfMatcher import RSequenceOfMatcher
from rambutan3.types.matcher.set.RRangeSizeSetMatcher import RRangeSizeSetMatcher
from rambutan3.types.matcher.set.RRangeSizeSetOfMatcher import RRangeSizeSetOfMatcher
from rambutan3.types.matcher.set.RSetEnum import RSetEnum
from rambutan3.types.matcher.set.RSetMatcher import RSetMatcher
from rambutan3.types.matcher.set.RSetOfMatcher import RSetOfMatcher
from rambutan3.types.string.RMessageText import RMessageText
from rambutan3.types.string.RNonEmptyStr import RNonEmptyStr
from rambutan3.types.string.RPatternText import RPatternText
from rambutan3.types.string.RVariableName import RVariableName


class RCheckArgsError(Exception):
    pass


ParamTuple = collections.namedtuple('ParamTuple', ['param', 'value_matcher'])


class __RCheckArgs:

    __FUNC_TYPE_TUPLE = (types.FunctionType, staticmethod, classmethod)
    __ERROR_FORMATTER = RCheckArgsErrorFormatterWithPrefix()

    def __init__(self, func: (types.FunctionType, staticmethod, classmethod)):
        RArgs.check_is_instance(func, self.__FUNC_TYPE_TUPLE, "func")
        if isinstance(func, (staticmethod, classmethod)):
            self.__unwrapped_func = getattr(func, '__func__')
        else:
            self.__unwrapped_func = func
        self.__func_signature = inspect.signature(self.__unwrapped_func)
        #: :type: dict of (str, Parameter)
        name_to_param_dict = self.__func_signature.parameters
        # Pre-allocate list
        #: :type: list of ParamTuple
#        self.__param_tuple_list = [None] * len(name_to_param_dict)
        self.__param_tuple_list = []
        #: :type index: int
        #: :type param: Parameter
        for index, param in enumerate(name_to_param_dict.values()):
            if param.annotation is inspect.Parameter.empty:
                raise RCheckArgsError("Missing type annotation for parameter #{}: '{}'".format(1 + index, param.name))
            elif isinstance(param.annotation, type):
                value_matcher = TYPE_OF(param.annotation)
            elif isinstance(param.annotation, RAbstractTypeMatcher):
                value_matcher = param.annotation
            else:
                raise RCheckArgsError("Parameter #{} '{}' annotation: Expected type '{}', but found type '{}'"
                                      .format(1 + index,
                                              param.name,
                                              RAbstractTypeMatcher.__name__,
                                              type(param.annotation).__name__))
            param_tuple = ParamTuple(param=param, value_matcher=value_matcher)
#            self.__param_tuple_list[index] = param_tuple
            self.__param_tuple_list.append(param_tuple)

        # TODO: Why is return_annotation checking disabled?
        # if self.__sig.return_annotation is inspect.Signature.empty:
        #     self.__return_value_matcher = OPT()
        # elif isinstance(self.__sig.return_annotation, type):
        #     self.__return_value_matcher = TYPE_OF(self.__sig.return_annotation)
        # elif isinstance(self.__sig.return_annotation, RValueMatcher):
        #     #: :type: RValueMatcher
        #     self.__return_value_matcher = self.__sig.return_annotation
        # else:
        #     raise RCheckArgsError("Return value annotation: Expected type '{}', but found type '{}'"
        #                           .format(RValueMatcher.__name__, type(self.__sig.return_annotation).__name__))
        self.__func = func

    def __call__(self, *args, **kwargs):
        if isinstance(self.__func, classmethod):
            cls = self._get_cls()
            try:
                #: :type: BoundArguments
                bound_args = self.__func_signature.bind(cls, *args, **kwargs)
            except TypeError as e:
                raise RCheckArgsError("Failed to bind arguments") from e
        else:
            cls = None
            try:
                #: :type: BoundArguments
                bound_args = self.__func_signature.bind(*args, **kwargs)
            except TypeError as e:
                raise RCheckArgsError("Failed to bind arguments: " + str(e)) from e

        arg_num_offset = 1
        for param_index, param_tuple in enumerate(self.__param_tuple_list):
            if isinstance(param_tuple.value_matcher, (RSelfInstanceMatcher, RClassInstanceMatcher)):
                # The first parameter for a method is always 'self', but when calling a method, 'self' is passed implicitly.
                # The first parameter for a classmethod is always 'cls', but when calling a method, 'cls' is passed implicitly.
                # Reduce the offset by one as first arg for method or classmethod will not be 'self' or 'cls'.
                arg_num_offset -= 1
                if 0 != param_index:
                    raise RCheckArgsError("SELF() and CLS() are only valid for first argument")
                if isinstance(param_tuple.value_matcher, RClassInstanceMatcher):
                    if not isinstance(self.__func, classmethod):
                        raise RCheckArgsError("CLS() is only valid for class methods (functions using @classmethod decorator)")
                    # The first argument ('cls') is never available here.  Continue with faith...
                    continue

            if param_tuple.param.name in bound_args.arguments:
                value = bound_args.arguments[param_tuple.param.name]
            elif param_tuple.param.default is not inspect.Parameter.empty:
                value = param_tuple.param.default
            else:
                raise RCheckArgsError("Argument #{} ({}) is missing and has no default value"
                                      .format(param_index + arg_num_offset, param_tuple.param.name))

            if inspect.Parameter.VAR_POSITIONAL == param_tuple.param.kind:
                value_tuple = value
                for value_index, value in enumerate(value_tuple):
                    param_tuple.value_matcher.check(value, self.__ERROR_FORMATTER, "*{}[{}]: ",
                                                    param_tuple.param.name, value_index)
            elif inspect.Parameter.VAR_KEYWORD == param_tuple.param.kind:
                key_value_dict = value
                for key, value in key_value_dict.items():
                    param_tuple.value_matcher.check(value, self.__ERROR_FORMATTER, "**{}[{}]: ",
                                                    param_tuple.param.name, key)
            else:
                param_tuple.value_matcher.check(value, self.__ERROR_FORMATTER, "Argument #{} ({}): ",
                                                param_index + arg_num_offset, param_tuple.param.name)

        if cls:
            result = self.__unwrapped_func(cls, *args, **kwargs)
        else:
            result = self.__unwrapped_func(*args, **kwargs)

        # TODO: Why is return_annotation checking disabled?
        # self.__return_value_matcher.check(result, self.__ERROR_FORMATTER, "Return value: ")

        return result

    def _get_cls(self):
        # Python does not allow this code to run from __init__, so do it here.
        if not hasattr(self, '__cls'):
            module_name = self.__unwrapped_func.__module__
            module = importlib.import_module(module_name)
            # Ex: 'MyClass.my_classmethod'
            qual_name = self.__unwrapped_func.__qualname__
            name_list = qual_name.split('.')

            # We need a for loop to handle nested classes, e.g., 'MyClass.MyNestedClass.my_classmethod'
            cls = module
            # Skip last item (method name)
            for name in name_list[:-1]:
                cls = getattr(cls, name)

            self.__cls = cls

        return self.__cls


def check_args(func: (types.FunctionType, staticmethod, classmethod)) -> types.FunctionType:
    wrapped_func = __RCheckArgs(func)

    # Why this additional layer of indirection?
    # A pure function does not eat special argument 'self'.
    # A functor (class that implements __call__()) will eat special argument 'self'.
    def check_args_delegator(*args, **kwargs):
        x = wrapped_func(*args, **kwargs)
        return x

    check_args_delegator.__doc__ = func.__doc__
    return check_args_delegator


def SELF() -> RSelfInstanceMatcher:
    x = RSelfInstanceMatcher()
    return x

def CLS() -> RClassInstanceMatcher:
    x = RClassInstanceMatcher()
    return x

@lru_cache(maxsize=None)
def SUBCLASS_OF(type_or_class: type) -> RSubclassMatcher:
    x = RSubclassMatcher(type_or_class)
    return x

__TYPE = RInstanceMatcher(type)

def TYPE() -> RInstanceMatcher:
    return __TYPE

@lru_cache(maxsize=None)
def TYPE_OF(type_or_class: type) -> RInstanceMatcher:
    x = RInstanceMatcher(type_or_class)
    return x

__TYPE_MATCHER = RInstanceMatcher(RAbstractTypeMatcher)

def TYPE_MATCHER() -> RInstanceMatcher:
    return __TYPE_MATCHER

__ANY = RAnyTypeMatcher()

def ANY() -> RInstanceMatcher:
    return __ANY

__OPT = ROptionalTypeMatcher()

def OPT() -> RInstanceMatcher:
    return __OPT

# @lru_cache(maxsize=None)
# def TYPE_MATCHER_OF(instance_matcher: RInstanceMatcher) -> RInstanceMatcherMatcher:
#     x = RInstanceMatcherMatcher(instance_matcher)
#     return x

__STR = RInstanceMatcher(str)

def STR() -> RInstanceMatcher:
    return __STR

__NON_EMPTY_STR = RInstanceMatcher(RNonEmptyStr)

def NON_EMPTY_STR() -> RInstanceMatcher:
    return __NON_EMPTY_STR

__MESSAGE_TEXT = RInstanceMatcher(RMessageText)

def MESSAGE_TEXT() -> RInstanceMatcher:
    return __MESSAGE_TEXT

__PATTERN_TEXT = RInstanceMatcher(RPatternText)

def PATTERN_TEXT() -> RInstanceMatcher:
    return __PATTERN_TEXT

__VARIABLE_NAME = RInstanceMatcher(RVariableName)

def VARIABLE_NAME() -> RInstanceMatcher:
    return __VARIABLE_NAME

__REGEX_PATTERN = RInstanceMatcher(RTypes.REGEX_PATTERN_TYPE())

def REGEX_PATTERN() -> RInstanceMatcher:
    return __REGEX_PATTERN

__BOOL = RInstanceMatcher(bool)

def BOOL() -> RInstanceMatcher:
    return __BOOL

__FUNC = RLogicalOrTypeMatcher(*(RTypes.FUNCTION_TYPE_TUPLE()))

def FUNC() -> RLogicalOrTypeMatcher:
    return __FUNC

def FUNC_OF(*matcher_tuple) -> RFunctionSignatureMatcherBuilder:
    x = RFunctionSignatureMatcherBuilder(*matcher_tuple)
    return x

def ANY_VALUE_OF(*value_tuple)- > RAnyValueOfMatcher:
    x = RAnyValueOfMatcher(*value_tuple)
    return x

__INT = RInstanceMatcher(int)

def INT() -> RInstanceMatcher:
    return __INT

__RANGE_BOUND_OP1 = ANY_VALUE_OF(*(RRangeBoundFunctionEnumData_.ONE_BOUND_OP_SET()))
__RANGE_BOUND_OP2 = ANY_VALUE_OF(*(RRangeBoundFunctionEnumData_.TWO_BOUND_OP2_SET()))


@check_args
def INT_RANGE(bound_op1: __RANGE_BOUND_OP1,
              value1: INT(),
              bound_op2: __RANGE_BOUND_OP2 | OPT()=None,
              value2: INT() | OPT()=None) \
        -> RIntRangeMatcher:
    x = RIntRangeMatcher(bound_op1, value1, bound_op2, value2)
    return x

__POSITIVE_INT = INT_RANGE('>', 0)

def POSITIVE_INT() -> RIntRangeMatcher:
    return __POSITIVE_INT

__NON_POSITIVE_INT = INT_RANGE('<=', 0)

def NON_POSITIVE_INT() -> RIntRangeMatcher:
    return __NON_POSITIVE_INT

__NEGATIVE_INT = INT_RANGE('<', 0)

def NEGATIVE_INT() -> RIntRangeMatcher:
    return __NEGATIVE_INT

__NON_NEGATIVE_INT = INT_RANGE('>=', 0)

def NON_NEGATIVE_INT() -> RIntRangeMatcher:
    return __NON_NEGATIVE_INT

__FLOAT = RInstanceMatcher(float)

def FLOAT() -> RInstanceMatcher:
    return __FLOAT

@check_args
def FLOAT_RANGE(bound1: __RANGE_BOUND_OP1,
                value1: FLOAT(),
                bound2: __RANGE_BOUND_OP2 | OPT()=None,
                value2: FLOAT() | OPT()=None) -> RFloatRangeMatcher:
    x = RFloatRangeMatcher(bound1, value1, bound2, value2)
    return x

__POSITIVE_FLOAT = FLOAT_RANGE('>', float(0))

def POSITIVE_FLOAT() -> RFloatRangeMatcher:
    return __POSITIVE_FLOAT

__NON_POSITIVE_FLOAT = FLOAT_RANGE('<=', float(0))

def NON_POSITIVE_FLOAT() -> RFloatRangeMatcher:
    return __NON_POSITIVE_FLOAT

__NEGATIVE_FLOAT = FLOAT_RANGE('<', float(0))

def NEGATIVE_FLOAT() -> RFloatRangeMatcher:
    return __NEGATIVE_FLOAT

__NON_NEGATIVE_FLOAT = FLOAT_RANGE('>=', float(0))

def NON_NEGATIVE_FLOAT() -> RFloatRangeMatcher:
    return __NON_NEGATIVE_FLOAT

__NUMBER = RInstanceMatcher(*(RTypes.NUMBER_TYPE_TUPLE()))

def NUMBER() -> RInstanceMatcher:
    return __NUMBER

@check_args
def NUMBER_RANGE(bound1: __RANGE_BOUND_OP1,
                 value1: NUMBER(),
                 bound2: __RANGE_BOUND_OP2 | OPT()=None,
                 value2: NUMBER() | OPT()=None) -> RNumberRangeMatcher:
    x = RNumberRangeMatcher(RTypes.NUMBER_TYPE_TUPLE(), bound1, value1, bound2, value2)
    return x

__POSITIVE_NUMBER = NUMBER_RANGE('>', 0)

def POSITIVE_NUMBER() -> RIntRangeMatcher:
    return __POSITIVE_NUMBER

__NON_POSITIVE_NUMBER = NUMBER_RANGE('<=', 0)

def NON_POSITIVE_NUMBER() -> RIntRangeMatcher:
    return __NON_POSITIVE_NUMBER

__NEGATIVE_NUMBER = NUMBER_RANGE('<', 0)

def NEGATIVE_NUMBER() -> RIntRangeMatcher:
    return __NEGATIVE_NUMBER

__NON_NEGATIVE_NUMBER = NUMBER_RANGE('>=', 0)

def NON_NEGATIVE_NUMBER() -> RIntRangeMatcher:
    return __NON_NEGATIVE_NUMBER

__TUPLE = RSequenceMatcher(RSequenceEnum.TUPLE)

def TUPLE() -> RSequenceMatcher:
    return __TUPLE

def TUPLE_OF(value_matcher: RAbstractTypeMatcher) -> RSequenceOfMatcher:
    x = RSequenceOfMatcher(RSequenceEnum.TUPLE, value_matcher)
    return x

def RANGE_SIZE_TUPLE(*, min_size: int=-1, max_size: int=-1) -> RRangeSizeSequenceMatcher:
    x = RRangeSizeSequenceMatcher(RSequenceEnum.TUPLE, min_size=min_size, max_size=max_size)
    return x

__NON_EMPTY_TUPLE = RRangeSizeSequenceMatcher(RSequenceEnum.TUPLE, min_size=1, max_size=-1)

def NON_EMPTY_TUPLE() -> RRangeSizeSequenceMatcher:
    return __NON_EMPTY_TUPLE

def RANGE_SIZE_TUPLE_OF(value_matcher: RAbstractTypeMatcher, *, min_size: int=-1, max_size: int=-1) \
        -> RRangeSizeSequenceOfMatcher:
    x = RRangeSizeSequenceOfMatcher(RSequenceEnum.TUPLE, value_matcher, min_size=min_size, max_size=max_size)
    return x

def NON_EMPTY_TUPLE_OF(value_matcher: RAbstractTypeMatcher) -> RRangeSizeSequenceOfMatcher:
    x = RRangeSizeSequenceOfMatcher(RSequenceEnum.TUPLE, value_matcher, min_size=1, max_size=-1)
    return x

__LIST = RSequenceMatcher(RSequenceEnum.LIST)

def LIST() -> RSequenceMatcher:
    return __LIST

def LIST_OF(value_matcher: RAbstractTypeMatcher) -> RSequenceOfMatcher:
    x = RSequenceOfMatcher(RSequenceEnum.LIST, value_matcher)
    return x

def RANGE_SIZE_LIST(*, min_size: int=-1, max_size: int=-1) -> RRangeSizeSequenceMatcher:
    x = RRangeSizeSequenceMatcher(RSequenceEnum.LIST, min_size=min_size, max_size=max_size)
    return x

__NON_EMPTY_LIST = RRangeSizeSequenceMatcher(RSequenceEnum.LIST, min_size=1, max_size=-1)

def NON_EMPTY_LIST() -> RRangeSizeSequenceMatcher:
    return __NON_EMPTY_LIST

def RANGE_SIZE_LIST_OF(value_matcher: RAbstractTypeMatcher, *, min_size: int=-1, max_size: int=-1) \
        -> RRangeSizeSequenceOfMatcher:
    x = RRangeSizeSequenceOfMatcher(RSequenceEnum.LIST, value_matcher, min_size=min_size, max_size=max_size)
    return x

def NON_EMPTY_LIST_OF(value_matcher: RAbstractTypeMatcher) -> RRangeSizeSequenceOfMatcher:
    x = RRangeSizeSequenceOfMatcher(RSequenceEnum.LIST, value_matcher, min_size=1, max_size=-1)
    return x

__SEQUENCE = RSequenceMatcher(RSequenceEnum.SEQUENCE)

def SEQUENCE() -> RSequenceMatcher:
    return __SEQUENCE

def SEQUENCE_OF(value_matcher: RAbstractTypeMatcher) -> RSequenceOfMatcher:
    x = RSequenceOfMatcher(RSequenceEnum.SEQUENCE, value_matcher)
    return x

def RANGE_SIZE_SEQUENCE(*, min_size: int=-1, max_size: int=-1) -> RRangeSizeSequenceMatcher:
    x = RRangeSizeSequenceMatcher(RSequenceEnum.SEQUENCE, min_size=min_size, max_size=max_size)
    return x

__NON_EMPTY_SEQUENCE = RRangeSizeSequenceMatcher(RSequenceEnum.SEQUENCE, min_size=1, max_size=-1)

def NON_EMPTY_SEQUENCE() -> RRangeSizeSequenceMatcher:
    return __NON_EMPTY_SEQUENCE

def RANGE_SIZE_SEQUENCE_OF(value_matcher: RAbstractTypeMatcher, *, min_size: int=-1, max_size: int=-1) \
        -> RRangeSizeSequenceOfMatcher:
    x = RRangeSizeSequenceOfMatcher(RSequenceEnum.SEQUENCE, value_matcher, min_size=min_size, max_size=max_size)
    return x

def NON_EMPTY_SEQUENCE_OF(value_matcher: RAbstractTypeMatcher) -> RRangeSizeSequenceOfMatcher:
    x = RRangeSizeSequenceOfMatcher(RSequenceEnum.SEQUENCE, value_matcher, min_size=1, max_size=-1)
    return x

__BUILTIN_SET = RSetMatcher(RSetEnum.BUILTIN_SET)

def BUILTIN_SET() -> RSetMatcher:
    return __BUILTIN_SET

def BUILTIN_SET_OF(value_matcher: RAbstractTypeMatcher) -> RSetOfMatcher:
    x = RSetOfMatcher(RSetEnum.BUILTIN_SET, value_matcher)
    return x

def RANGE_SIZE_BUILTIN_SET(*, min_size: int=-1, max_size: int=-1) -> RRangeSizeSetMatcher:
    x = RRangeSizeSetMatcher(RSetEnum.BUILTIN_SET, min_size=min_size, max_size=max_size)
    return x

__NON_EMPTY_BUILTIN_SET = RRangeSizeSetMatcher(RSetEnum.BUILTIN_SET, min_size=1, max_size=-1)

def NON_EMPTY_BUILTIN_SET() -> RRangeSizeSetMatcher:
    return __NON_EMPTY_BUILTIN_SET

def RANGE_SIZE_BUILTIN_SET_OF(value_matcher: RAbstractTypeMatcher, *, min_size: int=-1, max_size: int=-1) \
        -> RRangeSizeSetOfMatcher:
    x = RRangeSizeSetOfMatcher(RSetEnum.BUILTIN_SET, value_matcher, min_size=min_size, max_size=max_size)
    return x

def NON_EMPTY_BUILTIN_SET_OF(value_matcher: RAbstractTypeMatcher) -> RRangeSizeSetOfMatcher:
    x = RRangeSizeSetOfMatcher(RSetEnum.BUILTIN_SET, value_matcher, min_size=1, max_size=-1)
    return x

__BUILTIN_FROZENSET = RSetMatcher(RSetEnum.BUILTIN_FROZENSET)

def BUILTIN_FROZENSET() -> RSetMatcher:
    return __BUILTIN_FROZENSET

def BUILTIN_FROZENSET_OF(value_matcher: RAbstractTypeMatcher) -> RSetOfMatcher:
    x = RSetOfMatcher(RSetEnum.BUILTIN_FROZENSET, value_matcher)
    return x

def RANGE_SIZE_BUILTIN_FROZENSET(*, min_size: int=-1, max_size: int=-1) -> RRangeSizeSetMatcher:
    x = RRangeSizeSetMatcher(RSetEnum.BUILTIN_FROZENSET, min_size=min_size, max_size=max_size)
    return x

__NON_EMPTY_BUILTIN_FROZENSET = RRangeSizeSetMatcher(RSetEnum.BUILTIN_FROZENSET, min_size=1, max_size=-1)

def NON_EMPTY_BUILTIN_FROZENSET() -> RRangeSizeSetMatcher:
    return __NON_EMPTY_BUILTIN_FROZENSET

def RANGE_SIZE_BUILTIN_FROZENSET_OF(value_matcher: RAbstractTypeMatcher, *, min_size: int=-1, max_size: int=-1) \
        -> RRangeSizeSetOfMatcher:
    x = RRangeSizeSetOfMatcher(RSetEnum.BUILTIN_FROZENSET, value_matcher, min_size=min_size, max_size=max_size)
    return x

def NON_EMPTY_BUILTIN_FROZENSET_OF(value_matcher: RAbstractTypeMatcher) -> RRangeSizeSetOfMatcher:
    x = RRangeSizeSetOfMatcher(RSetEnum.BUILTIN_FROZENSET, value_matcher, min_size=1, max_size=-1)
    return x

__SET = RSetMatcher(RSetEnum.SET)

def SET() -> RSetMatcher:
    return __SET

def SET_OF(value_matcher: RAbstractTypeMatcher) -> RSetOfMatcher:
    x = RSetOfMatcher(RSetEnum.SET, value_matcher)
    return x

def RANGE_SIZE_SET(*, min_size: int=-1, max_size: int=-1) -> RRangeSizeSetMatcher:
    x = RRangeSizeSetMatcher(RSetEnum.SET, min_size=min_size, max_size=max_size)
    return x

__NON_EMPTY_SET = RRangeSizeSetMatcher(RSetEnum.SET, min_size=1, max_size=-1)

def NON_EMPTY_SET() -> RRangeSizeSetMatcher:
    return __NON_EMPTY_SET

def RANGE_SIZE_SET_OF(value_matcher: RAbstractTypeMatcher, *, min_size: int=-1, max_size: int=-1) \
        -> RRangeSizeSetOfMatcher:
    x = RRangeSizeSetOfMatcher(RSetEnum.SET, value_matcher, min_size=min_size, max_size=max_size)
    return x

def NON_EMPTY_SET_OF(value_matcher: RAbstractTypeMatcher) -> RRangeSizeSetOfMatcher:
    x = RRangeSizeSetOfMatcher(RSetEnum.SET, value_matcher, min_size=1, max_size=-1)
    return x

__BUILTIN_DICT = RDictMatcher(RDictEnum.BUILTIN_DICT)

def BUILTIN_DICT() -> RDictMatcher:
    return __BUILTIN_DICT

def BUILTIN_DICT_OF(*,
                    key_matcher: RAbstractTypeMatcher=None,
                    value_matcher: RAbstractTypeMatcher=None) \
        -> RDictWhereMatcher:
    x = RDictOfMatcher(RDictEnum.BUILTIN_DICT, key_matcher=key_matcher, value_matcher=value_matcher)
    return x

def RANGE_SIZE_BUILTIN_DICT(*, min_size: int=-1, max_size: int=-1) -> RRangeSizeDictMatcher:
    x = RRangeSizeDictMatcher(RDictEnum.BUILTIN_DICT, min_size=min_size, max_size=max_size)
    return x

__NON_EMPTY_BUILTIN_DICT = RRangeSizeDictMatcher(RDictEnum.BUILTIN_DICT, min_size=1)

def NON_EMPTY_BUILTIN_DICT() -> RRangeSizeDictMatcher:
    return __NON_EMPTY_BUILTIN_DICT

def RANGE_SIZE_BUILTIN_DICT_OF(*,
                               key_matcher: RAbstractTypeMatcher=None,
                               value_matcher: RAbstractTypeMatcher=None,
                               min_size: int=-1, max_size: int=-1) -> RRangeSizeDictOfMatcher:
    x = RRangeSizeDictOfMatcher(RDictEnum.BUILTIN_DICT,
                                key_matcher=key_matcher,
                                value_matcher=value_matcher,
                                min_size=min_size,
                                max_size=max_size)
    return x

def NON_EMPTY_BUILTIN_DICT_OF(*,
                              key_matcher: RAbstractTypeMatcher=None,
                              value_matcher: RAbstractTypeMatcher=None) -> RRangeSizeDictOfMatcher:
    x = RRangeSizeDictOfMatcher(RDictEnum.BUILTIN_DICT,
                                key_matcher=key_matcher,
                                value_matcher=value_matcher,
                                min_size=1)
    return x

def BUILTIN_DICT_WHERE_AT_LEAST(matcher_dict: dict) -> RDictWhereMatcher:
    x = RDictWhereMatcher(RDictEnum.BUILTIN_DICT, matcher_dict, is_exact=False)
    return x

def BUILTIN_DICT_WHERE_EXACTLY(matcher_dict: dict) -> RDictWhereMatcher:
    x = RDictWhereMatcher(RDictEnum.BUILTIN_DICT, matcher_dict, is_exact=True)
    return x

__TRACEBACK = RInstanceMatcher(types.TracebackType)

def TRACEBACK() -> RInstanceMatcher:
    return __TRACEBACK

__FRAME = RInstanceMatcher(types.FrameType)

def FRAME() -> RInstanceMatcher:
    return __FRAME

# __CAN_WRITE = RAttrMatcher(RTokenText("write"))
#
# def CAN_WRITE() -> RAttrMatcher:
#     return __CAN_WRITE
