import sys

def argv0(num):
    v = num * 100
    if v % 100 == 0:
        for index in range(0,20):
            num /= 5
    print(str(v))


def main(argv):
    if len(argv) == 0:
        argv0(10)


if __name__ == "__main__":
    main(sys.argv[1:])
