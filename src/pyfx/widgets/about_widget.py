from PySide6.QtGui import QPixmap, Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class AboutWidget(QWidget):
    """
    A widget for displaying about information including a title, logo, and copyright message.
    """

    def __init__(self):
        """
        Initialize the AboutWidget.
        """
        super().__init__()
        self.setWindowTitle("About Pedal Builder")
        self.initUI()
        self.setAttribute(Qt.WA_DeleteOnClose)

    def initUI(self):
        """
        Initializes the UI components of the AboutWidget.
        """
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(60, 20, 60, 30)

        # Title
        self.title_label = QLabel("Pedal Builder", self)
        self._configure_label_font(self.title_label, 24, True)

        # Logo
        self.logo_label = QLabel(self)
        self._set_logo("src/pyfx/assets/pyfx_logo.png")

        # Copyright Message
        self.copy_right_label = QLabel("© 2023 Keaton Scheible", self)
        self._configure_label_font(self.copy_right_label, 16, False)

        # Adding widgets to the layout
        self._add_to_layout(main_layout)

    def _configure_label_font(self, label, point_size, is_bold):
        """
        Configures the font for a given label.
        :param label: The QLabel to configure.
        :param point_size: The point size of the font.
        :param is_bold: Whether the font should be bold.
        """
        font = label.font()
        font.setPointSize(point_size)
        font.setBold(is_bold)
        label.setFont(font)

    def _set_logo(self, logo_path):
        """
        Sets the logo image for the widget.
        :param logo_path: The path to the logo image file.
        """
        pixmap = QPixmap(logo_path)
        scaled_pixmap = pixmap.scaled(400, 400, Qt.KeepAspectRatio)
        self.logo_label.setPixmap(scaled_pixmap)

    def _add_to_layout(self, layout):
        """
        Adds the title, logo, and copyright labels to the layout.
        :param layout: The layout to which the widgets will be added.
        """
        layout.addWidget(self.title_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.logo_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.copy_right_label, alignment=Qt.AlignCenter)
        self.setLayout(layout)
