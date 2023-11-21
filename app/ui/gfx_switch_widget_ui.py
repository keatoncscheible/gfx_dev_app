# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gfx_switch_widget.ui'
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
from PySide6.QtWidgets import (QApplication, QSizePolicy, QVBoxLayout, QWidget)

from widgets.editable_label_widget import EditableLabelWidget
from widgets.footswitch_widget import FootswitchWidget

class Ui_GfxSwitchWidget(object):
    def setupUi(self, GfxSwitchWidget):
        if not GfxSwitchWidget.objectName():
            GfxSwitchWidget.setObjectName(u"GfxSwitchWidget")
        GfxSwitchWidget.resize(102, 69)
        self.verticalLayout = QVBoxLayout(GfxSwitchWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gfx_switch = FootswitchWidget(GfxSwitchWidget)
        self.gfx_switch.setObjectName(u"gfx_switch")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gfx_switch.sizePolicy().hasHeightForWidth())
        self.gfx_switch.setSizePolicy(sizePolicy)
        self.gfx_switch.setMinimumSize(QSize(0, 0))
        self.gfx_switch.setMaximumSize(QSize(16777215, 16777215))
        self.gfx_switch.setCheckable(True)
        self.gfx_switch.setAutoDefault(False)
        self.gfx_switch.setFlat(False)

        self.verticalLayout.addWidget(self.gfx_switch, 0, Qt.AlignHCenter)

        self.gfx_switch_name = EditableLabelWidget(GfxSwitchWidget)
        self.gfx_switch_name.setObjectName(u"gfx_switch_name")
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.gfx_switch_name.setFont(font)

        self.verticalLayout.addWidget(self.gfx_switch_name, 0, Qt.AlignHCenter)


        self.retranslateUi(GfxSwitchWidget)
        self.gfx_switch.clicked["bool"].connect(GfxSwitchWidget.gfx_switch_toggled)

        self.gfx_switch.setDefault(False)


        QMetaObject.connectSlotsByName(GfxSwitchWidget)
    # setupUi

    def retranslateUi(self, GfxSwitchWidget):
        GfxSwitchWidget.setWindowTitle(QCoreApplication.translate("GfxSwitchWidget", u"GFX Switch", None))
        self.gfx_switch.setText("")
        self.gfx_switch_name.setText(QCoreApplication.translate("GfxSwitchWidget", u"GFX Switch", None))
    # retranslateUi

