from rambutan3 import RArgs
from rambutan3.types.matcher.RAbstractTypeMatcher import RAbstractTypeMatcher, RLogicalOrTypeMatcher


RInstanceMatcher = None
class RInstanceMatcher(RAbstractTypeMatcher):
    """Type instance matcher

    Example: {@code "abc"} has type {@link str}
    Example: {@code 123.456} has type {@link float}

    This class is fully tested.

    @author Kevin Connor ARPE (kevinarpe@gmail.com)

    @see builtins#isinstance()
    """

    def __init__(self, *class_or_type_tuple):
        """
        @param *class_or_type_tuple
               one or more value type classes, e.g., {@link str} or {@link float}

        @throws ValueError
                if {@code *class_or_type_tuple} is empty
        @throws TypeError
                if {@code *class_or_type_tuple} contains a item that is not a type/class
        """
        super().__init__()
        if not class_or_type_tuple:
            raise ValueError("Arg '*class_or_type_tuple' is empty")
        for index, class_or_type in enumerate(class_or_type_tuple):
            RArgs.check_is_instance(class_or_type, type, "Arg#{}", 1 + index)
        self.__class_or_type_tuple = class_or_type_tuple

    # @property
    # def type(self):
    #     return self.__value_type

    # @override
    def matches(self, value) -> bool:
        x = isinstance(value, self.__class_or_type_tuple)
        return x

    # @override
    def _contains(self, matcher: RInstanceMatcher) -> bool:
        # TODO: Something isn't right about this code.  The second block should reversed/delegated somehow...
        if isinstance(matcher, type(self)):
            x = issubclass(matcher.__class_or_type_tuple, self.__class_or_type_tuple)
        elif isinstance(matcher, RLogicalOrTypeMatcher):
            x = any(self.contains(sub_matcher) for sub_matcher in matcher)
        else:
            x = False
        return x

    # @override
    def _str(self):
        x = " | ".join([x.__name__ for x in self.__class_or_type_tuple])
        return x
