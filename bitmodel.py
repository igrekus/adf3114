from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex, QVariant, pyqtSlot


class BitModel(QAbstractTableModel):

    def __init__(self, rowSize=8, bits='', labels=None, disabled=None, parent=None):
        super().__init__(parent)

        self._data = list()

        self._init(rowSize, bits, labels, disabled)
        # TODO pad missing cols if needed

    def clear(self):
        self.beginRemoveRows(QModelIndex(), 0, len(self._data))
        self._data.clear()
        self.endRemoveRows()

    def _init(self, rowSize, bits, labels, disabled):
        self.beginResetModel()
        row = list()
        for char, label, dis in zip(bits, labels, disabled):
            row.append((bool(int(char)), label, dis))
            if len(row) == rowSize:
                self._data.append(row)
                row = list()
        self._data = list(reversed(self._data))
        self.endResetModel()

    def rowCount(self, parent=None, *args, **kwargs):
        if parent.isValid():
            return 0
        return len(self._data)

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self._data[0])

    def data(self, index, role=None):
        if not index.isValid():
            return QVariant()

        if not self._data:
            return QVariant()
        col = index.column()
        row = index.row()

        if role == Qt.DisplayRole:
            return QVariant(self._data[row][col][1])

        if role == Qt.CheckStateRole:
            return QVariant(self._data[row][col][0] * 2)

        return QVariant()

    def flags(self, index: QModelIndex):
        f = super().flags(index)
        row = index.row()
        col = index.column()
        if self._data[row][col][2]:
            f &= Qt.ItemIsUserCheckable
        return f

    @pyqtSlot(int)
    def updateModel(self, chip):
        self._init(chip)
