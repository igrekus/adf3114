from PyQt5.QtCore import pyqtSlot, pyqtSignal

from adf3114registerbase import *
from PyQt5.QtWidgets import QGroupBox, QComboBox, QFormLayout

from mytools.mapmodel import MapModel

# map latch bits onto register bits
P2, P1, PD2, CPI6, CPI5, CPI4, CPI3, CPI2, CPI1, TC4, TC3, TC2, TC1, F5, F4, F3, F2, M3, M2, M1, PD1, F1, C2, C1 = \
    DB23, DB22, DB21, DB20, DB19, DB18, DB17, DB16, DB15, DB14, DB13, DB12, DB11, DB10, DB9, DB8, DB7, DB6, DB5, DB4, DB3, DB2, DB1, DB0

# 0000_0000_0000_0000_0000_00xx
# for function latch mode must be (1, 0)
CONTROL_BITS = (C2, C1)

# 0000_0000_0000_0000_0000_0x00   --   counter operation
# F1
#  0   0=normal
#  1   1=R,A,B counters held in reset
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
PD_POLARITY_BITS = (F2, )
PD_POLARITY = {
    0: [0],
    1: [1]
}

# 0000_0000_0000_000x_0000_0000   --   charge pump
# F3
#  0   0=output normal
#  1   1=three-state
CHARGE_PUMP_BITS = (F3, )
CHARGE_PUMP_MODE = {
    0: [0],
    1: [1]
}

# 0000_0000_0000_0xx0_0000_0000   --   fastlock mode
# F5 | F4
#  0    x   0=disabled
#  1    0   1=mode 1
#  1    1   2=mode 2
FASTLOCK_MODE_BITS = (F4, F5)
FASTLOCK_MODE = {
    0: [0, 0],
    1: [1, 0],
    2: [1, 1]
}

# 0000_0000_0xxx_x000_0000_0000   --   timer counter control
# TC4 | TC3 | TC2 | TC1  | timeout (PFD cycles)
#   0     0     0     0      0=3
#   0     0     0     1      1=7
#   0     0     1     0      2=11
#   0     0     1     1      3=15
#   0     1     0     0      4=19
#   0     1     0     1      5=23
#   0     1     1     0      6=27
#   0     1     1     1      7=31
#   1     0     0     0      8=35
#   1     0     0     1      9=39
#   1     0     1     0      10=43
#   1     0     1     1      11=47
#   1     1     0     0      12=51
#   1     1     0     1      13=55
#   1     1     1     0      14=59
#   1     1     1     1      15=63
TIMER_COUNTER_MODE_BITS = (TC4, TC3, TC2, TC1)
TIMER_COUNTER_MODE = {
    0:  [0, 0, 0, 0],
    1:  [0, 0, 0, 1],
    2:  [0, 0, 1, 0],
    3:  [0, 0, 1, 1],
    4:  [0, 1, 0, 0],
    5:  [0, 1, 0, 1],
    6:  [0, 1, 1, 0],
    7:  [0, 1, 1, 1],
    8:  [1, 0, 0, 0],
    9:  [1, 0, 0, 1],
    10: [1, 0, 1, 0],
    11: [1, 0, 1, 1],
    12: [1, 1, 0, 0],
    13: [1, 1, 0, 1],
    14: [1, 1, 1, 0],
    15: [1, 1, 1, 1]
}

