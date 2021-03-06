# -*- coding: UTF-8 -*-
import os

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QButtonGroup
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot

from adf4113ncountlatch import Adf4113NcountLatchWidget
from adf4113refcountlatch import Adf4113RefcountLatchWidget
from adf4113funclatch import Adf4113FuncLatchWidget
from adf4113initlatch import Adf4113InitLatchWidget
from domain import Domain
from mytools.mapmodel import MapModel


preset_file = 'presets.txt'


class MainWindow(QMainWindow):

    instrumentsFound = pyqtSignal()
    sampleFound = pyqtSignal()
    measurementFinished = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setAttribute(Qt.WA_QuitOnClose)
        self.setAttribute(Qt.WA_DeleteOnClose)

        # create instance variables
        self._ui = uic.loadUi('mainwindow.ui', self)

        self._domain = Domain(parent=self)

        # create latch widgets
        self._ui.ncounterLatchWidget = Adf4113NcountLatchWidget(parent=self)
        self._ui.gridLatch.addWidget(self._ui.ncounterLatchWidget, 1, 2)

        self._ui.rcounterLatchWidget = Adf4113RefcountLatchWidget(parent=self)
        self._ui.gridLatch.addWidget(self._ui.rcounterLatchWidget, 0, 2)

        self._ui.funcLatchWidget = Adf4113FuncLatchWidget(parent=self)
        self._ui.gridLatch.addWidget(self._ui.funcLatchWidget, 0, 1, 2, 1)

        self._ui.initLatchWidget = Adf4113InitLatchWidget(parent=self)
        self._ui.gridLatch.addWidget(self._ui.initLatchWidget, 0, 0, 2, 1)

        # TODO extract class
        # TODO load command presets from a config file
        self._commandPresets = dict()

        # create models
        self._funcModel = MapModel(self, {
            0: ('Test connection', 'Протестировать подключение к программатору'),
            1: ('Counter reset method', 'Сбросить R и AB счетчики')
        }, sort=False)

        self.initDialog()

        # self.size()

    def loadPresets(self):
        if not os.path.isfile(f'./{preset_file}'):
            return

        labels = dict()
        with open(f'./{preset_file}', 'rt', encoding='utf-8') as f:
            for index, line in enumerate(f.readlines()):
                if '#' not in line:
                    command, label, tip = line.split('|')
                    self._commandPresets[index] = command
                    labels[index] = (label, tip)

        self._funcModel.initModel(labels)

    def setupUiSignals(self):
        self._ui.ncounterLatchWidget.bitmapChanged.connect(self._buildDebug)
        self._ui.rcounterLatchWidget.bitmapChanged.connect(self._buildDebug)
        self._ui.funcLatchWidget.bitmapChanged.connect(self._buildDebug)
        self._ui.initLatchWidget.bitmapChanged.connect(self._buildDebug)

        self._ui.ncounterLatchWidget.toggled.connect(self._buildDebug)
        self._ui.rcounterLatchWidget.toggled.connect(self._buildDebug)
        self._ui.funcLatchWidget.toggled.connect(self._buildDebug)
        self._ui.initLatchWidget.toggled.connect(self._buildDebug)

        self._ui.ncounterLatchWidget.bitmapChanged.connect(self._buildRun)
        self._ui.rcounterLatchWidget.bitmapChanged.connect(self._buildRun)
        self._ui.funcLatchWidget.bitmapChanged.connect(self._buildRun)

        self._ui.ncounterLatchWidget.toggled.connect(self._buildRun)
        self._ui.rcounterLatchWidget.toggled.connect(self._buildRun)
        self._ui.funcLatchWidget.toggled.connect(self._buildRun)

    def setupModels(self):
        self._ui.comboFunc.setModel(self._funcModel)

    def initUi(self):
        self._ui.initLatchWidget.setChecked(False)
        self._buildRun()

    def initDialog(self):
        self.loadPresets()



        self.setupModels()
        self.setupUiSignals()
        self.initUi()

        self._modeDisconnected()

    def _modeDisconnected(self):
        self._ui.btnConnect.setVisible(True)
        self._ui.btnDisconnect.setVisible(False)
        self._ui.btnWrite.setEnabled(False)
        self._ui.btnRun.setEnabled(False)

    def _modeConnected(self):
        self._ui.btnConnect.setVisible(False)
        self._ui.btnDisconnect.setVisible(True)
        self._ui.btnWrite.setEnabled(True)
        self._ui.btnRun.setEnabled(True)

    @pyqtSlot()
    def on_btnConnect_clicked(self):
        if not self._domain.connectProgr():
            QMessageBox.warning(self, 'Ошибка',
                                'Не найден программатор, проверьте подкючение.')
            return
        print('connected to SPI')
        self._modeConnected()

    @pyqtSlot()
    def on_btnDisconnect_clicked(self):
        self._domain.disconnectProgr()

        self._modeDisconnected()

    @pyqtSlot()
    def on_btnWrite_clicked(self):
        if self._domain.connected:
            self._domain.send(self._ui.editCommand.text())

    @pyqtSlot()
    def on_btnRun_clicked(self):
        if self._domain.connected:
            self._domain.send(self._ui.editRun.text())

    @pyqtSlot(int)
    def on_comboFunc_currentIndexChanged(self, index: int):
        command_id = self._ui.comboFunc.currentData(MapModel.RoleNodeId)
        command_seq = self._commandPresets[command_id]
        print(f'init command: id={command_id}, hex={command_seq}')
        self._ui.editCommand.setText(command_seq)
        self._ui.editFuncDesc.setText(self._ui.comboFunc.currentData(Qt.ToolTipRole))

    @pyqtSlot()
    def _buildDebug(self):
        def get_hex(widget):
            if not widget.isChecked():
                return ''
            return f'.{widget.latch.hex}'

        cmd = f'<f' \
              f'{get_hex(self._ui.initLatchWidget)}' \
              f'{get_hex(self._ui.funcLatchWidget)}' \
              f'{get_hex(self._ui.rcounterLatchWidget)}' \
              f'{get_hex(self._ui.ncounterLatchWidget)}>'

        self._ui.editCommand.setText(cmd)

    @pyqtSlot()
    def _buildRun(self):

        def enable_reset(widget):
            widget.latch.counter_reset = 1
            return f'{widget.latch.hex}'

        def disable_reset(widget):
            widget.latch.counter_reset = 0
            return f'{widget.latch.hex}'

        cmd = f'<f' \
              f'.{enable_reset(self._ui.funcLatchWidget)}' \
              f'.{self._ui.rcounterLatchWidget.latch.hex}' \
              f'.{self._ui.ncounterLatchWidget.latch.hex}' \
              f'.{disable_reset(self._ui.funcLatchWidget)}>'

        self._ui.editRun.setText(cmd)


