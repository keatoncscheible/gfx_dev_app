# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'open_pedal_dialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QLabel, QListWidget, QListWidgetItem, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_OpenPedalDialog(object):
    def setupUi(self, OpenPedalDialog):
        if not OpenPedalDialog.objectName():
            OpenPedalDialog.setObjectName(u"OpenPedalDialog")
        OpenPedalDialog.resize(186, 197)
        self.verticalLayout = QVBoxLayout(OpenPedalDialog)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(15, 15, 15, 15)
        self.open_pedal_label = QLabel(OpenPedalDialog)
        self.open_pedal_label.setObjectName(u"open_pedal_label")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.open_pedal_label.sizePolicy().hasHeightForWidth())
        self.open_pedal_label.setSizePolicy(sizePolicy)
        self.open_pedal_label.setMinimumSize(QSize(0, 30))
        self.open_pedal_label.setMaximumSize(QSize(16777215, 50))
        font = QFont()
        font.setPointSize(16)
        self.open_pedal_label.setFont(font)

        self.verticalLayout.addWidget(self.open_pedal_label, 0, Qt.AlignHCenter)

        self.pedal_list = QListWidget(OpenPedalDialog)
        self.pedal_list.setObjectName(u"pedal_list")

        self.verticalLayout.addWidget(self.pedal_list, 0, Qt.AlignHCenter)

        self.button_box = QDialogButtonBox(OpenPedalDialog)
        self.button_box.setObjectName(u"button_box")
        self.button_box.setOrientation(Qt.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Open)

        self.verticalLayout.addWidget(self.button_box, 0, Qt.AlignHCenter)


        self.retranslateUi(OpenPedalDialog)
        self.button_box.accepted.connect(OpenPedalDialog.accept)
        self.button_box.rejected.connect(OpenPedalDialog.reject)

        QMetaObject.connectSlotsByName(OpenPedalDialog)
    # setupUi

    def retranslateUi(self, OpenPedalDialog):
        OpenPedalDialog.setWindowTitle(QCoreApplication.translate("OpenPedalDialog", u"Open Pedal", None))
        self.open_pedal_label.setText(QCoreApplication.translate("OpenPedalDialog", u"Open Pedal", None))
    # retranslateUi

