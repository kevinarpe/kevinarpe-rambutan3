from rambutan3 import RArgs
from rambutan3.types.matcher.RInstanceMatcher import RInstanceMatcher


class RRangeSizeCollectionMatcher(RInstanceMatcher):

    def __init__(self, class_or_type_tuple: tuple, *, min_size: int=-1, max_size: int=-1):
        RArgs.check_is_instance(class_or_type_tuple, tuple, "class_or_type_tuple")
        super().__init__(*class_or_type_tuple)
        RArgs.check_is_instance(min_size, int, "min_size")
        RArgs.check_is_instance(max_size, int, "max_size")
        if -1 == min_size and -1 == max_size:
            raise ValueError("Both args 'min_size' and 'max_size' are -1")
        if min_size < -1:
            raise ValueError("Arg 'min_size' must be >= -1: {}".format(min_size))
        if max_size < -1:
            raise ValueError("Arg 'max_size' must be >= -1: {}".format(max_size))
        self.__min_size = min_size
        self.__max_size = max_size

    # @override
    def matches(self, seq) -> bool:
        if not super().matches(seq):
            return False
        L = len(seq)
        if -1 != self.__min_size and L < self.__min_size:
            return False
        if -1 != self.__max_size and L > self.__max_size:
            return False
        return True

    # @override
    def _str(self):
        suffix = ""
        if -1 != self.__min_size:
            suffix = "size >= {}".format(self.__min_size)
        if -1 != self.__max_size:
            if suffix:
                suffix += " and "
            suffix = "size <= {}".format(self.__max_size)
        x = super()._str() + " where " + suffix
        return x
