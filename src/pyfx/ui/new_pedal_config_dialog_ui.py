# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_pedal_config_dialog.ui'
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
    QFormLayout, QLabel, QLineEdit, QSizePolicy,
    QSpinBox, QVBoxLayout, QWidget)

from pyfx.widgets.color_selector import ColorSelector

class Ui_NewPedalConfigDialog(object):
    def setupUi(self, NewPedalConfigDialog):
        if not NewPedalConfigDialog.objectName():
            NewPedalConfigDialog.setObjectName(u"NewPedalConfigDialog")
        NewPedalConfigDialog.resize(319, 302)
        self.verticalLayout = QVBoxLayout(NewPedalConfigDialog)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(15, 15, 15, 15)
        self.new_pedal_config_label = QLabel(NewPedalConfigDialog)
        self.new_pedal_config_label.setObjectName(u"new_pedal_config_label")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.new_pedal_config_label.sizePolicy().hasHeightForWidth())
        self.new_pedal_config_label.setSizePolicy(sizePolicy)
        self.new_pedal_config_label.setMinimumSize(QSize(0, 30))
        self.new_pedal_config_label.setMaximumSize(QSize(16777215, 50))
        font = QFont()
        font.setPointSize(16)
        self.new_pedal_config_label.setFont(font)

        self.verticalLayout.addWidget(self.new_pedal_config_label, 0, Qt.AlignHCenter)

        self.config_layout = QFormLayout()
        self.config_layout.setObjectName(u"config_layout")
        self.config_layout.setFormAlignment(Qt.AlignHCenter|Qt.AlignTop)
        self.config_layout.setHorizontalSpacing(40)
        self.config_layout.setVerticalSpacing(15)
        self.config_layout.setContentsMargins(-1, 5, 25, 5)
        self.pedal_name_label = QLabel(NewPedalConfigDialog)
        self.pedal_name_label.setObjectName(u"pedal_name_label")
        font1 = QFont()
        font1.setPointSize(12)
        self.pedal_name_label.setFont(font1)

        self.config_layout.setWidget(0, QFormLayout.LabelRole, self.pedal_name_label)

        self.pedal_name_editbox = QLineEdit(NewPedalConfigDialog)
        self.pedal_name_editbox.setObjectName(u"pedal_name_editbox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pedal_name_editbox.sizePolicy().hasHeightForWidth())
        self.pedal_name_editbox.setSizePolicy(sizePolicy1)
        self.pedal_name_editbox.setMinimumSize(QSize(140, 0))
        self.pedal_name_editbox.setMaximumSize(QSize(140, 16777215))

        self.config_layout.setWidget(0, QFormLayout.FieldRole, self.pedal_name_editbox)

        self.knob_label = QLabel(NewPedalConfigDialog)
        self.knob_label.setObjectName(u"knob_label")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.knob_label.sizePolicy().hasHeightForWidth())
        self.knob_label.setSizePolicy(sizePolicy2)
        self.knob_label.setFont(font1)

        self.config_layout.setWidget(1, QFormLayout.LabelRole, self.knob_label)

        self.knob_cfg_spinbox = QSpinBox(NewPedalConfigDialog)
        self.knob_cfg_spinbox.setObjectName(u"knob_cfg_spinbox")
        sizePolicy1.setHeightForWidth(self.knob_cfg_spinbox.sizePolicy().hasHeightForWidth())
        self.knob_cfg_spinbox.setSizePolicy(sizePolicy1)
        self.knob_cfg_spinbox.setMaximumSize(QSize(50, 16777215))
        self.knob_cfg_spinbox.setAlignment(Qt.AlignCenter)
        self.knob_cfg_spinbox.setMaximum(12)
        self.knob_cfg_spinbox.setValue(1)

        self.config_layout.setWidget(1, QFormLayout.FieldRole, self.knob_cfg_spinbox)

        self.switches_label = QLabel(NewPedalConfigDialog)
        self.switches_label.setObjectName(u"switches_label")
        sizePolicy2.setHeightForWidth(self.switches_label.sizePolicy().hasHeightForWidth())
        self.switches_label.setSizePolicy(sizePolicy2)
        self.switches_label.setFont(font1)

        self.config_layout.setWidget(2, QFormLayout.LabelRole, self.switches_label)

        self.switch_cfg_spinbox = QSpinBox(NewPedalConfigDialog)
        self.switch_cfg_spinbox.setObjectName(u"switch_cfg_spinbox")
        sizePolicy1.setHeightForWidth(self.switch_cfg_spinbox.sizePolicy().hasHeightForWidth())
        self.switch_cfg_spinbox.setSizePolicy(sizePolicy1)
        self.switch_cfg_spinbox.setMaximumSize(QSize(50, 16777215))
        self.switch_cfg_spinbox.setAlignment(Qt.AlignCenter)
        self.switch_cfg_spinbox.setMaximum(12)
        self.switch_cfg_spinbox.setValue(1)

        self.config_layout.setWidget(2, QFormLayout.FieldRole, self.switch_cfg_spinbox)

        self.pedal_color_label = QLabel(NewPedalConfigDialog)
        self.pedal_color_label.setObjectName(u"pedal_color_label")
        sizePolicy2.setHeightForWidth(self.pedal_color_label.sizePolicy().hasHeightForWidth())
        self.pedal_color_label.setSizePolicy(sizePolicy2)
        self.pedal_color_label.setFont(font1)

        self.config_layout.setWidget(3, QFormLayout.LabelRole, self.pedal_color_label)

        self.pedal_color = ColorSelector(NewPedalConfigDialog)
        self.pedal_color.setObjectName(u"pedal_color")

        self.config_layout.setWidget(3, QFormLayout.FieldRole, self.pedal_color)

        self.text_color_label = QLabel(NewPedalConfigDialog)
        self.text_color_label.setObjectName(u"text_color_label")
        sizePolicy2.setHeightForWidth(self.text_color_label.sizePolicy().hasHeightForWidth())
        self.text_color_label.setSizePolicy(sizePolicy2)
        self.text_color_label.setFont(font1)

        self.config_layout.setWidget(4, QFormLayout.LabelRole, self.text_color_label)

        self.text_color = ColorSelector(NewPedalConfigDialog)
        self.text_color.setObjectName(u"text_color")

        self.config_layout.setWidget(4, QFormLayout.FieldRole, self.text_color)


        self.verticalLayout.addLayout(self.config_layout)

        self.button_box = QDialogButtonBox(NewPedalConfigDialog)
        self.button_box.setObjectName(u"button_box")
        self.button_box.setOrientation(Qt.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.button_box, 0, Qt.AlignHCenter)


        self.retranslateUi(NewPedalConfigDialog)
        self.button_box.accepted.connect(NewPedalConfigDialog.accept)
        self.button_box.rejected.connect(NewPedalConfigDialog.reject)

        QMetaObject.connectSlotsByName(NewPedalConfigDialog)
    # setupUi

    def retranslateUi(self, NewPedalConfigDialog):
        NewPedalConfigDialog.setWindowTitle(QCoreApplication.translate("NewPedalConfigDialog", u"New Pedal Configuration", None))
        self.new_pedal_config_label.setText(QCoreApplication.translate("NewPedalConfigDialog", u"New Pedal Configuration", None))
        self.pedal_name_label.setText(QCoreApplication.translate("NewPedalConfigDialog", u"Pedal Name", None))
        self.pedal_name_editbox.setPlaceholderText(QCoreApplication.translate("NewPedalConfigDialog", u"Enter Pedal Name", None))
        self.knob_label.setText(QCoreApplication.translate("NewPedalConfigDialog", u"Knobs", None))
        self.switches_label.setText(QCoreApplication.translate("NewPedalConfigDialog", u"Switches", None))
        self.pedal_color_label.setText(QCoreApplication.translate("NewPedalConfigDialog", u"Pedal Color", None))
        self.text_color_label.setText(QCoreApplication.translate("NewPedalConfigDialog", u"Text Color", None))
    # retranslateUi

