from adf3114register import *

# 0000_0000_0000_0000_0000_00xx
# в режиме initialization latch должны = 1, 1
CONTROL_BITS = (DB1, DB0)

# 0000_0000_0000_0x00   --   counter operation
# F1
#  0   0=normal
#  1   1=R,A,B counters held in reset
F1 = DB2
COUNTER_RESET_BITS = (F1,)
COUNTER_RESET_MODE = {
    0: [0],
    1: [1]
}

# 00x0_0000_0000_0000_0000_x000   --   power-down mode
# CE pin | PD2 | PD1
#    0      x     x   0=async power-down
#    1      x     0   1=normal operation
#    1      0     1   2=async power-down
#    1      1     1   3=sync power-down
PD2, PD1 = DB21, DB3
POWER_DOWN_BITS = (PD2, PD1)
POWER_DOWN_MODE = {
    0: [0, 0],
    1: [0, 0],
    2: [0, 1],
    3: [1, 1]
}

# 0000_0000_0000_0000_0xxx_0000   --   muxout control
# M3 | M2 | M1
#  0    0    0   0=three-state output
#  0    0    1   1=digital lock detect (active high)
#  0    1    0   2=N divider output
#  0    1    1   3=DVdd
#  1    0    0   4=R divider output
#  1    0    1   5=analog lock detect (n-channel open-drain)
#  1    1    0   6=serial data output
#  1    1    1   7=DGND
M3, M2, M1 = DB6, DB5, DB4
MUXOUT_BITS = (M3, M2, M1)
MUXOUT_MODE = {
    0: [0, 0, 0],
    1: [0, 0, 1],
    2: [0, 1, 0],
    3: [0, 1, 1],
    4: [1, 0, 0],
    5: [1, 0, 1],
    6: [1, 1, 0],
    7: [1, 1, 1],
}

# 0000_0000_0000_0000_x000_0000   --   phase detector polarity
# F2
#  0   0=negative
#  1   1=positive
#
F2 = DB7
PD_POLARITY_BITS = (F2, )
PD_POLARITY = {
    0: [0],
    1: [1]
}


class Adf3114InitLatch(Adf3114Register):

    def __init__(self, bits=0):
        super().__init__(bits=bits)

        self.set_bits(CONTROL_BITS)

    @property
    def counter_reset(self):
        return self._find_seq(COUNTER_RESET_BITS, COUNTER_RESET_MODE)

    @counter_reset.setter
    def counter_reset(self, state):
        if state not in COUNTER_RESET_MODE:
            raise ValueError('Incorrect counter state.')
        self.set_bit_pattern(state, COUNTER_RESET_BITS, COUNTER_RESET_MODE)

    @property
    def power_down_mode(self):
        return self._find_seq(POWER_DOWN_BITS, POWER_DOWN_MODE)

    @power_down_mode.setter
    def power_down_mode(self, mode: int):
        if mode not in POWER_DOWN_MODE:
            raise ValueError('Incorrect power down mode.')
        self.set_bit_pattern(mode, POWER_DOWN_BITS, POWER_DOWN_MODE)

    @property
    def muxout_control(self):
        return self._find_seq(MUXOUT_BITS, MUXOUT_MODE)

    @muxout_control.setter
    def muxout_control(self, code: int):
        if code not in MUXOUT_MODE:
            raise ValueError('Incorrect muxout control code.')
        self.set_bit_pattern(code, MUXOUT_BITS, MUXOUT_MODE)

    @property
    def phase_detector_polarity(self):
        return self._find_seq(PD_POLARITY_BITS, PD_POLARITY)

    @phase_detector_polarity.setter
    def phase_detector_polarity(self, code):
        if code not in PD_POLARITY:
            raise ValueError('Incorrect phase detector polarity code.')
        self.set_bit_pattern(code, PD_POLARITY_BITS, PD_POLARITY)


