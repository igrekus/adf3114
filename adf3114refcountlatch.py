from adf3114register import *

# 0000_0000_0000_0000_0000_00xx
# for reference counter latch mode must be (0, 0)
CONTROL_BITS = (DB1, DB0)

# 0000_0000_xxxx_xxxx_xxxx_xx00   --   counter operation
# R14 | R13 | ... | R2 | R1   divide ratio
#  0     0    ...    0    1   1
#  0     0    ...    1    0   2
#  0     0    ...    1    1   3
#  .     .    ...    .    .   .
#  1     1    ...    1    0   16382
#  1     1    ...    1    1   16383
R14, R13, R12, R11, R10, R9, R8, R7, R6, R5, R4, R3, R2, R1 = DB15, DB14, DB13, DB12, DB11, DB10, DB9, DB8, DB7, DB6, DB5, DB4, DB3, DB2
REFCOUNTER_BITS = (R14, R13, R12, R11, R10, R9, R8, R7, R6, R5, R4, R3, R2, R1)

# 0000_00xx_0000_0000_0000_0000   --   antibacklash pulse width
#  ABP2 | ABP1
#    0      0     0=3.0 ns
#    0      1     1=1.5 ns
#    1      0     2=6.5 ns
#    1      1     3=3.0 ns
ABP2, ABP1 = DB17, DB16
ANTIBACKLASH_PULSE_WIDTH_BITS = (ABP2, ABP1)
ANTIBACKLASH_PULSE_WIDTH = {
    0: [0, 0],
    1: [0, 1],
    2: [1, 0],
    3: [1, 1]
}

# 0000_xx00_0000_0000_0000_0000   --   test mode
# T2 | T1   should be (0, 0) for normal operation
T2, T1 = DB19, DB18
TEST_MODE_BITS = (T2, T1)
TEST_MODE = {}

# 000x_0000_0000_0000_0000_0000   --   lock detect precision
# LPD
#  0   0=3 consecutive cycles of phase delay less than 16ns must occur before lock detect is set
#  1   1=5 consecutive cycles of phase delay less than 16ns must occur before lock detect is set
LDP = DB20
LOCK_DETECT_PREC_BITS = (LDP, )
LOCK_DETECT_PREC = {
    0: [0],
    1: [1]
}

# 0xx0_0000_0000_0000_0000_0000   --   sync mode
# DLY | SYNC
#  0     0   0=normal operation
#  0     1   1=output of prescaler is resynced with nondelayed version of RF input
#  1     0   2=normal operation
#  1     1   2=output of prescaler is resynced with delayed version of RF input
DLY, SYNC = DB22, DB21
SYNC_MODE_BITS = (DLY, SYNC)
SYNC_MODE = {
    0: [0, 0],
    1: [0, 1],
    2: [1, 0],
    3: [1, 1]
}

# x000_0000_0000_0000_0000_0000   --   reserved


class Adf3114RefcountLatch(Adf3114Register):

    def __init__(self, bits=0):
        super().__init__(bits=bits)

        self.unset_bits(CONTROL_BITS)

    @property
    def reference_counter(self):
        return int(''.join([str(bit) for bit in self.nth_bits(REFCOUNTER_BITS)]), 2)

    @reference_counter.setter
    def reference_counter(self, value: int):
        if not 1 < value < 16384:
            raise ValueError('Incorrect antibacklash pulse width.')
        bits = [int(bit) for bit in f'{value:014b}']
        mapping = {value: bits}
        self.set_bit_pattern(value, REFCOUNTER_BITS, mapping)

    @property
    def antibacklash_pulse_width(self):
        return self._find_seq(ANTIBACKLASH_PULSE_WIDTH_BITS, ANTIBACKLASH_PULSE_WIDTH)

    @antibacklash_pulse_width.setter
    def antibacklash_pulse_width(self, code):
        if code not in ANTIBACKLASH_PULSE_WIDTH:
            raise ValueError('Incorrect power down mode.')
        self.set_bit_pattern(code, ANTIBACKLASH_PULSE_WIDTH_BITS, ANTIBACKLASH_PULSE_WIDTH)

    @property
    def lock_detect_precision(self):
        return self._find_seq(LOCK_DETECT_PREC_BITS, LOCK_DETECT_PREC)

    @lock_detect_precision.setter
    def lock_detect_precision(self, code):
        if code not in LOCK_DETECT_PREC:
            raise ValueError('Incorrect power down mode.')
        self.set_bit_pattern(code, LOCK_DETECT_PREC_BITS, LOCK_DETECT_PREC)

    @property
    def sync_mode(self):
        return self._find_seq(SYNC_MODE_BITS, SYNC_MODE)

    @sync_mode.setter
    def sync_mode(self, code):
        if code not in SYNC_MODE:
            raise ValueError('Incorrect power down mode.')
        self.set_bit_pattern(code, SYNC_MODE_BITS, SYNC_MODE)


