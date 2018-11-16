from adf3114registerbase import *
from PyQt5.QtWidgets import QGroupBox, QComboBox, QFormLayout
from spinslide import SpinSlide

# map latch bits onto register bits
_, DLY, SYNC, LDP, T2, T1, ABP2, ABP1, R14, R13, R12, R11, R10, R9, R8, R7, R6, R5, R4, R3, R2, R1, C2, C1 = \
    DB23, DB22, DB21, DB20, DB19, DB18, DB17, DB16, DB15, DB14, DB13, DB12, DB11, DB10, DB9, DB8, DB7, DB6, DB5, DB4, DB3, DB2, DB1, DB0

# 0000_0000_0000_0000_0000_00xx
# for reference counter latch mode must be (0, 0)
CONTROL_BITS = (C2, C1)

# 0000_0000_xxxx_xxxx_xxxx_xx00   --   counter operation
# R14 | R13 | ... | R2 | R1   divide ratio
#  0     0    ...    0    1   1
#  0     0    ...    1    0   2
#  0     0    ...    1    1   3
#  .     .    ...    .    .   .
#  1     1    ...    1    0   16382
#  1     1    ...    1    1   16383
REFCOUNTER_BITS = (R14, R13, R12, R11, R10, R9, R8, R7, R6, R5, R4, R3, R2, R1)

# 0000_00xx_0000_0000_0000_0000   --   antibacklash pulse width
#  ABP2 | ABP1
#    0      0     0=3.0 ns
#    0      1     1=1.5 ns
#    1      0     2=6.5 ns
#    1      1     3=3.0 ns
ANTIBACKLASH_PULSE_WIDTH_BITS = (ABP2, ABP1)
ANTIBACKLASH_PULSE_WIDTH = {
    0: [0, 0],
    1: [0, 1],
    2: [1, 0],
    3: [1, 1]
}
antibacklash_pulse_width_labels = {
    0: '3.0 нс',
    1: '1.5 нс',
    2: '6.5 нс',
    3: '3.0 нс'
}

# 0000_xx00_0000_0000_0000_0000   --   test mode
# T2 | T1   should be (0, 0) for normal operation
TEST_MODE_BITS = (T2, T1)
TEST_MODE = {}

# 000x_0000_0000_0000_0000_0000   --   lock detect precision
# LPD
#  0   0=3 consecutive cycles of phase delay less than 16ns must occur before lock detect is set
#  1   1=5 consecutive cycles of phase delay less than 16ns must occur before lock detect is set
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
SYNC_MODE_BITS = (DLY, SYNC)
SYNC_MODE = {
    0: [0, 0],
    1: [0, 1],
    2: [1, 0],
    3: [1, 1]
}

# x000_0000_0000_0000_0000_0000   --   reserved


class Adf3114RefcountLatch(Adf3114RegisterBase):

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


class Adf3114RefcountLatchWidget(QGroupBox):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setTitle('Reference count latch')
        self.setCheckable(True)
        self.setChecked(True)

        self._slideRefcount = SpinSlide(1, 16380, 1, '')
        self._comboAntibacklash = QComboBox()
        self._comboLockDetectPrec = QComboBox()
        self._comboSync = QComboBox()

        self._layout = QFormLayout(parent=self)
        self._layout.addRow('Reference counter', self._slideRefcount)
        self._layout.addRow('Anti-backlash pulse width', self._comboAntibacklash)
        self._layout.addRow('Lock detection precision', self._comboLockDetectPrec)
        self._layout.addRow('Prescaler sync', self._comboSync)



