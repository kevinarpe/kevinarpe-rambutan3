from bin import Sample


def main():
    print(Sample.MAYBE_CONST)
    Sample.MAYBE_CONST = 456
    print(Sample.MAYBE_CONST)

if __name__ == "__main__":
    main()
