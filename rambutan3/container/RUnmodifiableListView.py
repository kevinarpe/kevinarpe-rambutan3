from rambutan3.container.RForwardingUnmodifiableList import RForwardingUnmodifiableList
from rambutan3.container.RList import RList
from rambutan3.type.matcher.RCheckArgs import check_args
from rambutan3.type.matcher.annotation.INSTANCE_OF import INSTANCE_OF
from rambutan3.type.matcher.annotation.SELF import SELF
from rambutan3.type.matcher.annotation.SEQUENCE import SEQUENCE


class RUnmodifiableListView(RForwardingUnmodifiableList):

    @check_args
    def __init__(self: SELF(), delegate_list: SEQUENCE | INSTANCE_OF(RList)):
        self.__list = delegate_list

    @property
    def _delegate(self) -> list:
        return self.__list
