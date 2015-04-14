from rambutan3.container.RForwardingUnmodifiableSet import RForwardingUnmodifiableSet
from rambutan3.container.RSet import RSet
from rambutan3.type.matcher.RCheckArgs import check_args
from rambutan3.type.matcher.annotation.INSTANCE_OF import INSTANCE_OF
from rambutan3.type.matcher.annotation.SELF import SELF
from rambutan3.type.matcher.annotation.SET import SET


class RUnmodifiableSetView(RForwardingUnmodifiableSet):

    @check_args
    def __init__(self: SELF(), delegate_set: SET | INSTANCE_OF(RSet)):
        self.__set = delegate_set

    @property
    def _delegate(self) -> set:
        return self.__set
