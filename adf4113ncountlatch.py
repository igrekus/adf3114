from PyQt5.QtCore import pyqtSignal, pyqtSlot

from bitmodel import BitModel
from mytools.mapmodel import MapModel
from adf4113registerbase import *
from PyQt5.QtWidgets import QGroupBox, QComboBox, QFormLayout, QLineEdit, QTableView, QVBoxLayout, QLabel
from spinslide import SpinSlide

# map latch bits onto register bits
_, _, G1, B13, B12, B11, B10, B9, B8, B7, B6, B5, B4, B3, B2, B1, A6, A5, A4, A3, A2, A1, C2, C1 = \
    DB23, DB22, DB21, DB20, DB19, DB18, DB17, DB16, DB15, DB14, DB13, DB12, DB11, DB10, DB9, DB8, DB7, DB6, DB5, DB4, DB3, DB2, DB1, DB0

# 0000_0000_0000_0000_0000_00xx
# for b(ab) counter latch mode must be (0, 1)
CONTROL_BITS = (C2, C1)

# 0000_0000_0000_0000_xxxx_xx00   --   a counter operation
# A6 | A5 | ... | A2 | A1   divide ratio
#  0    0   ...    0    0   0
#  0    0   ...    0    1   1
#  0    0   ...    1    0   2
#  .    .   ...    .    .   .
#  1    1   ...    1    0   62
#  1    1   ...    1    1   63
A_COUNTER_BITS = (A6, A5, A4, A3, A2, A1)

# 000x_xxxx_xxxx_xxxx_0000_0000   --   b counter operation
# B13 | B13 | ... | B2 | B1   divide ratio
#  0     0    ...    0    0   N/A
#  0     0    ...    0    1   N/A
#  0     0    ...    1    0   N/A
#  0     0    ...    1    1   3
#  .     .    ...    .    .   .
#  1     1    ...    1    0   8190
#  1     1    ...    1    1   8191
B_COUNTER_BITS = (B13, B12, B11, B10, B9, B8, B7, B6, B5, B4, B3, B2, B1)

# 00x0_0000_0000_0000_0000_0000   --   CP gain (depends on F4 of function latch)
# F4 | G1   operation
#  0   0    0=charge pump current setting 1 is permanently used
#  0   1    1=charge pump current setting 2 is permanently used
#  1   0    2=charge pump current setting 1 is used
#  1   1    3=charge pump is switched to setting 2; the time spent in setting 2 depends on fastlock mode (see function latch)
CP_GAIN_BITS = (G1, )
CP_GAIN_MODE = {
    0: [0],
    1: [1],
    2: [0],
    3: [1]
}

# xx00_0000_0000_0000_0000_0000   --   reserved


class Adf4113NcountLatch(Adf4113RegisterBase):

    cp_gain_mode_labels = {
        0: ('Setting 1 perm', 'Charge pump current setting 1 is permanently used.'),
        1: ('Setting 2 perm', 'Charge pump current setting 2 is permanently used.'),
        2: ('Setting 1', 'Charge pump current setting 1 is used.'),
        3: ('Switch to setting 2',
            'Charge pump is switched to setting 2. The time spent in setting 2 depends on fastlock mode (see function latch).')
    }

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


class Adf4113NcountLatchWidget(QGroupBox):

    bitmapChanged = pyqtSignal()
    title = 'AB count latch'

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setCheckable(True)
        self.setChecked(True)

        self._slideAcount = SpinSlide(0, 63, 0, '')
        self._slideBcount = SpinSlide(3, 8191, 1, '')
        self._comboCpGain = QComboBox()

        self._containerLayout = QVBoxLayout()
        self._formLayout = QFormLayout()
        self._bitLayout = QVBoxLayout()

        self._latch = Adf4113NcountLatch()

        self._tableBits = QTableView()
        self._bitModel = BitModel(rowSize=8,
                                  bits=self._latch.bin,
                                  labels=['X', 'X', 'G1', 'B13', 'B12', 'B11', 'B10', 'B9',
                                          'B8', 'B7', 'B6', 'B5', 'B4', 'B3', 'B2', 'B1',
                                          'A6', 'A5', 'A4', 'A3', 'A2', 'A1', 'C2', 'C1'],
                                  disabled=[True, True, False, False, False, False, False, False,
                                            False, False, False, False, False, False, False, False,
                                            False, False, False, False, False, False, True, True],
                                  parent=self)

        self._init()

    def _init(self):
        self._containerLayout.addLayout(self._formLayout)
        self._containerLayout.addLayout(self._bitLayout)

        self._formLayout.addRow('A counter', self._slideAcount)
        self._formLayout.addRow('B counter', self._slideBcount)
        self._formLayout.addRow('Charge pump gain', self._comboCpGain)

        self._bitLayout.addWidget(self._tableBits)

        self.setLayout(self._containerLayout)

        self._comboCpGain.setModel(MapModel(self, self._latch.cp_gain_mode_labels, sort=False))
        self.setTitle(f'{self.title} (h:{self._latch.hex} b:{self._latch.bin})')

        self._tableBits.setModel(self._bitModel)

        self._tableBits.horizontalHeader().setVisible(False)
        self._tableBits.verticalHeader().setVisible(False)
        self._tableBits.verticalHeader().setDefaultSectionSize(20)
        self._tableBits.resizeColumnsToContents()
        self._tableBits.setSelectionMode(0)

        self._setupSignals()

    def _setupSignals(self):
        self._slideAcount.valueChanged.connect(self.updateBitmap)
        self._slideBcount.valueChanged.connect(self.updateBitmap)
        self._comboCpGain.currentIndexChanged.connect(self.updateBitmap)
        self._bitModel.bitChanged.connect(self.onBitChanged)

    def updateDisplay(self):
        self.setTitle(f'{self.title} (h:{self._latch.hex} b:{self._latch.bin})')

        self._bitModel.update(self._latch.bin)

        self.bitmapChanged.emit()

    @pyqtSlot(int)
    def updateBitmap(self, _):
        self._latch.a_counter = self._slideAcount.value()
        self._latch.b_counter = self._slideBcount.value()
        self._latch.cp_gain = self._comboCpGain.currentData(MapModel.RoleNodeId)

        self.updateDisplay()

    @pyqtSlot(int, int)
    def onBitChanged(self, row, col):
        self.latch.toggle_nth_bit(row * 8 + 7 - col)

        self.updateDisplay()

    @property
    def latch(self):
        return self._latch


