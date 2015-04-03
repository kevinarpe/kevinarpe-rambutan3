from rambutan3 import RArgs
from rambutan3.types.matcher.RInstanceMatcher import RInstanceMatcher
from rambutan3.types.matcher.range.RRange_ import RRange_

RNumberRangeMatcher = None
class RNumberRangeMatcher(RInstanceMatcher):

    def __init__(self,
                 class_or_type_tuple: tuple,
                 bound_op1: str,
                 value1: (int, float),
                 bound_op2: str=None,
                 value2: (int, float)=None):
        RArgs.check_is_instance(class_or_type_tuple, tuple, "class_or_type_tuple")
        super().__init__(*class_or_type_tuple)
        RArgs.check_is_instance(value1, class_or_type_tuple, "value1")
        if value2:
            RArgs.check_is_instance(value2, class_or_type_tuple, "value2")
        self.__range = RRange_.create(bound_op1, value1, bound_op2, value2)

    # @override
    def matches(self, value: (int, float)) -> bool:
        x = super().matches(value) and value in self.__range
        return x

    def contains(self, matcher: RNumberRangeMatcher) -> bool:
        x = super().contains(matcher) and matcher.__range in self.__range
        return x

    # @override
    def _str(self):
        x = "{}: {}".format(super()._str(), self.__range)
        return x
