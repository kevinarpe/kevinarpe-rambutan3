from rambutan3.check_args.RCheckArgs import check_args
from rambutan3.check_args.annotation.ANY_VALUE_OF import ANY_VALUE_OF
from rambutan3.check_args.annotation.INSTANCE_OF import INSTANCE_OF
from rambutan3.check_args.annotation.INT import INT
from rambutan3.check_args.annotation.NONE import NONE
from rambutan3.check_args.range.RIntRangeMatcher import RIntRangeMatcher
from rambutan3.check_args.range.RRangeBoundFunctionEnumData_ import RRangeBoundFunctionEnumData_


__RANGE_BOUND_OP1 = ANY_VALUE_OF(*RRangeBoundFunctionEnumData_.ONE_BOUND_OP_STR_SET)
__RANGE_BOUND_OP2 = ANY_VALUE_OF(*RRangeBoundFunctionEnumData_.TWO_BOUND_OP2_STR_SET)


# noinspection PyPep8Naming
@check_args
def INT_RANGE(bound_op1: __RANGE_BOUND_OP1,
              value1: INT,
              bound_op2: __RANGE_BOUND_OP2 | NONE=None,
              value2: INT | NONE=None) \
        -> INSTANCE_OF(RIntRangeMatcher):
    """
    @param bound_op1
           if a single-bound range: any one of '>', '>=', '<', or '<='
           if a dual-bound range: any one of '>' or '>='
    @param value1
           first boundary value, e.g., x > 5, thus {@code value1} is 5
    @param bound_op2
           if a single-bound range: None
           if a dual-bound range: any one of '<' or '<='
    @param value2
           if a single-bound range: None
           if a dual-bound range: second boundary value, e.g., x < 12, thus {@code value2} is 12

    @throws RCheckArgsError
            if any argument is invalid
    """
    x = RIntRangeMatcher(bound_op1, value1, bound_op2, value2)
    return x
