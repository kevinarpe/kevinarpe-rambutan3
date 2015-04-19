from abc import abstractmethod, ABCMeta

from bin import Sample
from rambutan3.check_args.RCheckArgs import check_args
from rambutan3.check_args.annotation.FUNC import FUNC
from rambutan3.string.RMessageText import RMessageText


class X(metaclass=ABCMeta):
    def __eq__(self, other):
        x = (self == other)
        return x

    def __hash__(self):
        x = id(self)
        return x

#    @abstractmethod
    def __str__(self):
        pass


class Y(X):

    def __hash__(self):
        x = super().__hash__()
#        y = hash(self)
        s = super()
        z = hash(s)
        z2 = hash(super())
        return x


@check_args
def overrides(func: FUNC) -> FUNC:
    func.__overrides__ = True
    return func


class RAbstractBaseClassMeta(ABCMeta):
    # noinspection PyMethodParameters
    def __new__(mcls, name, bases, namespace):
            x = super().__new__(mcls, name, bases, namespace)
            return x


class RAbstractBaseClass(metaclass=RAbstractBaseClassMeta):
    pass


class AbstractClass(RAbstractBaseClass):
    @abstractmethod
    def f(self):
        pass


# noinspection PyAbstractClass
class Z(AbstractClass):
    @overrides
    def f2(self):
        print("f()")


def main():
    msg = RMessageText("abc")
    msg_iter = iter(msg)
    for char in msg_iter:
        pass
    for char in msg:
        pass
    Z().f2()

    x_hash = hash(X())
    y_hash = hash(Y())
    print(Sample.MAYBE_CONST)
    Sample.MAYBE_CONST = 456
    print(Sample.MAYBE_CONST)

if __name__ == "__main__":
    main()
