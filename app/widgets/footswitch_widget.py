from PySide6.QtWidgets import QPushButton


class FootswitchWidget(QPushButton):
    def __init__(self, parent):
        super().__init__()

    def contextMenuEvent(self, event):
        """Add context menu if needed in the future"""
