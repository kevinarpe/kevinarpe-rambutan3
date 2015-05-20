from rambutan3.check_args.RCheckArgs import check_args
from rambutan3.check_args.annotation.MESSAGE_TEXT import MESSAGE_TEXT
from rambutan3.check_args.annotation.NON_EMPTY_SEQUENCE_OF import NON_EMPTY_SEQUENCE_OF
from rambutan3.check_args.annotation.NON_NEGATIVE_INT import NON_NEGATIVE_INT
from rambutan3.check_args.annotation.SELF import SELF
from rambutan3.container.RAbstractMatrix import RAbstractMatrix


# noinspection PyAbstractClass
class RAbstractTable(RAbstractMatrix):

    @check_args
    def __init__(self: SELF(), header_list: NON_EMPTY_SEQUENCE_OF(MESSAGE_TEXT)):
        """:type header_list: list[str]"""
        super().__init__()
        self.__header_list = header_list

    @check_args
    def get_header(self: SELF(), *, column_index: NON_NEGATIVE_INT) -> MESSAGE_TEXT:
        try:
            x = self.__header_list[column_index]
            return x
        except IndexError:
            self._check_column_index(column_index)

    # @overrides
    @property
    def column_count(self: SELF()) -> NON_NEGATIVE_INT:
        x = len(self.__header_list)
        return x
