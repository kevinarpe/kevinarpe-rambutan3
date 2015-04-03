import inspect
import types
from rambutan3 import RArgs
from rambutan3.types import RTypes
from rambutan3.types.matcher.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.types.matcher.RInstanceMatcher import RInstanceMatcher


class RFunctionSignatureMatcher(RInstanceMatcher):

    def __init__(self, param_matcher_list: tuple, opt_return_matcher: RAbstractTypeMatcher):
        """
        :param param_matcher_list: list of RAbstractValueChecker
        :param opt_return_matcher: if None, this is a subroutine, not a function
        """
        super().__init__(*(RTypes.FUNCTION_TYPE_TUPLE()))
        RArgs.check_not_none(param_matcher_list, "param_matcher_list")
        for index, param_matcher in enumerate(param_matcher_list):
            RArgs.check_is_instance(param_matcher, RAbstractTypeMatcher, "param_matcher_list[{}]", index)
        if opt_return_matcher is not None:
            RArgs.check_is_instance(opt_return_matcher, RAbstractTypeMatcher, "opt_return_matcher")
        self.__param_matcher_list = param_matcher_list
        self.__opt_return_matcher = opt_return_matcher

    def matches(self, func: RTypes.FUNCTION_TYPE_TUPLE()) -> bool:
        if not super().matches(func):
            return False
        #: :type: Signature
        sig = inspect.signature(func)
        #: :type: dict of (str, Parameter)
        name_to_param_dict = sig.parameters
        if len(name_to_param_dict) != len(self.__param_matcher_list):
            return False
        #: :type index: int
        #: :type param: Parameter
        for index, param in enumerate(name_to_param_dict.values()):
            actual_matcher = param.annotation
            #: :type: RAbstractTypeMatcher
            expected_matcher = self.__param_matcher_list[index]
            if not expected_matcher.contains(actual_matcher):
                return False
        x = self.__contains_opt_return_matcher(sig.return_annotation)
        return x

    def contains(self, matcher) -> bool:
        if not isinstance(matcher, type(self)):
            return False
        #: :type matcher: RFunctionSignatureMatcher
        if len(self.__param_matcher_list) != len(matcher.__param_matcher_list):
            return False
        for mine, other in zip(self.__param_matcher_list, matcher.__param_matcher_list):
            if not mine.contains(other):
                return False
        x = self.__contains_opt_return_matcher(matcher.__opt_return_matcher)
        return x

    def __contains_opt_return_matcher(self, opt_return_matcher) -> bool:
        """ Gracefully handle if either return matcher is None """
        if opt_return_matcher is not None and self.__opt_return_matcher is not None:
            if not self.__opt_return_matcher.contains(opt_return_matcher):
                return False
        else:
            # False if exactly one has return annotation.
            x = (opt_return_matcher is None) != (self.__opt_return_matcher is None)
            return x
