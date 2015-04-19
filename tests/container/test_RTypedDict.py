import pytest
from rambutan3.check_args.annotation.INT import INT
from rambutan3.check_args.error.RCheckArgsError import RCheckArgsError
from rambutan3.container.RTypedDict import RTypedDict


def test():
    with pytest.raises(ValueError):
        RTypedDict()

    RTypedDict(key_matcher=INT, dictionary={123: "abc", 456: 789})

    with pytest.raises(RCheckArgsError):
        RTypedDict(key_matcher=INT, dictionary={123: "abc", 456: 789, None: None})

    RTypedDict(value_matcher=INT, dictionary={"abc": 123, 456: 789})

    with pytest.raises(RCheckArgsError):
        RTypedDict(value_matcher=INT, dictionary={"abc": 123, 456: 789, None: None})
