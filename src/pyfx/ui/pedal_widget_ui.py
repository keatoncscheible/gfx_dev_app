# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pedal_widget.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QLayout,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

from pyfx.widgets.editable_label_widget import EditableLabelWidget

class Ui_PedalWidget(object):
    def setupUi(self, PedalWidget):
        if not PedalWidget.objectName():
            PedalWidget.setObjectName(u"PedalWidget")
        PedalWidget.resize(219, 340)
        PedalWidget.setMaximumSize(QSize(16777215, 16777215))
        PedalWidget.setFocusPolicy(Qt.ClickFocus)
        self.verticalLayout = QVBoxLayout(PedalWidget)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(20, 40, 20, 20)
        self.pedal_name_label = EditableLabelWidget(PedalWidget)
        self.pedal_name_label.setObjectName(u"pedal_name_label")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pedal_name_label.sizePolicy().hasHeightForWidth())
        self.pedal_name_label.setSizePolicy(sizePolicy)
        self.pedal_name_label.setMinimumSize(QSize(0, 40))
        self.pedal_name_label.setMaximumSize(QSize(16777215, 40))
        font = QFont()
        font.setPointSize(24)
        font.setBold(True)
        self.pedal_name_label.setFont(font)

        self.verticalLayout.addWidget(self.pedal_name_label, 0, Qt.AlignHCenter)

        self.knob_layout = QGridLayout()
        self.knob_layout.setSpacing(10)
        self.knob_layout.setObjectName(u"knob_layout")
        self.knob_layout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.knob_layout.setContentsMargins(20, 0, 20, 60)

        self.verticalLayout.addLayout(self.knob_layout)

        self.footswitch_layout = QGridLayout()
        self.footswitch_layout.setSpacing(10)
        self.footswitch_layout.setObjectName(u"footswitch_layout")
        self.footswitch_layout.setContentsMargins(20, -1, 20, 20)

        self.verticalLayout.addLayout(self.footswitch_layout)

        self.verticalSpacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Maximum)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(PedalWidget)

        QMetaObject.connectSlotsByName(PedalWidget)
    # setupUi

    def retranslateUi(self, PedalWidget):
        PedalWidget.setWindowTitle(QCoreApplication.translate("PedalWidget", u"Frame", None))
        self.pedal_name_label.setText(QCoreApplication.translate("PedalWidget", u"Pedal Name", None))
    # retranslateUi

