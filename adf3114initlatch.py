from adf3114register import *

# 0000_0000_0000_00xx
# в режиме initialization latch должны = 1, 1
CONTROL_BIT_1 = DB0
CONTROL_BIT_2 = DB1

# 0000_0000_0000_0x00   --   counter operation
# 0=normal
# 1=R,A,B counters held in reset
COUNTER_RESET = DB2
COUNTER_RESET_MODE = {
    0: [0],
    1: [1]
}

# 00x0_0000_0000_x000   --   power-down mode
# CE pin | PD2 | PD1
#    0      x     x   0=async power-down
#    1      x     0   1=normal operation
#    1      0     1   2=async power-down
#    1      1     1   3=sync power-down
POWER_DOWN_1 = PD1 = DB3
POWER_DOWN_2 = PD2 = DB21
POWER_DOWN_MODE = {
    0: [0, 0],
    1: [0, 0],
    2: [0, 1],
    3: [1, 1]
}

# 0000_0000_0xxx_0000   --   muxout control
# M3 | M2 | M1
#  0    0    0   0=three-state output
#  0    0    1   1=digital lock detect (active high)
#  0    1    0   2=N divider output
#  0    1    1   3=DVdd
#  1    0    0   4=R divider output
#  1    0    1   5=analog lock detect (n-channel open-drain)
#  1    1    0   6=serial data output
#  1    1    1   7=DGND
MUXOUT_1 = M1 = DB4
MUXOUT_2 = M2 = DB5
MUXOUT_3 = M3 = DB6
MUXOUT_CONTROL = {
    0: [0, 0, 0],
    1: [0, 0, 1],
    2: [0, 1, 0],
    3: [0, 1, 1],
    4: [1, 0, 0],
    5: [1, 0, 1],
    6: [1, 1, 0],
    7: [1, 1, 1],
}


class Adf3114InitLatch(Adf3114Register):

    def __init__(self, bits=0):
        super().__init__(bits=bits)

        self.set_bits([CONTROL_BIT_1, CONTROL_BIT_2])

    @property
    def counter_reset(self):
        return self.nth_bit(COUNTER_RESET)

    @counter_reset.setter
    def counter_reset(self, state):
        if state not in [0, 1]:
            raise ValueError('Incorrect counter state.')
        if state:
            self.set_nth_bit(COUNTER_RESET)
        else:
            self.unset_nth_bit(COUNTER_RESET)

    @property
    def power_down_mode(self):
        bits = [self.nth_bit(POWER_DOWN_2), self.nth_bit(POWER_DOWN_1)]
        for k, v in POWER_DOWN_MODE.items():
            if v == bits:
                return k
        else:
            raise ValueError('Wrong power-down bit pattern.')

    @power_down_mode.setter
    def power_down_mode(self, mode: int):
        bits = POWER_DOWN_MODE[mode]
        self.set_bit_pattern([[n, bit] for n, bit in zip([PD2, PD1], bits)])

    @property
    def muxout_control(self):
        bits = [self.nth_bit(MUXOUT_3), self.nth_bit(MUXOUT_2), self.nth_bit(MUXOUT_1)]
        for k, v in MUXOUT_CONTROL.items():
            if v == bits:
                return k
        else:
            raise ValueError('Wrong power-down bit pattern.')

    @muxout_control.setter
    def muxout_control(self, mode: int):
        bits = MUXOUT_CONTROL[mode]
        self.set_bit_pattern([[n, bit] for n, bit in zip([M3, M2, M1], bits)])

