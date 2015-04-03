from rambutan3 import RArgs
from rambutan3.types.matcher.range.RRangeBoundFunction_ import RRangeBoundFunction_


class RRangeBound_:
    """
    This class exists only to be used by matchers.
    """

    def __init__(self, func: RRangeBoundFunction_):
        RArgs.check_is_instance(func, RRangeBoundFunction_, "func")
        self.__func = func

    def __contains__(self, item) -> bool:
        """ This is the membership operator: in """
        RArgs.check_not_none(item, "item")
        if isinstance(item, type(self)):
            x = item in self.__func
        else:
            x = self.__func(item)
        return x

    def __str__(self):
        x = str(self.__func)
        return x
