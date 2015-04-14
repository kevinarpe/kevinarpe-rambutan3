from rambutan3.container.RDict import RDict
from rambutan3.container.RForwardingUnmodifiableDict import RForwardingUnmodifiableDict
from rambutan3.type.matcher.RCheckArgs import check_args
from rambutan3.type.matcher.annotation.DICT import DICT
from rambutan3.type.matcher.annotation.INSTANCE_OF import INSTANCE_OF
from rambutan3.type.matcher.annotation.SELF import SELF


class RUnmodifiableDictView(RForwardingUnmodifiableDict):

    @check_args
    def __init__(self: SELF(), delegate_dict: DICT | INSTANCE_OF(RDict)):
        self.__dict = delegate_dict

    @property
    def _delegate(self) -> dict:
        return self.__dict
