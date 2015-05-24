import enum

import pytest

from rambutan3.enumeration.REnum import REnum


def test():
    with pytest.raises(ValueError):
        @enum.unique
        class _NonUniqueEnum(REnum):
            A = 1
            B = 1
