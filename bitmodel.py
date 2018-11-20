from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex, QVariant, pyqtSlot


class BitModel(QAbstractTableModel):

    def __init__(self, rowSize=8, bits='', labels=None, parent=None):
        super().__init__(parent)

        self._data = list()

        self._init(rowSize, bits, labels)
        # TODO pad missing cols if needed

    def clear(self):
        self.beginRemoveRows(QModelIndex(), 0, len(self._data))
        self._data.clear()
        self.endRemoveRows()

    def _init(self, rowSize, bits, labels):
        self.beginResetModel()
        row = list()
        for char, label in zip(bits, labels):
            row.append((bool(int(char)), label))
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

        col = index.column()
        row = index.row()

        if role == Qt.DisplayRole:
            if not self._data:
                return QVariant()
            return QVariant(self._data[row][col][1])

        return QVariant()

    @pyqtSlot(int)
    def updateModel(self, chip):
        self._init(chip)
