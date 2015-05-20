from rambutan3.check_args.annotation.NOT_NONE import NOT_NONE
from rambutan3.check_args.annotation.INSTANCE_OF import INSTANCE_OF
from rambutan3.check_args.annotation.NON_NEGATIVE_INT import NON_NEGATIVE_INT
from rambutan3.container.RAbstractMatrix import RAbstractMatrix


class RTransposedMatrix(RAbstractMatrix):

    def __init__(self, matrix: INSTANCE_OF(RAbstractMatrix)):
        super().__init__()
        self.__matrix = matrix

    def row_count(self) -> NON_NEGATIVE_INT:
        x = self.__matrix.column_count
        return x

    def column_count(self) -> NON_NEGATIVE_INT:
        x = self.__matrix.row_count
        return x

    # @overrides
    def get_data(self, *, row_index: NON_NEGATIVE_INT, column_index: NON_NEGATIVE_INT) -> NOT_NONE:
        x = super().get_data(row_index=column_index, column_index=row_index)
        return x

    # @check_args
    # def __getitem__(self: SELF(), row_column_index_tuple: TUPLE_WHERE_EXACTLY(NON_NEGATIVE_INT, NON_NEGATIVE_INT)) -> ANY:
    #     column_index = row_column_index_tuple[0]
    #     row_index = row_column_index_tuple[1]
    #     x = super().__getitem__(column_index, row_index)
    #     return x