from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFormLayout
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot

from adf3114ncountlatch import Adf3114NcountLatchWidget
from adf3114refcountlatch import Adf3114RefcountLatchWidget
from adf3114funclatch import Adf3114FuncLatchWidget
from adf3114initlatch import Adf3114InitLatchWidget
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
        self._ui.ncounterLatchWidget = Adf3114NcountLatchWidget(parent=self)
        self._ui.gridLatch.addWidget(self._ui.ncounterLatchWidget, 1, 2)

        self._ui.rcounterLatchWidget = Adf3114RefcountLatchWidget(parent=self)
        self._ui.gridLatch.addWidget(self._ui.rcounterLatchWidget, 0, 2)

        self._ui.funcLatchWidget = Adf3114FuncLatchWidget(parent=self)
        self._ui.gridLatch.addWidget(self._ui.funcLatchWidget, 0, 1, 2, 1)

        self._ui.initLatchWidget = Adf3114InitLatchWidget(parent=self)
        self._ui.initLatchWidget.setTitle('Init latch')
        self._ui.gridLatch.addWidget(self._ui.initLatchWidget, 0, 0, 2, 1)

        # create models
        self.initDialog()

    def setupUiSignals(self):
        self._ui.ncounterLatchWidget.bitmapChanged.connect(self.updateNcounterInput)
        self._ui.rcounterLatchWidget.bitmapChanged.connect(self.updateRcounterInput)
        self._ui.funcLatchWidget.bitmapChanged.connect(self.updateFuncInput)
        self._ui.initLatchWidget.bitmapChanged.connect(self.updateInitInput)

    def setupModels(self):
        pass

    def initDialog(self):
        self.setupModels()
        self.setupUiSignals()

        self._ui.btnDisconnect.setVisible(False)

    @pyqtSlot()
    def on_btnConnect_clicked(self):
        if not self._domain.connectProgr():
            QMessageBox.warning(self, 'Ошибка',
                                'Не найден программатор, проверьте подкючение.')

    @pyqtSlot()
    def on_btnWrite_clicked(self):
        self._domain.send(self._ui.editCommand.text())

    @pyqtSlot()
    def updateNcounterInput(self):
        self.updateRegisterInput(self._ui.ncounterLatchWidget.latch)

    @pyqtSlot()
    def updateRcounterInput(self):
        self.updateRegisterInput(self._ui.rcounterLatchWidget.latch)

    @pyqtSlot()
    def updateFuncInput(self):
        self.updateRegisterInput(self._ui.funcLatchWidget.latch)

    @pyqtSlot()
    def updateInitInput(self):
        self.updateRegisterInput(self._ui.initLatchWidget.latch)

    @pyqtSlot(str)
    def on_editRegister_textChanged(self, text: str):
        command = f'<f.{text.upper()}.FFFFFF>'
        self._ui.editCommand.setText(command)

    # helpers
    def updateRegisterInput(self, latch):
        self._ui.editRegister.setText(latch.hex)

