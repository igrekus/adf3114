from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFormLayout
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot

from adf3114ncountlatch import cp_gain_mode_labels
from adf3114refcountlatch import antibacklash_pulse_width_labels
from mytools.mapmodel import MapModel
from spinslide import SpinSlide

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

        # create models
        self._slideRefcount = SpinSlide(1, 16380, 1, '')
        self._ui.flRefcount.insertRow(0, 'Reference counter', self._slideRefcount)

        self._slideAcount = SpinSlide(0, 63, 0, '')
        self._ui.flAbcount.insertRow(0, 'A counter', self._slideAcount)
        self._slideBcount = SpinSlide(3, 8191, 1, '')
        self._ui.flAbcount.insertRow(3, 'B counter', self._slideBcount)

        self._modelCpGain = MapModel(parent=self, data=cp_gain_mode_labels, sort=False)
        self._modelAntibacklash = MapModel(parent=self, data=antibacklash_pulse_width_labels, sort=False)

        self.initDialog()

    def setupUiSignals(self):
        pass

        # self.measurementFinished.connect(self._measureModel.updateModel)
        # self.measurementFinished.connect(self._plotWidget.updatePlot)

    def setupModels(self):
        self._ui.comboCpGain.setModel(self._modelCpGain)
        self._ui.comboAntibacklash.setModel(self._modelAntibacklash)

    def initDialog(self):
        self.setupModels()
        self.setupUiSignals()

        self._ui.btnDisconnect.setVisible(False)
        # self._ui.comboChip.setModel(self._chipModel)
        #
        # self._ui.tableMeasure.setModel(self._measureModel)

        # self.refreshView()

    # # UI utility methods
    # def refreshView(self):
    #     self.resizeTable()
    #
    # def resizeTable(self):
    #     self._ui.tableMeasure.resizeRowsToContents()
    #     self._ui.tableMeasure.resizeColumnsToContents()
    #
    # def modeSearchInstruments(self):
    #     self._ui.btnMeasureStop.hide()
    #     self._ui.btnCheckSample.setEnabled(False)
    #     self._ui.comboChip.setEnabled(False)
    #     self._ui.btnMeasureStart.setEnabled(False)
    #
    # def modeCheckSample(self):
    #     self._ui.btnCheckSample.setEnabled(True)
    #     self._ui.comboChip.setEnabled(True)
    #     self._ui.btnMeasureStart.show()
    #     self._ui.btnMeasureStart.setEnabled(False)
    #     self._ui.btnMeasureStop.hide()
    #     analyzer, progr = self._instrumentManager.getInstrumentNames()
    #     self._ui.editAnalyzer.setText(analyzer)
    #     self._ui.editProg.setText(progr)
    #
    # def modeReadyToMeasure(self):
    #     self._ui.btnCheckSample.setEnabled(False)
    #     self._ui.comboChip.setEnabled(False)
    #     self._ui.btnMeasureStart.setEnabled(True)
    #
    # def modeMeasureInProgress(self):
    #     self._ui.btnCheckSample.setEnabled(False)
    #     self._ui.comboChip.setEnabled(False)
    #     self._ui.btnMeasureStart.setVisible(False)
    #     self._ui.btnMeasureStop.setVisible(True)
    #
    # def modeMeasureFinished(self):
    #     self._ui.btnCheckSample.setEnabled(False)
    #     self._ui.comboChip.setEnabled(False)
    #     self._ui.btnMeasureStart.setVisible(False)
    #     self._ui.btnMeasureStop.setVisible(True)
    #
    # def collectParams(self):
    #     chip_type = self._ui.comboChip.currentData(MapModel.RoleNodeId)
    #     return chip_type
    #
    # # instrument control methods
    # def search(self):
    #     if not self._instrumentManager.findInstruments():
    #         QMessageBox.information(self, "Ошибка",
    #                                 "Не удалось найти инструменты, проверьте подключение.\nПодробности в логах.")
    #         return False
    #
    #     print('found all instruments, enabling sample test')
    #     return True
    #
    # # event handlers
    # def resizeEvent(self, event):
    #     self.refreshView()
    #
    # # autowire callbacks
    # @pyqtSlot()
    # def on_btnSearchInstruments_clicked(self):
    #     self.modeSearchInstruments()
    #     if not self.search():
    #         return
    #     self.modeCheckSample()
    #     self.instrumentsFound.emit()
    #
    #
    # def failWith(self, message):
    #     QMessageBox.information(self, "Ошибка", message)
    #
    # @pyqtSlot()
    # def on_btnCheckSample_clicked(self):
    #     try:
    #         if not self._instrumentManager.checkSample():
    #             self.failWith("Не удалось найти образец, проверьте подключение.\nПодробности в логах.")
    #             print('sample not detected')
    #             return
    #     except Exception as ex:
    #         print(ex)
    #     self.modeReadyToMeasure()
    #     self.sampleFound.emit()
    #     self.refreshView()
    #
    # @pyqtSlot()
    # def on_btnMeasureStart_clicked(self):
    #     print('start measurement task')
    #
    #     # if not self._instrumentManager.checkSample():
    #     #     self.failWith("Не удалось найти образец, проверьте подключение.\nПодробности в логах.")
    #     #     print('sample not detected')
    #     #     return
    #
    #     self.modeMeasureInProgress()
    #     params = self.collectParams()
    #     self._instrumentManager.measure(params)
    #     self.measurementFinished.emit(params)
    #     self.modeMeasureFinished()
    #     self.refreshView()
    #
    # @pyqtSlot()
    # def on_btnMeasureStop_clicked(self):
    #     # TODO implement
    #     print('abort measurement task')
    #     self.modeCheckSample()
    #
    # @pyqtSlot()
    # def on_btnReport_clicked(self):
    #     print('reporting')
    #
