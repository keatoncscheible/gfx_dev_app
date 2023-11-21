from PySide6.QtCore import Signal
from PySide6.QtWidgets import QLabel, QLineEdit


class EditableLabelWidget(QLabel):
    label_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.edit = None

    def mouseDoubleClickEvent(self, event):
        if not self.edit:
            self.edit = QLineEdit(self)
            self.edit.setText(self.text())
            self.edit.setFixedSize(self.size())
            self.edit.returnPressed.connect(self.finish_editing)
            self.edit.show()
            self.edit.setFocus()

    def finish_editing(self):
        label_text = self.edit.text()
        self.setText(label_text)
        self.label_changed.emit(label_text)
        self.edit.deleteLater()
        self.edit = None
