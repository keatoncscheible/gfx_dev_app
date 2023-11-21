# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gfx_knob_widget.ui'
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
from widgets.knob_widget import KnobWidget

class Ui_GfxKnobWidget(object):
    def setupUi(self, GfxKnobWidget):
        if not GfxKnobWidget.objectName():
            GfxKnobWidget.setObjectName(u"GfxKnobWidget")
        GfxKnobWidget.resize(94, 120)
        self.verticalLayout = QVBoxLayout(GfxKnobWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gfx_knob = KnobWidget(GfxKnobWidget)
        self.gfx_knob.setObjectName(u"gfx_knob")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gfx_knob.sizePolicy().hasHeightForWidth())
        self.gfx_knob.setSizePolicy(sizePolicy)
        self.gfx_knob.setMinimumSize(QSize(75, 75))
        self.gfx_knob.setMaximumSize(QSize(75, 75))
        self.gfx_knob.setMaximum(1000)
        self.gfx_knob.setValue(500)

        self.verticalLayout.addWidget(self.gfx_knob, 0, Qt.AlignHCenter)

        self.gfx_knob_name = EditableLabelWidget(GfxKnobWidget)
        self.gfx_knob_name.setObjectName(u"gfx_knob_name")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.gfx_knob_name.sizePolicy().hasHeightForWidth())
        self.gfx_knob_name.setSizePolicy(sizePolicy1)
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.gfx_knob_name.setFont(font)

        self.verticalLayout.addWidget(self.gfx_knob_name, 0, Qt.AlignHCenter)


        self.retranslateUi(GfxKnobWidget)

        QMetaObject.connectSlotsByName(GfxKnobWidget)
    # setupUi

    def retranslateUi(self, GfxKnobWidget):
        GfxKnobWidget.setWindowTitle(QCoreApplication.translate("GfxKnobWidget", u"GFX Knob", None))
        self.gfx_knob_name.setText(QCoreApplication.translate("GfxKnobWidget", u"GFX Knob", None))
    # retranslateUi

