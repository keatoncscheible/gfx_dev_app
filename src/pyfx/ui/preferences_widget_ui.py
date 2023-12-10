# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'preferences_widget.ui'
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
from PySide6.QtWidgets import (QApplication, QSizePolicy, QTabWidget, QVBoxLayout,
    QWidget)

from pyfx.widgets.audio_preferences_widget import AudioPreferencesWidget

class Ui_PreferencesWidget(object):
    def setupUi(self, PreferencesWidget):
        if not PreferencesWidget.objectName():
            PreferencesWidget.setObjectName(u"PreferencesWidget")
        PreferencesWidget.resize(400, 300)
        self.verticalLayout = QVBoxLayout(PreferencesWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.preferences_tab_widget = QTabWidget(PreferencesWidget)
        self.preferences_tab_widget.setObjectName(u"preferences_tab_widget")
        self.audio_preferences = AudioPreferencesWidget()
        self.audio_preferences.setObjectName(u"audio_preferences")
        self.preferences_tab_widget.addTab(self.audio_preferences, "")

        self.verticalLayout.addWidget(self.preferences_tab_widget)


        self.retranslateUi(PreferencesWidget)

        self.preferences_tab_widget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(PreferencesWidget)
    # setupUi

    def retranslateUi(self, PreferencesWidget):
        PreferencesWidget.setWindowTitle(QCoreApplication.translate("PreferencesWidget", u"Preferences", None))
        self.preferences_tab_widget.setTabText(self.preferences_tab_widget.indexOf(self.audio_preferences), QCoreApplication.translate("PreferencesWidget", u"Audio", None))
    # retranslateUi

