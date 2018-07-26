import sys

def argv0(num):
    v = num * 100
    if v % 100 == 0:
        for index in range(0,20):
            num /= 5
    print(str(v))


def main(argv):
    if len(argv) == 0:
        n_to_check = 153
    else:
        n_to_check = int(argv[0])

    argv0(n_to_check)


if __name__ == "__main__":
    main(sys.argv[1:])
