from rambutan3.type.matcher.cls_or_self.RAbstractClassOrSelfInstanceMatcher import RAbstractClassOrSelfInstanceMatcher


RSelfInstanceMatcher = None
class RSelfInstanceMatcher(RAbstractClassOrSelfInstanceMatcher):

    def __init__(self):
        super().__init__()

    # @override
    def matches(self, value) -> bool:
        x = isinstance(value, self._caller_class)
        return x

    # @override
    def __str__(self):
        x = "self: {}".format(self._caller_class.__name__)
        return x