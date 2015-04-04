from abc import abstractmethod, ABCMeta
from bin import Sample


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

def main():
    x_hash = hash(X())
    y_hash = hash(Y())
    print(Sample.MAYBE_CONST)
    Sample.MAYBE_CONST = 456
    print(Sample.MAYBE_CONST)

if __name__ == "__main__":
    main()
