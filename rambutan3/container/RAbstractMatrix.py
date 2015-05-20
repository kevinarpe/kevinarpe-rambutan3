from abc import ABC, abstractmethod

from rambutan3.check_args.RCheckArgs import check_args
from rambutan3.check_args.annotation.ANY import ANY
from rambutan3.check_args.annotation.NON_NEGATIVE_INT import NON_NEGATIVE_INT


# Unmodifiable or ReadOnly; FixedSize; () or ReadWrite
from rambutan3.check_args.annotation.SELF import SELF


class RAbstractMatrix(ABC):

    @property
    @abstractmethod
    def row_count(self: SELF()) -> NON_NEGATIVE_INT:
        pass

    @property
    @abstractmethod
    def column_count(self: SELF()) -> NON_NEGATIVE_INT:
        pass

    @check_args
    def get_data(self: SELF(), *, row_index: NON_NEGATIVE_INT, column_index: NON_NEGATIVE_INT) -> ANY:
        try:
            x = self._get_data(row_index=row_index, column_index=column_index)
            return x
        except IndexError:
            self._check_row_index(row_index)
            self._check_column_index(column_index)

    def _check_row_index(self: SELF(), row_index: NON_NEGATIVE_INT):
        row_count = self.row_count
        if row_index >= row_count:
            raise IndexError("row_index({}) >= row_count({})".format(row_index, row_count))

    def _check_column_index(self: SELF(), column_index: NON_NEGATIVE_INT):
        column_count = self.column_count
        if column_index >= column_count:
            raise IndexError("column_index({}) >= column_count({})".format(column_index, column_count))

    @abstractmethod
    def _get_data(self: SELF(), *, row_index: NON_NEGATIVE_INT, column_index: NON_NEGATIVE_INT) -> ANY:
        pass
