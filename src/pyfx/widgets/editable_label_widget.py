from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QLabel, QLineEdit


class CustomLineEdit(QLineEdit):
    """
    A custom QLineEdit that emits signals when editing is either accepted or canceled.
    """

    editing_canceled = Signal()
    editing_accepted = Signal()

    def __init__(self, parent):
        """
        Initialize the custom line edit with a parent.
        :param parent: The parent widget.
        """
        super().__init__(parent)
        self.setStyleSheet("color: #000000;")

    def focusOutEvent(self, event):
        """
        Handles the focus out event. Emits the editing_accepted signal.
        :param event: The focus out event.
        """
        super().focusOutEvent(event)
        self.editing_accepted.emit()

    def keyPressEvent(self, event):
        """
        Handles the key press event. Emits the editing_canceled signal if the Escape key is pressed.
        :param event: The key press event.
        """
        if event.key() == Qt.Key_Escape:
            self.editing_canceled.emit()
        else:
            super().keyPressEvent(event)


class EditableLabelWidget(QLabel):
    """
    A custom QLabel that becomes a QLineEdit when double-clicked, allowing the text to be edited.
    """

    label_changed = Signal(str)

    def __init__(self, parent=None):
        """
        Initialize the editable label widget with an optional parent.
        :param parent: The parent widget, default is None.
        """
        super().__init__(parent)
        self.editbox = None

    def mouseDoubleClickEvent(self, event):
        """
        Handles the mouse double-click event to create an edit box for editing the label.
        :param event: The mouse double-click event.
        """
        if not self.editbox:
            self.create_editbox()

    def create_editbox(self):
        """
        Creates the edit box for editing the label's text.
        """
        self.editbox = CustomLineEdit(self)
        self.editbox.setText(self.text())
        self.editbox.returnPressed.connect(self.finish_editing)
        self.editbox.editing_accepted.connect(self.finish_editing)
        self.editbox.editing_canceled.connect(self.cancel_editing)
        self.editbox.show()
        self.editbox.setFocus()
        self.editbox.selectAll()

    def finish_editing(self):
        """
        Finishes editing the label, updating the label's text and emitting the label_changed signal.
        """
        if self.editbox is not None:
            label_text = self.editbox.text()
            self.setText(label_text)
            self.label_changed.emit(label_text)
            self.cleanup_editbox()

    def cancel_editing(self):
        """
        Cancels the editing and removes the edit box.
        """
        self.cleanup_editbox()

    def cleanup_editbox(self):
        """
        Cleans up the edit box, deleting it and resetting the reference to None.
        """
        if self.editbox is not None:
            self.editbox.deleteLater()
            self.editbox = None
