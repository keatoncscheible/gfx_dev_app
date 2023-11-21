from PySide6.QtGui import QPixmap, Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class AboutWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setAttribute(Qt.WA_DeleteOnClose)

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(60, 20, 60, 30)

        # Title
        self.title_label = QLabel("GFX Dev App", self)
        title_font = self.title_label.font()
        title_font.setPointSize(24)
        title_font.setBold(True)
        self.title_label.setFont(title_font)

        # Logo
        self.logo_label = QLabel(self)
        pixmap = QPixmap("app/assets/gfx_dev_logo.png")
        scaled_pixmap = pixmap.scaled(400, 400, Qt.KeepAspectRatio)
        self.logo_label.setPixmap(scaled_pixmap)

        # Copyright Message

        self.copyright_label = QLabel("© 2023 Keaton Scheible", self)
        copyright_font = self.title_label.font()
        copyright_font.setPointSize(16)
        copyright_font.setBold(False)
        self.copyright_label.setFont(copyright_font)

        # Adding widgets to the layout
        main_layout.addWidget(self.title_label, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.logo_label, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.copyright_label, alignment=Qt.AlignCenter)
        self.setLayout(main_layout)


# For testing purposes
if __name__ == "__main__":
    import sys

    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    about_widget = AboutWidget()
    about_widget.show()
    sys.exit(app.exec())
