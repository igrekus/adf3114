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
        self._ui.initLatchWidget.setTitle('Init latch')
        self._ui.gridLatch.addWidget(self._ui.initLatchWidget, 0, 0, 2, 1)

        self._bitGroup = QButtonGroup(self)
        self._bitGroup.setExclusive(False)
        for index, box in enumerate((getattr(self._ui, f'cbox{index:02d}') for index in range(24))):
            self._bitGroup.addButton(box, index)

        # create models
        self.initDialog()

        # self.size()

    def setupUiSignals(self):
        self._ui.ncounterLatchWidget.bitmapChanged.connect(self.updateNcounterInput)
        self._ui.rcounterLatchWidget.bitmapChanged.connect(self.updateRcounterInput)
        self._ui.funcLatchWidget.bitmapChanged.connect(self.updateFuncInput)
        self._ui.initLatchWidget.bitmapChanged.connect(self.updateInitInput)

        self._ui.ncounterLatchWidget.toggled.connect(self.onLatchChecked)
        self._ui.rcounterLatchWidget.toggled.connect(self.onLatchChecked)
        self._ui.funcLatchWidget.toggled.connect(self.onLatchChecked)
        self._ui.initLatchWidget.toggled.connect(self.onLatchChecked)

        self._bitGroup.buttonToggled[int, bool].connect(self.on_bitGroup_buttonToggled)

    def setupModels(self):
        pass

    def initDialog(self):
        self.setupModels()
        self.setupUiSignals()

        self.modeDisconnected()

    def modeDisconnected(self):
        self._ui.btnConnect.setVisible(True)
        self._ui.btnDisconnect.setVisible(False)
        self._ui.btnWrite.setEnabled(False)

        # self._ui.ncounterLatchWidget.setEnabled(False)
        # self._ui.rcounterLatchWidget.setEnabled(False)
        # self._ui.funcLatchWidget.setEnabled(False)
        # self._ui.initLatchWidget.setEnabled(False)

        # self._ui.editBin.setEnabled(False)
        # self._ui.editHex.setEnabled(False)
        # self._ui.editCommand.setEnabled(False)
        # self.setBitGroupEnabled(False)

    def modeConnected(self):
        self._ui.btnConnect.setVisible(False)
        self._ui.btnDisconnect.setVisible(True)
        self._ui.btnWrite.setEnabled(True)

        # self._ui.ncounterLatchWidget.setEnabled(True)
        # self._ui.rcounterLatchWidget.setEnabled(True)
        # self._ui.funcLatchWidget.setEnabled(True)
        # self._ui.initLatchWidget.setEnabled(True)

        # self._ui.editBin.setEnabled(True)
        # self._ui.editHex.setEnabled(True)
        # self._ui.editCommand.setEnabled(True)
        # self.setBitGroupEnabled(True)

    def setBitGroupEnabled(self, state: bool):
        for box in self._bitGroup.buttons():
            box.setEnabled(state)

    @pyqtSlot()
    def on_btnConnect_clicked(self):
        if not self._domain.connectProgr():
            QMessageBox.warning(self, 'Ошибка',
                                'Не найден программатор, проверьте подкючение.')

        self.modeConnected()

    @pyqtSlot()
    def on_btnDisconnect_clicked(self):
        self._domain.disconnectProgr()

        self.modeDisconnected()

    @pyqtSlot()
    def on_btnWrite_clicked(self):
        self._domain.send(self._ui.editCommand.text())

    @pyqtSlot()
    def updateNcounterInput(self):
        self._updateRegisterInput(self._ui.ncounterLatchWidget.latch)

    @pyqtSlot()
    def updateRcounterInput(self):
        self._updateRegisterInput(self._ui.rcounterLatchWidget.latch)

    @pyqtSlot()
    def updateFuncInput(self):
        self._updateRegisterInput(self._ui.funcLatchWidget.latch)

    @pyqtSlot()
    def updateInitInput(self):
        self._updateRegisterInput(self._ui.initLatchWidget.latch)

    @pyqtSlot(str)
    def on_editHex_textChanged(self, text: str):
        if not text:
            return

        # self._ui.editCommand.blockSignals(True)
        # self._ui.editBin.blockSignals(True)

        self._buildCommand()
        self._ui.editBin.setText(f'{int(text, 16):024b}')

        # self._ui.editBin.blockSignals(False)
        # self._ui.editCommand.blockSignals(False)

    @pyqtSlot(str)
    def on_editBin_textChanged(self, text: str):
        if not text:
            return

        # self._ui.editHex.blockSignals(True)
        # self._bitGroup.blockSignals(True)

        self._ui.editHex.setText(f'{int(text, 2):06X}')
        for box, state in zip(self._bitGroup.buttons(), reversed([bool(int(c)) for c in self._ui.editBin.text()])):
            box.setChecked(state)

        # self._bitGroup.blockSignals(False)
        # self._ui.editHex.blockSignals(False)

    @pyqtSlot(int, bool)
    def on_bitGroup_buttonToggled(self, _):
        # self._ui.editBin.blockSignals(True)

        self._ui.editBin.setText(''.join(list(reversed([str(int(b.isChecked())) for b in self._bitGroup.buttons()]))))

        # self._ui.editBin.blockSignals(False)

    @pyqtSlot(bool)
    def onLatchChecked(self, _):
        self.on_editHex_textChanged(self._ui.editHex.text())

    # helpers
    def _updateRegisterInput(self, latch):
        self._ui.editHex.setText(latch.hex)

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


