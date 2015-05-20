from rambutan3.check_args.RCheckArgs import check_args
from rambutan3.check_args.annotation.MESSAGE_TEXT import MESSAGE_TEXT
from rambutan3.check_args.annotation.NON_EMPTY_SEQUENCE import NON_EMPTY_SEQUENCE
from rambutan3.check_args.annotation.NOT_NONE import NOT_NONE
from rambutan3.check_args.annotation.NON_EMPTY_SEQUENCE_OF import NON_EMPTY_SEQUENCE_OF
from rambutan3.check_args.annotation.NON_NEGATIVE_INT import NON_NEGATIVE_INT
from rambutan3.check_args.annotation.SELF import SELF
from rambutan3.container.RAbstractTable import RAbstractTable


class RRowTupleTable(RAbstractTable):

    def __init__(self: SELF(), header_list: NON_EMPTY_SEQUENCE_OF(MESSAGE_TEXT)):
        super().__init__(header_list)
        self.__row_tuple_list = []

    @check_args
    def append_row(self: SELF(), row_seq: NON_EMPTY_SEQUENCE):
        column_count = self.column_count
        if (0 != column_count) and (len(row_seq) != column_count):
            raise ValueError("len(row_seq) != self.column_count: {} != {}".format(len(row_seq), column_count))

        self.__row_tuple_list.append(tuple(row_seq))

    # @overrides
    @property
    def row_count(self) -> NON_NEGATIVE_INT:
        x = len(self.__row_tuple_list)
        return x

    # @overrides
    def _get_data(self, *, row_index: NON_NEGATIVE_INT, column_index: NON_NEGATIVE_INT) -> NOT_NONE:
        if row_index >= len(self.__row_tuple_list):
            raise IndexError("row_index({}) >= row_count({})".format(row_index, len(self.__row_tuple_list)))

        row_tuple = self.__row_tuple_list[row_index]
        if column_index >= len(row_tuple):
            raise IndexError("column_index({}) >= column_count({})".format(column_index, len(row_tuple)))

        x = row_tuple[column_index]
        return x
