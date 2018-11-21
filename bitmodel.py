from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex, QVariant, pyqtSignal


class BitModel(QAbstractTableModel):

    bitChanged = pyqtSignal(int, int)

    def __init__(self, rowSize=8, bits='', labels=None, disabled=None, parent=None):
        super().__init__(parent)

        self._data = list()

        self._rowSize = rowSize
        self._labels = labels
        self._disabled = disabled

        self._init(self._rowSize, bits, self._labels, self._disabled)
        # TODO pad missing cols if needed

    def clear(self):
        self.beginRemoveRows(QModelIndex(), 0, len(self._data))
        self._data.clear()
        self.endRemoveRows()

    def _init(self, rowSize, bits, labels, disabled):
        self.beginResetModel()
        self._data.clear()
        row = list()
        for char, label, dis in zip(bits, labels, disabled):
            row.append((bool(int(char)), label, dis))
            if len(row) == rowSize:
                self._data.append(row)
                row = list()
        self._data = list(reversed(self._data))
        self.endResetModel()

    def update(self, bits: str):
        self._init(self._rowSize, bits, self._labels, self._disabled)

    def rowCount(self, parent=None, *args, **kwargs):
        if parent.isValid():
            return 0
        return len(self._data)

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self._data[0])

    def setData(self, index, value, role=None):
        self.bitChanged.emit(index.row(), index.column())
        return True

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
        if not self._data[row][col][2]:
            f = f | Qt.ItemIsUserCheckable # | Qt.ItemIsEnabled
        else:
            f ^= Qt.ItemIsEnabled
        return f
