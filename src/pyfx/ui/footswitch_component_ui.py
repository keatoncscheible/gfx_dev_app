# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'footswitch_component.ui'
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

from pyfx.widgets.editable_label_widget import EditableLabelWidget
from pyfx.widgets.footswitch import Footswitch

class Ui_FootswitchComponent(object):
    def setupUi(self, FootswitchComponent):
        if not FootswitchComponent.objectName():
            FootswitchComponent.setObjectName(u"FootswitchComponent")
        FootswitchComponent.resize(101, 69)
        self.verticalLayout = QVBoxLayout(FootswitchComponent)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.footswitch = Footswitch(FootswitchComponent)
        self.footswitch.setObjectName(u"footswitch")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.footswitch.sizePolicy().hasHeightForWidth())
        self.footswitch.setSizePolicy(sizePolicy)
        self.footswitch.setMinimumSize(QSize(0, 0))
        self.footswitch.setMaximumSize(QSize(16777215, 16777215))
        self.footswitch.setCheckable(True)
        self.footswitch.setAutoDefault(False)
        self.footswitch.setFlat(False)

        self.verticalLayout.addWidget(self.footswitch, 0, Qt.AlignHCenter)

        self.footswitch_name = EditableLabelWidget(FootswitchComponent)
        self.footswitch_name.setObjectName(u"footswitch_name")
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.footswitch_name.setFont(font)

        self.verticalLayout.addWidget(self.footswitch_name, 0, Qt.AlignHCenter)


        self.retranslateUi(FootswitchComponent)
        self.footswitch.clicked["bool"].connect(FootswitchComponent.footswitch_toggled)

        self.footswitch.setDefault(False)


        QMetaObject.connectSlotsByName(FootswitchComponent)
    # setupUi

    def retranslateUi(self, FootswitchComponent):
        FootswitchComponent.setWindowTitle(QCoreApplication.translate("FootswitchComponent", u"FootswitchComponent", None))
        self.footswitch.setText("")
        self.footswitch_name.setText(QCoreApplication.translate("FootswitchComponent", u"Footswitch", None))
    # retranslateUi

