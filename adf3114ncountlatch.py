from adf3114register import *

# 0000_0000_0000_0000_0000_00xx
# for b(ab) counter latch mode must be (0, 1)
CONTROL_BITS = (DB1, DB0)

# 0000_0000_0000_0000_xxxx_xx00   --   counter operation
# A6 | A5 | ... | A2 | A1   divide ratio
#  0    0   ...    0    0   0
#  0    0   ...    0    1   1
#  0    0   ...    1    0   2
#  .    .   ...    .    .   .
#  1    1   ...    1    0   62
#  1    1   ...    1    1   63
A6, A5, A4, A3, A2, A1 = DB7, DB6, DB5, DB4, DB3, DB2
A_COUNTER_BITS = (A6, A5, A4, A3, A2, A1)

# 000x_xxxx_xxxx_xxxx_0000_0000   --   counter operation
# B13 | B13 | ... | B2 | B1   divide ratio
#  0     0    ...    0    0   N/A
#  0     0    ...    0    1   N/A
#  0     0    ...    1    0   N/A
#  0     0    ...    1    1   3
#  .     .    ...    .    .   .
#  1     1    ...    1    0   8190
#  1     1    ...    1    1   8191
B13, B12, B11, B10, B9, B8, B7, B6, B5, B4, B3, B2, B1 = DB20, DB19, DB18, DB17, DB16, DB15, DB14, DB13, DB12, DB11, DB10, DB9, DB8
B_COUNTER_BITS = (B13, B12, B11, B10, B9, B8, B7, B6, B5, B4, B3, B2, B1)

# 00x0_0000_0000_0000_0000_0000   --   CP gain (depends on F4 of function latch)
# F4 | G1   operation
#  0   0    0=charge pump current setting 1 is permanently used
#  0   1    1=charge pump current setting 2 is permanently used
#  1   0    2=charge pump current setting 1 is used
#  1   1    3=charge pump is switched to setting 2; the time spent in setting 2 depends on fastlock mode (see function latch)
G1 = DB21
CP_GAIN_BITS = (G1, )
CP_GAIN_MODE = {
    0: [0],
    1: [1],
    2: [0],
    3: [1]
}
cp_gain_mode_labels = {
    0: ('Setting 1 perm', 'Charge pump current setting 1 is permanently used.'),
    1: ('Setting 2 perm', 'Charge pump current setting 2 is permanently used.'),
    2: ('Setting 1', 'Charge pump current setting 1 is used.'),
    3: ('Switch to setting 2', 'Charge pump is switched to setting 2. The time spent in setting 2 depends on fastlock mode (see function latch).')
}

# xx00_0000_0000_0000_0000_0000   --   reserved


class Adf3114NcountLatch(Adf3114Register):

    def __init__(self, bits=0):
        super().__init__(bits=bits)

        self.unset_nth_bit(CONTROL_BITS[0])
        self.set_nth_bit(CONTROL_BITS[1])

    @property
    def a_counter(self):
        return int(''.join([str(bit) for bit in self.nth_bits(A_COUNTER_BITS)]), 2)

    @a_counter.setter
    def a_counter(self, value: int):
        if not 0 <= value < 64:
            raise ValueError('Incorrect a counter value.')
        bits = [int(bit) for bit in f'{value:06b}']
        mapping = {value: bits}
        self.set_bit_pattern(value, A_COUNTER_BITS, mapping)

    @property
    def b_counter(self):
        return int(''.join([str(bit) for bit in self.nth_bits(B_COUNTER_BITS)]), 2)

    @b_counter.setter
    def b_counter(self, value: int):
        if not 2 < value < 8192:
            raise ValueError('Incorrect b counter value.')
        bits = [int(bit) for bit in f'{value:013b}']
        mapping = {value: bits}
        self.set_bit_pattern(value, B_COUNTER_BITS, mapping)

    @property
    def cp_gain(self):
        return self._find_seq(CP_GAIN_BITS, CP_GAIN_MODE)

    @cp_gain.setter
    def cp_gain(self, code):
        if code not in CP_GAIN_MODE:
            raise ValueError('Incorrect CP gain mode.')
        self.set_bit_pattern(code, CP_GAIN_BITS, CP_GAIN_MODE)

