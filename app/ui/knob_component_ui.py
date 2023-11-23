# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'knob_component.ui'
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
from PySide6.QtWidgets import (QApplication, QLineEdit, QSizePolicy, QVBoxLayout,
    QWidget)

from widgets.editable_label_widget import EditableLabelWidget
from widgets.knob import Knob

class Ui_KnobComponent(object):
    def setupUi(self, KnobComponent):
        if not KnobComponent.objectName():
            KnobComponent.setObjectName(u"KnobComponent")
        KnobComponent.resize(94, 136)
        self.verticalLayout = QVBoxLayout(KnobComponent)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.knob_editbox = QLineEdit(KnobComponent)
        self.knob_editbox.setObjectName(u"knob_editbox")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.knob_editbox.sizePolicy().hasHeightForWidth())
        self.knob_editbox.setSizePolicy(sizePolicy)
        self.knob_editbox.setMaximumSize(QSize(60, 16777215))

        self.verticalLayout.addWidget(self.knob_editbox, 0, Qt.AlignHCenter)

        self.knob = Knob(KnobComponent)
        self.knob.setObjectName(u"knob")
        sizePolicy.setHeightForWidth(self.knob.sizePolicy().hasHeightForWidth())
        self.knob.setSizePolicy(sizePolicy)
        self.knob.setMinimumSize(QSize(75, 75))
        self.knob.setMaximumSize(QSize(75, 75))

        self.verticalLayout.addWidget(self.knob, 0, Qt.AlignHCenter)

        self.knob_name = EditableLabelWidget(KnobComponent)
        self.knob_name.setObjectName(u"knob_name")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.knob_name.sizePolicy().hasHeightForWidth())
        self.knob_name.setSizePolicy(sizePolicy1)
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.knob_name.setFont(font)

        self.verticalLayout.addWidget(self.knob_name, 0, Qt.AlignHCenter)


        self.retranslateUi(KnobComponent)

        QMetaObject.connectSlotsByName(KnobComponent)
    # setupUi

    def retranslateUi(self, KnobComponent):
        KnobComponent.setWindowTitle(QCoreApplication.translate("KnobComponent", u"Knob Component", None))
        self.knob_name.setText(QCoreApplication.translate("KnobComponent", u"Knob", None))
    # retranslateUi

