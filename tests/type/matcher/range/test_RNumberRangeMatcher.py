

# TODO: LAST: Finish me
def test_one_bound():
    assert


def test_one_boundXYZ(self):
    self.__test_bound1(RCheckArgs.INT_RANGE('>', 5), [6, 7, 8], is_expected_pass=True)
    self.__test_bound1(RCheckArgs.INT_RANGE('>=', 5), [5, 6, 7, 8], is_expected_pass=True)
    self.__test_bound1(RCheckArgs.INT_RANGE('>', 5), [-1, 0, 5], is_expected_pass=False)
    self.__test_bound1(RCheckArgs.INT_RANGE('>=', 5), [-1, 0, 4], is_expected_pass=False)

def test_two_bound(self):
    self.__test_bound1(RCheckArgs.INT_RANGE('>', 5), [6, 7, 8], is_expected_pass=True)
    self.__test_bound1(RCheckArgs.INT_RANGE('>=', 5), [5, 6, 7, 8], is_expected_pass=True)
    self.__test_bound1(RCheckArgs.INT_RANGE('>', 5), [-1, 0, 5], is_expected_pass=False)
    self.__test_bound1(RCheckArgs.INT_RANGE('>=', 5), [-1, 0, 4], is_expected_pass=False)

def __test_bound1(self, matcher: RIntRangeMatcher, test_value_list: list, is_expected_pass: bool):
    error_value_list = []
    for test_value in test_value_list:
        if is_expected_pass != matcher.matches(test_value):
            error_value_list.append(str(test_value))
    if error_value_list:
        x = ", ".join(error_value_list)
        raise AssertionError("Matcher '{}': Expected {}, but {}: {}"
                             .format(matcher, is_expected_pass, not is_expected_pass, x))
