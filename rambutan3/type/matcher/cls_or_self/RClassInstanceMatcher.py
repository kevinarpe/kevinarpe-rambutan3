from rambutan3.type.matcher.cls_or_self import RAbstractClassOrSelfInstanceMatcher


RClassInstanceMatcher = None
class RClassInstanceMatcher(RAbstractClassOrSelfInstanceMatcher):

    def __init__(self):
        super().__init__()

    # @override
    def matches(self, value) -> bool:
        x = isinstance(type(value), self._caller_class)
        return x

    # @override
    def __str__(self):
        x = "cls: {}".format(self._caller_class.__name__)
        return x
