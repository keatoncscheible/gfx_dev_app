# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'footswitch_config_dialog.ui'
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
    QDialog, QDialogButtonBox, QFormLayout, QHBoxLayout,
    QLabel, QListWidget, QListWidgetItem, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)
import pyfx.assets.icons_rc

class Ui_FootswitchConfigDialog(object):
    def setupUi(self, FootswitchConfigDialog):
        if not FootswitchConfigDialog.objectName():
            FootswitchConfigDialog.setObjectName(u"FootswitchConfigDialog")
        FootswitchConfigDialog.resize(250, 355)
        self.footswitch_config_dialog_layout = QVBoxLayout(FootswitchConfigDialog)
        self.footswitch_config_dialog_layout.setSpacing(20)
        self.footswitch_config_dialog_layout.setObjectName(u"footswitch_config_dialog_layout")
        self.footswitch_configration_label = QLabel(FootswitchConfigDialog)
        self.footswitch_configration_label.setObjectName(u"footswitch_configration_label")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.footswitch_configration_label.sizePolicy().hasHeightForWidth())
        self.footswitch_configration_label.setSizePolicy(sizePolicy)
        self.footswitch_configration_label.setMinimumSize(QSize(0, 30))
        self.footswitch_configration_label.setMaximumSize(QSize(16777215, 30))
        font = QFont()
        font.setPointSize(16)
        self.footswitch_configration_label.setFont(font)

        self.footswitch_config_dialog_layout.addWidget(self.footswitch_configration_label, 0, Qt.AlignHCenter)

        self.footswitch_config_form_layout = QFormLayout()
        self.footswitch_config_form_layout.setObjectName(u"footswitch_config_form_layout")
        self.footswitch_config_form_layout.setFormAlignment(Qt.AlignHCenter|Qt.AlignTop)
        self.footswitch_config_form_layout.setHorizontalSpacing(25)
        self.footswitch_config_form_layout.setVerticalSpacing(10)
        self.footswitch_config_form_layout.setContentsMargins(-1, -1, 25, -1)
        self.footswitch_type_label = QLabel(FootswitchConfigDialog)
        self.footswitch_type_label.setObjectName(u"footswitch_type_label")
        font1 = QFont()
        font1.setPointSize(12)
        self.footswitch_type_label.setFont(font1)

        self.footswitch_config_form_layout.setWidget(0, QFormLayout.LabelRole, self.footswitch_type_label)

        self.footswitch_type_combobox = QComboBox(FootswitchConfigDialog)
        self.footswitch_type_combobox.addItem("")
        self.footswitch_type_combobox.addItem("")
        self.footswitch_type_combobox.addItem("")
        self.footswitch_type_combobox.setObjectName(u"footswitch_type_combobox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.footswitch_type_combobox.sizePolicy().hasHeightForWidth())
        self.footswitch_type_combobox.setSizePolicy(sizePolicy1)
        self.footswitch_type_combobox.setMaximumSize(QSize(100, 16777215))

        self.footswitch_config_form_layout.setWidget(0, QFormLayout.FieldRole, self.footswitch_type_combobox)

        self.default_label = QLabel(FootswitchConfigDialog)
        self.default_label.setObjectName(u"default_label")
        self.default_label.setFont(font1)

        self.footswitch_config_form_layout.setWidget(1, QFormLayout.LabelRole, self.default_label)

        self.default_combobox = QComboBox(FootswitchConfigDialog)
        self.default_combobox.addItem("")
        self.default_combobox.addItem("")
        self.default_combobox.setObjectName(u"default_combobox")
        sizePolicy1.setHeightForWidth(self.default_combobox.sizePolicy().hasHeightForWidth())
        self.default_combobox.setSizePolicy(sizePolicy1)
        self.default_combobox.setMaximumSize(QSize(100, 16777215))

        self.footswitch_config_form_layout.setWidget(1, QFormLayout.FieldRole, self.default_combobox)

        self.modes_label = QLabel(FootswitchConfigDialog)
        self.modes_label.setObjectName(u"modes_label")
        self.modes_label.setFont(font1)

        self.footswitch_config_form_layout.setWidget(2, QFormLayout.LabelRole, self.modes_label)

        self.modes_list = QListWidget(FootswitchConfigDialog)
        self.modes_list.setObjectName(u"modes_list")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.modes_list.sizePolicy().hasHeightForWidth())
        self.modes_list.setSizePolicy(sizePolicy2)
        self.modes_list.setMaximumSize(QSize(100, 100))

        self.footswitch_config_form_layout.setWidget(2, QFormLayout.FieldRole, self.modes_list)

        self.modes_spacer = QSpacerItem(0, 0, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.footswitch_config_form_layout.setItem(3, QFormLayout.LabelRole, self.modes_spacer)

        self.modes_button_layout = QHBoxLayout()
        self.modes_button_layout.setSpacing(2)
        self.modes_button_layout.setObjectName(u"modes_button_layout")
        self.add_mode_button = QPushButton(FootswitchConfigDialog)
        self.add_mode_button.setObjectName(u"add_mode_button")
        sizePolicy1.setHeightForWidth(self.add_mode_button.sizePolicy().hasHeightForWidth())
        self.add_mode_button.setSizePolicy(sizePolicy1)
        self.add_mode_button.setMaximumSize(QSize(20, 20))
        icon = QIcon()
        icon.addFile(u":/footswitch_mode_control/plus.png", QSize(), QIcon.Normal, QIcon.Off)
        self.add_mode_button.setIcon(icon)
        self.add_mode_button.setIconSize(QSize(12, 12))

        self.modes_button_layout.addWidget(self.add_mode_button)

        self.remove_mode_button = QPushButton(FootswitchConfigDialog)
        self.remove_mode_button.setObjectName(u"remove_mode_button")
        sizePolicy1.setHeightForWidth(self.remove_mode_button.sizePolicy().hasHeightForWidth())
        self.remove_mode_button.setSizePolicy(sizePolicy1)
        self.remove_mode_button.setMaximumSize(QSize(20, 20))
        icon1 = QIcon()
        icon1.addFile(u":/footswitch_mode_control/minus.png", QSize(), QIcon.Normal, QIcon.Off)
        self.remove_mode_button.setIcon(icon1)
        self.remove_mode_button.setIconSize(QSize(12, 12))

        self.modes_button_layout.addWidget(self.remove_mode_button)

        self.move_mode_up_button = QPushButton(FootswitchConfigDialog)
        self.move_mode_up_button.setObjectName(u"move_mode_up_button")
        sizePolicy1.setHeightForWidth(self.move_mode_up_button.sizePolicy().hasHeightForWidth())
        self.move_mode_up_button.setSizePolicy(sizePolicy1)
        self.move_mode_up_button.setMaximumSize(QSize(20, 20))
        icon2 = QIcon()
        icon2.addFile(u":/footswitch_mode_control/up-arrow.png", QSize(), QIcon.Normal, QIcon.Off)
        self.move_mode_up_button.setIcon(icon2)
        self.move_mode_up_button.setIconSize(QSize(12, 12))

        self.modes_button_layout.addWidget(self.move_mode_up_button)

        self.move_mode_down_button = QPushButton(FootswitchConfigDialog)
        self.move_mode_down_button.setObjectName(u"move_mode_down_button")
        sizePolicy1.setHeightForWidth(self.move_mode_down_button.sizePolicy().hasHeightForWidth())
        self.move_mode_down_button.setSizePolicy(sizePolicy1)
        self.move_mode_down_button.setMaximumSize(QSize(20, 20))
        icon3 = QIcon()
        icon3.addFile(u":/footswitch_mode_control/down-arrow.png", QSize(), QIcon.Normal, QIcon.Off)
        self.move_mode_down_button.setIcon(icon3)
        self.move_mode_down_button.setIconSize(QSize(12, 12))

        self.modes_button_layout.addWidget(self.move_mode_down_button)


        self.footswitch_config_form_layout.setLayout(3, QFormLayout.FieldRole, self.modes_button_layout)

        self.enable_display_checkbox = QCheckBox(FootswitchConfigDialog)
        self.enable_display_checkbox.setObjectName(u"enable_display_checkbox")
        sizePolicy1.setHeightForWidth(self.enable_display_checkbox.sizePolicy().hasHeightForWidth())
        self.enable_display_checkbox.setSizePolicy(sizePolicy1)
        self.enable_display_checkbox.setMaximumSize(QSize(100, 16777215))
        self.enable_display_checkbox.setLayoutDirection(Qt.LeftToRight)

        self.footswitch_config_form_layout.setWidget(4, QFormLayout.FieldRole, self.enable_display_checkbox)

        self.enable_display_label = QLabel(FootswitchConfigDialog)
        self.enable_display_label.setObjectName(u"enable_display_label")
        self.enable_display_label.setFont(font1)

        self.footswitch_config_form_layout.setWidget(4, QFormLayout.LabelRole, self.enable_display_label)


        self.footswitch_config_dialog_layout.addLayout(self.footswitch_config_form_layout)

        self.button_box = QDialogButtonBox(FootswitchConfigDialog)
        self.button_box.setObjectName(u"button_box")
        self.button_box.setLayoutDirection(Qt.RightToLeft)
        self.button_box.setOrientation(Qt.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.Apply|QDialogButtonBox.Cancel)
        self.button_box.setCenterButtons(True)

        self.footswitch_config_dialog_layout.addWidget(self.button_box)


        self.retranslateUi(FootswitchConfigDialog)
        self.button_box.accepted.connect(FootswitchConfigDialog.accept)
        self.button_box.rejected.connect(FootswitchConfigDialog.reject)

        QMetaObject.connectSlotsByName(FootswitchConfigDialog)
    # setupUi

    def retranslateUi(self, FootswitchConfigDialog):
        FootswitchConfigDialog.setWindowTitle(QCoreApplication.translate("FootswitchConfigDialog", u"Configure Footswitch", None))
        self.footswitch_configration_label.setText(QCoreApplication.translate("FootswitchConfigDialog", u"Footswitch Configuration", None))
        self.footswitch_type_label.setText(QCoreApplication.translate("FootswitchConfigDialog", u"Type", None))
        self.footswitch_type_combobox.setItemText(0, QCoreApplication.translate("FootswitchConfigDialog", u"latching", None))
        self.footswitch_type_combobox.setItemText(1, QCoreApplication.translate("FootswitchConfigDialog", u"momentary", None))
        self.footswitch_type_combobox.setItemText(2, QCoreApplication.translate("FootswitchConfigDialog", u"mode", None))

        self.default_label.setText(QCoreApplication.translate("FootswitchConfigDialog", u"Default State", None))
        self.default_combobox.setItemText(0, QCoreApplication.translate("FootswitchConfigDialog", u"off", None))
        self.default_combobox.setItemText(1, QCoreApplication.translate("FootswitchConfigDialog", u"on", None))

        self.modes_label.setText(QCoreApplication.translate("FootswitchConfigDialog", u"Modes", None))
        self.add_mode_button.setText("")
        self.remove_mode_button.setText("")
        self.move_mode_up_button.setText("")
        self.move_mode_down_button.setText("")
        self.enable_display_checkbox.setText("")
        self.enable_display_label.setText(QCoreApplication.translate("FootswitchConfigDialog", u"Enable Display", None))
    # retranslateUi

