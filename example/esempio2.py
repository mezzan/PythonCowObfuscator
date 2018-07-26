import sys


def armstrong_number(num):
    s = 0
    temp = num
    while temp > 0:
       digit = temp % 10
       s += digit ** 3
       temp //= 10

    if num == s:
       return True
    else:
      return False

def main(argv):
    if len(argv) == 0:
        n_to_check = 153
    else:
        n_to_check = int(argv[0])

    res = armstrong_number(n_to_check)
    if res == True:
        print('Yes')
    else:
        print('No')


if __name__ == "__main__":
    main(sys.argv[1:])
