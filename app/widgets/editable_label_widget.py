from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QLabel, QLineEdit


class CustomLineEdit(QLineEdit):
    editingCanceled = Signal()

    def __init__(self, parent):
        super().__init__(parent)
        self.setStyleSheet("color: #000000;")

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.editingCanceled.emit()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.editingCanceled.emit()
        else:
            super().keyPressEvent(event)


class EditableLabelWidget(QLabel):
    label_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.editbox = None

    def mouseDoubleClickEvent(self, event):
        if not self.editbox:
            self.create_editbox()

    def create_editbox(self):
        self.editbox = CustomLineEdit(self)
        self.editbox.setText(self.text())
        self.editbox.returnPressed.connect(self.finish_editing)
        self.editbox.editingCanceled.connect(self.cancel_editing)
        self.editbox.show()
        self.editbox.setFocus()
        self.editbox.selectAll()

    def finish_editing(self):
        if self.editbox is not None:
            label_text = self.editbox.text()
            self.setText(label_text)
            self.label_changed.emit(label_text)
            self.cleanup_editbox()

    def cancel_editing(self):
        self.cleanup_editbox()

    def cleanup_editbox(self):
        if self.editbox is not None:
            self.editbox.deleteLater()
            self.editbox = None
