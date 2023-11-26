# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'knob_config_dialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QComboBox,
    QDialog, QDialogButtonBox, QDoubleSpinBox, QFormLayout,
    QLabel, QSizePolicy, QVBoxLayout, QWidget)

class Ui_KnobConfigDialog(object):
    def setupUi(self, KnobConfigDialog):
        if not KnobConfigDialog.objectName():
            KnobConfigDialog.setObjectName(u"KnobConfigDialog")
        KnobConfigDialog.resize(276, 341)
        self.knob_config_dialog_layout = QVBoxLayout(KnobConfigDialog)
        self.knob_config_dialog_layout.setSpacing(20)
        self.knob_config_dialog_layout.setObjectName(u"knob_config_dialog_layout")
        self.knob_configuration_label = QLabel(KnobConfigDialog)
        self.knob_configuration_label.setObjectName(u"knob_configuration_label")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.knob_configuration_label.sizePolicy().hasHeightForWidth())
        self.knob_configuration_label.setSizePolicy(sizePolicy)
        self.knob_configuration_label.setMinimumSize(QSize(0, 30))
        self.knob_configuration_label.setMaximumSize(QSize(16777215, 30))
        font = QFont()
        font.setPointSize(16)
        self.knob_configuration_label.setFont(font)

        self.knob_config_dialog_layout.addWidget(self.knob_configuration_label, 0, Qt.AlignHCenter)

        self.knob_config_form_layout = QFormLayout()
        self.knob_config_form_layout.setObjectName(u"knob_config_form_layout")
        self.knob_config_form_layout.setLabelAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.knob_config_form_layout.setFormAlignment(Qt.AlignHCenter|Qt.AlignTop)
        self.knob_config_form_layout.setHorizontalSpacing(25)
        self.knob_config_form_layout.setVerticalSpacing(10)
        self.knob_config_form_layout.setContentsMargins(-1, -1, 25, -1)
        self.minimum_label = QLabel(KnobConfigDialog)
        self.minimum_label.setObjectName(u"minimum_label")
        font1 = QFont()
        font1.setPointSize(12)
        self.minimum_label.setFont(font1)

        self.knob_config_form_layout.setWidget(0, QFormLayout.LabelRole, self.minimum_label)

        self.minimum_spinbox = QDoubleSpinBox(KnobConfigDialog)
        self.minimum_spinbox.setObjectName(u"minimum_spinbox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.minimum_spinbox.sizePolicy().hasHeightForWidth())
        self.minimum_spinbox.setSizePolicy(sizePolicy1)
        self.minimum_spinbox.setMaximumSize(QSize(100, 16777215))
        self.minimum_spinbox.setMinimum(-999999999.000000000000000)
        self.minimum_spinbox.setMaximum(999999999.000000000000000)
        self.minimum_spinbox.setSingleStep(0.010000000000000)

        self.knob_config_form_layout.setWidget(0, QFormLayout.FieldRole, self.minimum_spinbox)

        self.maximum_label = QLabel(KnobConfigDialog)
        self.maximum_label.setObjectName(u"maximum_label")
        self.maximum_label.setFont(font1)
        self.maximum_label.setLayoutDirection(Qt.LeftToRight)

        self.knob_config_form_layout.setWidget(1, QFormLayout.LabelRole, self.maximum_label)

        self.maximum_spinbox = QDoubleSpinBox(KnobConfigDialog)
        self.maximum_spinbox.setObjectName(u"maximum_spinbox")
        sizePolicy1.setHeightForWidth(self.maximum_spinbox.sizePolicy().hasHeightForWidth())
        self.maximum_spinbox.setSizePolicy(sizePolicy1)
        self.maximum_spinbox.setMaximumSize(QSize(100, 16777215))
        self.maximum_spinbox.setMinimum(-999999999.000000000000000)
        self.maximum_spinbox.setMaximum(999999999.000000000000000)
        self.maximum_spinbox.setSingleStep(0.010000000000000)
        self.maximum_spinbox.setValue(1.000000000000000)

        self.knob_config_form_layout.setWidget(1, QFormLayout.FieldRole, self.maximum_spinbox)

        self.default_label = QLabel(KnobConfigDialog)
        self.default_label.setObjectName(u"default_label")
        self.default_label.setFont(font1)

        self.knob_config_form_layout.setWidget(2, QFormLayout.LabelRole, self.default_label)

        self.default_spinbox = QDoubleSpinBox(KnobConfigDialog)
        self.default_spinbox.setObjectName(u"default_spinbox")
        sizePolicy1.setHeightForWidth(self.default_spinbox.sizePolicy().hasHeightForWidth())
        self.default_spinbox.setSizePolicy(sizePolicy1)
        self.default_spinbox.setMaximumSize(QSize(100, 16777215))
        self.default_spinbox.setMinimum(-999999999.000000000000000)
        self.default_spinbox.setMaximum(999999999.000000000000000)
        self.default_spinbox.setSingleStep(0.010000000000000)
        self.default_spinbox.setValue(0.500000000000000)

        self.knob_config_form_layout.setWidget(2, QFormLayout.FieldRole, self.default_spinbox)

        self.precision_label = QLabel(KnobConfigDialog)
        self.precision_label.setObjectName(u"precision_label")
        self.precision_label.setFont(font1)

        self.knob_config_form_layout.setWidget(3, QFormLayout.LabelRole, self.precision_label)

        self.precision_spinbox = QDoubleSpinBox(KnobConfigDialog)
        self.precision_spinbox.setObjectName(u"precision_spinbox")
        sizePolicy1.setHeightForWidth(self.precision_spinbox.sizePolicy().hasHeightForWidth())
        self.precision_spinbox.setSizePolicy(sizePolicy1)
        self.precision_spinbox.setMaximumSize(QSize(100, 16777215))
        self.precision_spinbox.setMaximum(999999999.000000000000000)
        self.precision_spinbox.setSingleStep(0.100000000000000)
        self.precision_spinbox.setValue(0.010000000000000)

        self.knob_config_form_layout.setWidget(3, QFormLayout.FieldRole, self.precision_spinbox)

        self.sensitivity_label = QLabel(KnobConfigDialog)
        self.sensitivity_label.setObjectName(u"sensitivity_label")
        self.sensitivity_label.setFont(font1)

        self.knob_config_form_layout.setWidget(4, QFormLayout.LabelRole, self.sensitivity_label)

        self.sensitivity_spinbox = QDoubleSpinBox(KnobConfigDialog)
        self.sensitivity_spinbox.setObjectName(u"sensitivity_spinbox")
        sizePolicy1.setHeightForWidth(self.sensitivity_spinbox.sizePolicy().hasHeightForWidth())
        self.sensitivity_spinbox.setSizePolicy(sizePolicy1)
        self.sensitivity_spinbox.setMaximumSize(QSize(100, 16777215))
        self.sensitivity_spinbox.setMinimum(0.100000000000000)
        self.sensitivity_spinbox.setMaximum(5.000000000000000)
        self.sensitivity_spinbox.setSingleStep(0.010000000000000)
        self.sensitivity_spinbox.setValue(1.000000000000000)

        self.knob_config_form_layout.setWidget(4, QFormLayout.FieldRole, self.sensitivity_spinbox)

        self.mode_label = QLabel(KnobConfigDialog)
        self.mode_label.setObjectName(u"mode_label")
        self.mode_label.setFont(font1)

        self.knob_config_form_layout.setWidget(5, QFormLayout.LabelRole, self.mode_label)

        self.mode_combobox = QComboBox(KnobConfigDialog)
        self.mode_combobox.addItem("")
        self.mode_combobox.addItem("")
        self.mode_combobox.setObjectName(u"mode_combobox")
        sizePolicy1.setHeightForWidth(self.mode_combobox.sizePolicy().hasHeightForWidth())
        self.mode_combobox.setSizePolicy(sizePolicy1)
        self.mode_combobox.setMaximumSize(QSize(100, 16777215))

        self.knob_config_form_layout.setWidget(5, QFormLayout.FieldRole, self.mode_combobox)

        self.enable_display_label = QLabel(KnobConfigDialog)
        self.enable_display_label.setObjectName(u"enable_display_label")
        self.enable_display_label.setFont(font1)

        self.knob_config_form_layout.setWidget(6, QFormLayout.LabelRole, self.enable_display_label)

        self.enable_display_checkbox = QCheckBox(KnobConfigDialog)
        self.enable_display_checkbox.setObjectName(u"enable_display_checkbox")
        sizePolicy1.setHeightForWidth(self.enable_display_checkbox.sizePolicy().hasHeightForWidth())
        self.enable_display_checkbox.setSizePolicy(sizePolicy1)
        self.enable_display_checkbox.setMaximumSize(QSize(100, 16777215))
        self.enable_display_checkbox.setLayoutDirection(Qt.LeftToRight)

        self.knob_config_form_layout.setWidget(6, QFormLayout.FieldRole, self.enable_display_checkbox)


        self.knob_config_dialog_layout.addLayout(self.knob_config_form_layout)

        self.button_box = QDialogButtonBox(KnobConfigDialog)
        self.button_box.setObjectName(u"button_box")
        self.button_box.setLayoutDirection(Qt.RightToLeft)
        self.button_box.setOrientation(Qt.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.Apply|QDialogButtonBox.Cancel)
        self.button_box.setCenterButtons(True)

        self.knob_config_dialog_layout.addWidget(self.button_box, 0, Qt.AlignHCenter)


        self.retranslateUi(KnobConfigDialog)
        self.button_box.accepted.connect(KnobConfigDialog.accept)
        self.button_box.rejected.connect(KnobConfigDialog.reject)

        QMetaObject.connectSlotsByName(KnobConfigDialog)
    # setupUi

    def retranslateUi(self, KnobConfigDialog):
        KnobConfigDialog.setWindowTitle(QCoreApplication.translate("KnobConfigDialog", u"Configure Knob", None))
        self.knob_configuration_label.setText(QCoreApplication.translate("KnobConfigDialog", u"Knob Configuration", None))
        self.minimum_label.setText(QCoreApplication.translate("KnobConfigDialog", u"Minimum Value", None))
        self.maximum_label.setText(QCoreApplication.translate("KnobConfigDialog", u"Maximum Value", None))
        self.default_label.setText(QCoreApplication.translate("KnobConfigDialog", u"Default Value", None))
        self.precision_label.setText(QCoreApplication.translate("KnobConfigDialog", u"Precision", None))
        self.sensitivity_label.setText(QCoreApplication.translate("KnobConfigDialog", u"Sensitivity", None))
        self.sensitivity_spinbox.setSuffix("")
        self.mode_label.setText(QCoreApplication.translate("KnobConfigDialog", u"Mode", None))
        self.mode_combobox.setItemText(0, QCoreApplication.translate("KnobConfigDialog", u"linear", None))
        self.mode_combobox.setItemText(1, QCoreApplication.translate("KnobConfigDialog", u"logarithmic", None))

        self.enable_display_label.setText(QCoreApplication.translate("KnobConfigDialog", u"Enable Display", None))
        self.enable_display_checkbox.setText("")
    # retranslateUi

