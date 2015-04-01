from rambutan3.types.RDelegator import RDelegator
from rambutan3 import RArgs


class RStringDelegator(RDelegator):
    """
    Delegates all methods to underlying {@link str} value.

    @author Kevin Connor ARPE (kevinarpe@gmail.com)
    """

    def __init__(self, value: str):
        RArgs.check_is_instance(value, str, "value")
        super().__init__(value)

    @property
    def str(self) -> str:
        """
        @return underlying {@link str} value
        """
        x = self._super_getattribute("__delegate")
        return x