# 0000_00xx_x000_0000_0000_0000   --   current setting 1/2
# CPI6 | CPI5 | CPI4 |     Icp(mA)
# CPI3 | CPI2 | CPI1 | 2.7kOhm | 4.7kOhm | 10kOhm
#   0      0      0     1.09      0.63      0.29   0
#   0      0      1     2.18      1.25      0.59   1
#   0      1      0     3.72      1.88      0.88   2
#   0      1      1     4.36      2.50      1.76   3   - ?
#   1      0      0     5.44      3.13      1.47   4   - ?
#   1      0      1     6.53      3.75      1.76   5   - ?
#   1      1      0     7.62      4.38      2.06   6
#   1      1      1     8.70      5.00      2.36   7
CURRENT_SETTING_1_BITS = (CPI3, CPI2, CPI1)
CURRENT_SETTING_2_BITS = (CPI6, CPI5, CPI4)
CURRENT_SETTING_1 = {
    0: [0, 0, 0],
    1: [0, 0, 1],
    2: [0, 1, 0],
    3: [0, 1, 1],
    4: [1, 0, 0],
    5: [1, 0, 1],
    6: [1, 1, 0],
    7: [1, 1, 1]
}
CURRENT_SETTING_2 = {
    0: [0, 0, 0],
    1: [0, 0, 1],
    2: [0, 1, 0],
    3: [0, 1, 1],
    4: [1, 0, 0],
    5: [1, 0, 1],
    6: [1, 1, 0],
    7: [1, 1, 1]
}

# xx00_0000_0000_0000_0000_0000   --   prescaler value
# P2 | P1
#  0    0   0=8/9
#  0    1   1=16/17
#  1    0   2=32/33
#  1    1   3=64/65
PRESCALER_VALUE_BITS = (P2, P1)
PRESCALER_VALUE = {
    0: [0, 0],
    1: [0, 1],
    2: [1, 0],
    3: [1, 1]
}


