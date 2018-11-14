import sys

from adf3114register import Adf3114Register
from adf3114initlatch import Adf3114InitLatch


def main(argv):
    pass


if __name__ == '__main__':
    main(sys.argv)

    reg = Adf3114InitLatch()
    print(reg)
    reg.power_down_mode = 1
    print(reg)
    reg.power_down_mode = 2
    print(reg)
    reg.power_down_mode = 3
    print(reg)
