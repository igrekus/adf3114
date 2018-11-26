from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QButtonGroup
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot

from adf4113ncountlatch import Adf4113NcountLatchWidget
from adf4113refcountlatch import Adf4113RefcountLatchWidget
from adf4113funclatch import Adf4113FuncLatchWidget
from adf4113initlatch import Adf4113InitLatchWidget
from domain import Domain


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

        # create models
        self.initDialog()

        # self.size()

    def setupUiSignals(self):
        self._ui.ncounterLatchWidget.bitmapChanged.connect(self._buildCommand)
        self._ui.rcounterLatchWidget.bitmapChanged.connect(self._buildCommand)
        self._ui.funcLatchWidget.bitmapChanged.connect(self._buildCommand)
        self._ui.initLatchWidget.bitmapChanged.connect(self._buildCommand)

        self._ui.ncounterLatchWidget.toggled.connect(self._buildCommand)
        self._ui.rcounterLatchWidget.toggled.connect(self._buildCommand)
        self._ui.funcLatchWidget.toggled.connect(self._buildCommand)
        self._ui.initLatchWidget.toggled.connect(self._buildCommand)

    def setupModels(self):
        pass

    def initDialog(self):
        self.setupModels()
        self.setupUiSignals()

        self._modeDisconnected()

    def _modeDisconnected(self):
        self._ui.btnConnect.setVisible(True)
        self._ui.btnDisconnect.setVisible(False)
        self._ui.btnWrite.setEnabled(False)

    def _modeConnected(self):
        self._ui.btnConnect.setVisible(False)
        self._ui.btnDisconnect.setVisible(True)
        self._ui.btnWrite.setEnabled(True)

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
    def _buildCommand(self):
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