class Adf3114FuncLatch(Adf3114RegisterBase):

    counter_reset_mode_labels = {
        0: ('Normal', 'Normal operation.'),
        1: ('Reset', 'R, A, B counters held in reset.')
    }

    power_down_mode_labels = {
        0: ('Async power-down #1', 'Asynchronous power-down.'),
        1: ('Normal operation', 'Normal operation'),
        2: ('Async power-down #2', 'Asynchronous power-down.'),
        3: ('Sync power-down', 'Synchronous power-down.')
    }

    muxout_mode_labels = {
        0: ('3-state', 'Three-state output.'),
        1: ('Digital lock detect', 'Digital lock detect (active high).'),
        2: ('N divider', 'N divider output.'),
        3: ('DVdd', 'DVdd.'),
        4: ('R divider', 'R divider output.'),
        5: ('Analog lock detect', 'Analog lock detect (n-channel open-drain.'),
        6: ('Serial out', 'Serial data output'),
        7: ('DGND', 'DGND.'),
    }

    pd_polarity_labels = {
        0: 'Negative',
        1: 'Positive'
    }

    charge_pump_output_mode_labels = {
        0: 'Normal output',
        1: 'Three-state'
    }

    fastlock_mode_labels = {
        0: ('Disabled', 'Fastlock disabled.'),
        1: ('Mode 1', 'Fastlock mode 1.'),
        2: ('Mode 2', 'Fastlock mode 2.'),
    }

    timer_counter_mode_labels = {
        0: '3 PFD cycles',
        1: '7 PFD cycles',
        2: '11 PFD cycles',
        3: '15 PFD cycles',
        4: '19 PFD cycles',
        5: '23 PFD cycles',
        6: '27 PFD cycles',
        7: '31 PFD cycles',
        8: '35 PFD cycles',
        9: '39 PFD cycles',
        10: '43 PFD cycles',
        11: '47 PFD cycles',
        12: '51 PFD cycles',
        13: '55 PFD cycles',
        14: '59 PFD cycles',
        15: '63 PFD cycles',
    }

    current_setting_labels = {
        0: ('1.09 / 0.63 / 0.29', '2.7кОм / 4.7кОм / 10кОм'),
        1: ('2.18 / 1.25 / 0.59', '2.7кОм / 4.7кОм / 10кОм'),
        2: ('3.72 / 1.88 / 0.88', '2.7кОм / 4.7кОм / 10кОм'),
        3: ('4.36 / 2.50 / 1.76', '2.7кОм / 4.7кОм / 10кОм'),
        4: ('5.44 / 3.13 / 1.47', '2.7кОм / 4.7кОм / 10кОм'),
        5: ('6.53 / 3.75 / 1.76', '2.7кОм / 4.7кОм / 10кОм'),
        6: ('7.62 / 4.38 / 2.06', '2.7кОм / 4.7кОм / 10кОм'),
        7: ('8.70 / 5.00 / 2.36', '2.7кОм / 4.7кОм / 10кОм'),
    }

    prescaler_value_labels = {
        0: '8/9',
        1: '16/17',
        2: '32/33',
        3: '64/65',
    }

    def __init__(self, bits=0):
        super().__init__(bits=bits)

        self.set_nth_bit(CONTROL_BITS[0])
        self.unset_nth_bit(CONTROL_BITS[1])

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

    @property
    def charge_pump_mode(self):
        return self._find_seq(CHARGE_PUMP_BITS, CHARGE_PUMP_MODE)

    @charge_pump_mode.setter
    def charge_pump_mode(self, mode):
        if mode not in PD_POLARITY:
            raise ValueError('Incorrect charge pump mode.')
        self.set_bit_pattern(mode, CHARGE_PUMP_BITS, CHARGE_PUMP_MODE)

    @property
    def fastlock_mode(self):
        return self._find_seq(FASTLOCK_MODE_BITS, FASTLOCK_MODE)

    @fastlock_mode.setter
    def fastlock_mode(self, mode):
        if mode not in FASTLOCK_MODE:
            raise ValueError('Incorrect charge pump mode.')
        self.set_bit_pattern(mode, FASTLOCK_MODE_BITS, FASTLOCK_MODE)

    @property
    def timer_counter_mode(self):
        return self._find_seq(TIMER_COUNTER_MODE_BITS, TIMER_COUNTER_MODE)

    @timer_counter_mode.setter
    def timer_counter_mode(self, mode):
        if mode not in TIMER_COUNTER_MODE:
            raise ValueError('Incorrect charge pump mode.')
        self.set_bit_pattern(mode, TIMER_COUNTER_MODE_BITS, TIMER_COUNTER_MODE)

    @property
    def current_setting_1(self):
        return self._find_seq(CURRENT_SETTING_1_BITS, CURRENT_SETTING_1)

    @current_setting_1.setter
    def current_setting_1(self, mode):
        if mode not in CURRENT_SETTING_1:
            raise ValueError('Incorrect current setting 1.')
        self.set_bit_pattern(mode, CURRENT_SETTING_1_BITS, CURRENT_SETTING_1)

    @property
    def current_setting_2(self):
        return self._find_seq(CURRENT_SETTING_2_BITS, CURRENT_SETTING_2)

    @current_setting_2.setter
    def current_setting_2(self, mode):
        if mode not in CURRENT_SETTING_2:
            raise ValueError('Incorrect current setting 2.')
        self.set_bit_pattern(mode, CURRENT_SETTING_2_BITS, CURRENT_SETTING_2)

    @property
    def prescale_value(self):
        return self._find_seq(PRESCALER_VALUE_BITS, PRESCALER_VALUE)

    @prescale_value.setter
    def prescale_value(self, mode):
        if mode not in PRESCALER_VALUE:
            raise ValueError('Incorrect current setting 2.')
        self.set_bit_pattern(mode, PRESCALER_VALUE_BITS, PRESCALER_VALUE)


