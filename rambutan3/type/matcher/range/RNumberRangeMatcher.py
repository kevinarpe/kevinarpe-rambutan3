from rambutan3 import RArgs
from rambutan3.type.matcher.RInstanceMatcher import RInstanceMatcher
from rambutan3.type.matcher.range.RRange_ import RRange_

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
        if not super().matches(value):
            return False
        x = (value in self.__range)
        return x

    # @override
    def __eq__(self, other: RNumberRangeMatcher) -> bool:
        if not isinstance(other, RNumberRangeMatcher):
            return False
        if not super().__eq__(other):
            return False
        x = (self.__range == other.__range)
        return x

    # @override
    def __hash__(self) -> int:
        # Ref: http://stackoverflow.com/questions/29435556/how-to-combine-hash-codes-in-in-python3
        super_hash = super().__hash__()
        self_hash = hash(self.__range)
        x = super_hash ^ self_hash
        return x

    # @override
    def __str__(self):
        x = "{}: {}".format(super().__str__(), self.__range)
        return x
