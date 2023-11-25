# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'transport_control_widget.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)
import pyfx.assets.icons_rc

class Ui_TransportControlWidget(object):
    def setupUi(self, TransportControlWidget):
        if not TransportControlWidget.objectName():
            TransportControlWidget.setObjectName(u"TransportControlWidget")
        TransportControlWidget.resize(350, 125)
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(TransportControlWidget.sizePolicy().hasHeightForWidth())
        TransportControlWidget.setSizePolicy(sizePolicy)
        TransportControlWidget.setMinimumSize(QSize(350, 125))
        TransportControlWidget.setMaximumSize(QSize(350, 125))
        self.verticalLayout = QVBoxLayout(TransportControlWidget)
        self.verticalLayout.setSpacing(15)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, -1, -1, 0)
        self.button_layout = QHBoxLayout()
        self.button_layout.setSpacing(30)
        self.button_layout.setObjectName(u"button_layout")
        self.horizontal_spacer_left = QSpacerItem(0, 0, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

        self.button_layout.addItem(self.horizontal_spacer_left)

        self.play_button = QPushButton(TransportControlWidget)
        self.play_button.setObjectName(u"play_button")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.play_button.sizePolicy().hasHeightForWidth())
        self.play_button.setSizePolicy(sizePolicy1)
        self.play_button.setMaximumSize(QSize(16777215, 16777215))
        icon = QIcon()
        icon.addFile(u":/transport_control/play_button.png", QSize(), QIcon.Normal, QIcon.Off)
        self.play_button.setIcon(icon)
        self.play_button.setIconSize(QSize(40, 40))
        self.play_button.setFlat(True)

        self.button_layout.addWidget(self.play_button, 0, Qt.AlignHCenter)

        self.pause_button = QPushButton(TransportControlWidget)
        self.pause_button.setObjectName(u"pause_button")
        sizePolicy1.setHeightForWidth(self.pause_button.sizePolicy().hasHeightForWidth())
        self.pause_button.setSizePolicy(sizePolicy1)
        self.pause_button.setMaximumSize(QSize(16777215, 16777215))
        icon1 = QIcon()
        icon1.addFile(u":/transport_control/pause_button.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pause_button.setIcon(icon1)
        self.pause_button.setIconSize(QSize(40, 40))
        self.pause_button.setFlat(True)

        self.button_layout.addWidget(self.pause_button, 0, Qt.AlignHCenter)

        self.stop_button = QPushButton(TransportControlWidget)
        self.stop_button.setObjectName(u"stop_button")
        sizePolicy1.setHeightForWidth(self.stop_button.sizePolicy().hasHeightForWidth())
        self.stop_button.setSizePolicy(sizePolicy1)
        self.stop_button.setMinimumSize(QSize(0, 0))
        self.stop_button.setMaximumSize(QSize(50, 50))
        icon2 = QIcon()
        icon2.addFile(u":/transport_control/stop_button.png", QSize(), QIcon.Normal, QIcon.Off)
        self.stop_button.setIcon(icon2)
        self.stop_button.setIconSize(QSize(40, 40))
        self.stop_button.setFlat(True)

        self.button_layout.addWidget(self.stop_button, 0, Qt.AlignHCenter)

        self.loop_button = QPushButton(TransportControlWidget)
        self.loop_button.setObjectName(u"loop_button")
        sizePolicy1.setHeightForWidth(self.loop_button.sizePolicy().hasHeightForWidth())
        self.loop_button.setSizePolicy(sizePolicy1)
        self.loop_button.setMinimumSize(QSize(0, 0))
        self.loop_button.setMaximumSize(QSize(50, 50))
        self.loop_button.setStyleSheet(u"QPushButton:checked {\n"
"    background-color: yellow;\n"
"}\n"
"QPushButton {\n"
"    background-color: transparent;\n"
"}\n"
"")
        icon3 = QIcon()
        icon3.addFile(u":/transport_control/loop_arrows.png", QSize(), QIcon.Normal, QIcon.Off)
        self.loop_button.setIcon(icon3)
        self.loop_button.setIconSize(QSize(40, 40))
        self.loop_button.setCheckable(True)
        self.loop_button.setFlat(True)

        self.button_layout.addWidget(self.loop_button)

        self.horizontal_spacer_right = QSpacerItem(0, 0, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

        self.button_layout.addItem(self.horizontal_spacer_right)


        self.verticalLayout.addLayout(self.button_layout)

        self.audio_file_combobox = QComboBox(TransportControlWidget)
        self.audio_file_combobox.setObjectName(u"audio_file_combobox")

        self.verticalLayout.addWidget(self.audio_file_combobox)


        self.retranslateUi(TransportControlWidget)
        self.play_button.pressed.connect(TransportControlWidget.play_button_pressed)
        self.stop_button.pressed.connect(TransportControlWidget.stop_button_pressed)
        self.loop_button.toggled.connect(TransportControlWidget.loop_button_toggled)
        self.pause_button.pressed.connect(TransportControlWidget.pause_button_pressed)
        self.audio_file_combobox.currentTextChanged.connect(TransportControlWidget.audio_file_changed)

        QMetaObject.connectSlotsByName(TransportControlWidget)
    # setupUi

    def retranslateUi(self, TransportControlWidget):
        TransportControlWidget.setWindowTitle(QCoreApplication.translate("TransportControlWidget", u"TransportControl", None))
        self.play_button.setText("")
        self.pause_button.setText("")
        self.stop_button.setText("")
        self.loop_button.setText("")
        self.audio_file_combobox.setCurrentText("")
        self.audio_file_combobox.setPlaceholderText(QCoreApplication.translate("TransportControlWidget", u"Select Audio File...", None))
    # retranslateUi