class Adf3114FuncLatchWidget(QGroupBox):

    bitmapChanged = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setTitle('Function latch')
        self.setCheckable(True)
        self.setChecked(True)

        self._comboCountReset = QComboBox()
        self._comboPowdown = QComboBox()
        self._comboMuxout = QComboBox()
        self._comboPdPolarity = QComboBox()
        self._comboCpOut = QComboBox()
        self._comboFastlock = QComboBox()
        self._comboTimer = QComboBox()
        self._comboCurrent1 = QComboBox()
        self._comboCurrent2 = QComboBox()
        self._comboPrescaler = QComboBox()

        self._layout = QFormLayout(parent=self)
        self._layout.addRow('Counter reset', self._comboCountReset)
        self._layout.addRow('Power-down mode', self._comboPowdown)
        self._layout.addRow('MUXOUT control', self._comboMuxout)
        self._layout.addRow('Phase detector polarity', self._comboPdPolarity)
        self._layout.addRow('Charge pump output', self._comboCpOut)
        self._layout.addRow('Fastlock mode', self._comboFastlock)
        self._layout.addRow('Timer counter control', self._comboTimer)
        self._layout.addRow('Current setting 1', self._comboCurrent1)
        self._layout.addRow('Current setting 2', self._comboCurrent2)
        self._layout.addRow('Prescaler calue', self._comboPrescaler)

        self._latch = Adf3114FuncLatch()
        self._comboCountReset.setModel(MapModel(self, self._latch.counter_reset_mode_labels, sort=False))
        self._comboPowdown.setModel(MapModel(self, self._latch.power_down_mode_labels, sort=False))
        self._comboMuxout.setModel(MapModel(self, self._latch.muxout_mode_labels, sort=False))
        self._comboPdPolarity.setModel(MapModel(self, self._latch.pd_polarity_labels, sort=False))
        self._comboCpOut.setModel(MapModel(self, self._latch.charge_pump_output_mode_labels, sort=False))
        self._comboFastlock.setModel(MapModel(self, self._latch.fastlock_mode_labels, sort=False))
        self._comboTimer.setModel(MapModel(self, self._latch.timer_counter_mode_labels, sort=False))
        self._comboCurrent1.setModel(MapModel(self, self._latch.current_setting_labels, sort=False))
        self._comboCurrent2.setModel(MapModel(self, self._latch.current_setting_labels, sort=False))
        self._comboPrescaler.setModel(MapModel(self, self._latch.prescaler_value_labels, sort=False))

        self._comboCountReset.currentIndexChanged.connect(self.updateBitmap)
        self._comboPowdown.currentIndexChanged.connect(self.updateBitmap)
        self._comboMuxout.currentIndexChanged.connect(self.updateBitmap)
        self._comboPdPolarity.currentIndexChanged.connect(self.updateBitmap)
        self._comboCpOut.currentIndexChanged.connect(self.updateBitmap)
        self._comboFastlock.currentIndexChanged.connect(self.updateBitmap)
        self._comboTimer.currentIndexChanged.connect(self.updateBitmap)
        self._comboCurrent1.currentIndexChanged.connect(self.updateBitmap)
        self._comboCurrent2.currentIndexChanged.connect(self.updateBitmap)
        self._comboPrescaler.currentIndexChanged.connect(self.updateBitmap)

    @pyqtSlot(int)
    def updateBitmap(self, _):
        self._latch.counter_reset = self._comboCountReset.currentData(MapModel.RoleNodeId)
        self._latch.power_down_mode = self._comboPowdown.currentData(MapModel.RoleNodeId)
        self._latch.muxout_control = self._comboMuxout.currentData(MapModel.RoleNodeId)
        self._latch.phase_detector_polarity = self._comboPdPolarity.currentData(MapModel.RoleNodeId)
        self._latch.charge_pump_mode = self._comboCpOut.currentData(MapModel.RoleNodeId)
        self._latch.fastlock_mode = self._comboFastlock.currentData(MapModel.RoleNodeId)
        self._latch.timer_counter_mode = self._comboTimer.currentData(MapModel.RoleNodeId)
        self._latch.current_setting_1 = self._comboCurrent1.currentData(MapModel.RoleNodeId)
        self._latch.current_setting_2 = self._comboCurrent2.currentData(MapModel.RoleNodeId)
        self._latch.prescale_value = self._comboPrescaler.currentData(MapModel.RoleNodeId)

        self.bitmapChanged.emit()

    @property
    def latch(self):
        return self._latch


