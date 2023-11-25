from PySide6.QtCore import QRect, Signal
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QColorDialog, QWidget


class ColorSelector(QWidget):
    color_changed = Signal(QColor)

    def __init__(self, parent, initial_color=QColor(255, 0, 0)):
        super().__init__()
        self.color = initial_color
        self.setFixedSize(50, 20)

    def set(self, color: QColor):
        if color.isValid():
            self.color = color
            self.update()
            self.color_changed.emit(color)

    def value(self):
        return self.color

    def paintEvent(self, event):
        painter = QPainter(self)
        if isinstance(self.color, QColor):
            painter.fillRect(QRect(0, 0, self.width(), self.height()), self.color)

    def mousePressEvent(self, event):
        new_color = QColorDialog.getColor(
            self.color if isinstance(self.color, QColor) else QColor(255, 0, 0)
        )
        self.set(new_color)
