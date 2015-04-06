from rambutan3.type.matcher.RCheckArgs import check_args
from rambutan3.type.matcher.annotation.ANY_VALUE_OF import ANY_VALUE_OF
from rambutan3.type.matcher.annotation.INT import INT
from rambutan3.type.matcher.annotation.OPT import OPT
from rambutan3.type.matcher.range.RIntRangeMatcher import RIntRangeMatcher
from rambutan3.type.matcher.range.RRangeBoundFunctionEnumData_ import RRangeBoundFunctionEnumData_

__RANGE_BOUND_OP1 = ANY_VALUE_OF(*RRangeBoundFunctionEnumData_.ONE_BOUND_OP_SET)
__RANGE_BOUND_OP2 = ANY_VALUE_OF(*RRangeBoundFunctionEnumData_.TWO_BOUND_OP2_SET)

@check_args
def INT_RANGE(bound_op1: __RANGE_BOUND_OP1,
              value1: INT,
              bound_op2: __RANGE_BOUND_OP2 | OPT=None,
              value2: INT | OPT=None) \
        -> RIntRangeMatcher:
    x = RIntRangeMatcher(bound_op1, value1, bound_op2, value2)
    return x
