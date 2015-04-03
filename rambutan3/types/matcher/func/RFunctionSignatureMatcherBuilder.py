from rambutan3 import RArgs
from rambutan3.types.matcher.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.types.matcher.func.RFunctionSignatureMatcher import RFunctionSignatureMatcher


class RFunctionSignatureMatcherBuilder:

    def __init__(self, *matcher_tuple):
        for index, value in enumerate(matcher_tuple):
            RArgs.check_is_instance(value, RAbstractTypeMatcher, "Arg#{}", 1 + index)
        self.__matcher_tuple = matcher_tuple

    def returns(self, opt_return_matcher: RAbstractTypeMatcher) -> RFunctionSignatureMatcher:
        x = RFunctionSignatureMatcher(param_matcher_list=self.__matcher_tuple,
                                      opt_return_matcher=opt_return_matcher)
        return x
