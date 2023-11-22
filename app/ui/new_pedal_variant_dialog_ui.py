# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_pedal_variant_dialog.ui'
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
    QLabel, QLineEdit, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_NewPedalVariantDialog(object):
    def setupUi(self, NewPedalVariantDialog):
        if not NewPedalVariantDialog.objectName():
            NewPedalVariantDialog.setObjectName(u"NewPedalVariantDialog")
        NewPedalVariantDialog.resize(232, 126)
        self.new_pedal_variant_dialog_layout = QVBoxLayout(NewPedalVariantDialog)
        self.new_pedal_variant_dialog_layout.setSpacing(10)
        self.new_pedal_variant_dialog_layout.setObjectName(u"new_pedal_variant_dialog_layout")
        self.new_pedal_variant_dialog_layout.setContentsMargins(15, 15, 15, 15)
        self.new_pedal_variant_label = QLabel(NewPedalVariantDialog)
        self.new_pedal_variant_label.setObjectName(u"new_pedal_variant_label")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.new_pedal_variant_label.sizePolicy().hasHeightForWidth())
        self.new_pedal_variant_label.setSizePolicy(sizePolicy)
        self.new_pedal_variant_label.setMinimumSize(QSize(0, 30))
        self.new_pedal_variant_label.setMaximumSize(QSize(16777215, 50))
        font = QFont()
        font.setPointSize(16)
        self.new_pedal_variant_label.setFont(font)

        self.new_pedal_variant_dialog_layout.addWidget(self.new_pedal_variant_label, 0, Qt.AlignHCenter)

        self.new_pedal_variant_editbox = QLineEdit(NewPedalVariantDialog)
        self.new_pedal_variant_editbox.setObjectName(u"new_pedal_variant_editbox")

        self.new_pedal_variant_dialog_layout.addWidget(self.new_pedal_variant_editbox)

        self.button_box = QDialogButtonBox(NewPedalVariantDialog)
        self.button_box.setObjectName(u"button_box")
        self.button_box.setOrientation(Qt.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.new_pedal_variant_dialog_layout.addWidget(self.button_box, 0, Qt.AlignHCenter)


        self.retranslateUi(NewPedalVariantDialog)
        self.button_box.accepted.connect(NewPedalVariantDialog.accept)
        self.button_box.rejected.connect(NewPedalVariantDialog.reject)

        QMetaObject.connectSlotsByName(NewPedalVariantDialog)
    # setupUi

    def retranslateUi(self, NewPedalVariantDialog):
        NewPedalVariantDialog.setWindowTitle(QCoreApplication.translate("NewPedalVariantDialog", u"Create New Pedal Variant", None))
        self.new_pedal_variant_label.setText(QCoreApplication.translate("NewPedalVariantDialog", u"New Pedal Variant", None))
        self.new_pedal_variant_editbox.setPlaceholderText(QCoreApplication.translate("NewPedalVariantDialog", u"Variant Name", None))
    # retranslateUi

