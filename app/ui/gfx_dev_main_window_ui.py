# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gfx_dev_main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QMainWindow, QMenu,
    QMenuBar, QSizePolicy, QSpacerItem, QStatusBar,
    QVBoxLayout, QWidget)

from widgets.transport_control_widget import TransportControlWidget

class Ui_GfxDevMainWindow(object):
    def setupUi(self, GfxDevMainWindow):
        if not GfxDevMainWindow.objectName():
            GfxDevMainWindow.setObjectName(u"GfxDevMainWindow")
        GfxDevMainWindow.resize(391, 230)
        self.action_about = QAction(GfxDevMainWindow)
        self.action_about.setObjectName(u"action_about")
        self.action_new_pedal = QAction(GfxDevMainWindow)
        self.action_new_pedal.setObjectName(u"action_new_pedal")
        self.action_open_pedal = QAction(GfxDevMainWindow)
        self.action_open_pedal.setObjectName(u"action_open_pedal")
        self.action_save_pedal = QAction(GfxDevMainWindow)
        self.action_save_pedal.setObjectName(u"action_save_pedal")
        self.action_quit = QAction(GfxDevMainWindow)
        self.action_quit.setObjectName(u"action_quit")
        self.action_close_pedal = QAction(GfxDevMainWindow)
        self.action_close_pedal.setObjectName(u"action_close_pedal")
        self.central_widget = QWidget(GfxDevMainWindow)
        self.central_widget.setObjectName(u"central_widget")
        self.verticalLayout = QVBoxLayout(self.central_widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(20, 10, 20, 0)
        self.transport_control = TransportControlWidget(self.central_widget)
        self.transport_control.setObjectName(u"transport_control")
        self.transport_control.setMinimumSize(QSize(350, 125))

        self.verticalLayout.addWidget(self.transport_control, 0, Qt.AlignHCenter)

        self.pedal_layout = QHBoxLayout()
        self.pedal_layout.setSpacing(0)
        self.pedal_layout.setObjectName(u"pedal_layout")
        self.pedal_layout.setContentsMargins(20, 20, 20, 20)
        self.pedal_layout_spacer_left = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.pedal_layout.addItem(self.pedal_layout_spacer_left)

        self.pedal_widget = QWidget(self.central_widget)
        self.pedal_widget.setObjectName(u"pedal_widget")
        self.pedal_widget.setMinimumSize(QSize(0, 0))

        self.pedal_layout.addWidget(self.pedal_widget)

        self.pedal_layout_spacer_right = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.pedal_layout.addItem(self.pedal_layout_spacer_right)


        self.verticalLayout.addLayout(self.pedal_layout)

        self.vertical_spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.verticalLayout.addItem(self.vertical_spacer)

        GfxDevMainWindow.setCentralWidget(self.central_widget)
        self.menubar = QMenuBar(GfxDevMainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 391, 22))
        self.menu_help = QMenu(self.menubar)
        self.menu_help.setObjectName(u"menu_help")
        self.menu_file = QMenu(self.menubar)
        self.menu_file.setObjectName(u"menu_file")
        GfxDevMainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(GfxDevMainWindow)
        self.statusbar.setObjectName(u"statusbar")
        GfxDevMainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu_file.menuAction())
        self.menubar.addAction(self.menu_help.menuAction())
        self.menu_help.addAction(self.action_about)
        self.menu_file.addAction(self.action_new_pedal)
        self.menu_file.addAction(self.action_open_pedal)
        self.menu_file.addAction(self.action_close_pedal)
        self.menu_file.addAction(self.action_save_pedal)
        self.menu_file.addAction(self.action_quit)
        self.menu_file.addSeparator()

        self.retranslateUi(GfxDevMainWindow)
        self.action_about.triggered.connect(GfxDevMainWindow.help__about_cb)
        self.action_new_pedal.triggered.connect(GfxDevMainWindow.file__new_pedal_cb)
        self.action_open_pedal.triggered.connect(GfxDevMainWindow.file__open_pedal_cb)
        self.action_save_pedal.triggered.connect(GfxDevMainWindow.file__save_pedal_cb)
        self.action_quit.triggered.connect(GfxDevMainWindow.file__quit_cb)
        self.action_close_pedal.triggered.connect(GfxDevMainWindow.file__close_pedal_cb)

        QMetaObject.connectSlotsByName(GfxDevMainWindow)
    # setupUi

    def retranslateUi(self, GfxDevMainWindow):
        GfxDevMainWindow.setWindowTitle(QCoreApplication.translate("GfxDevMainWindow", u"GFX Dev App", None))
        self.action_about.setText(QCoreApplication.translate("GfxDevMainWindow", u"About", None))
#if QT_CONFIG(shortcut)
        self.action_about.setShortcut(QCoreApplication.translate("GfxDevMainWindow", u"Ctrl+Shift+/", None))
#endif // QT_CONFIG(shortcut)
        self.action_new_pedal.setText(QCoreApplication.translate("GfxDevMainWindow", u"New Pedal", None))
#if QT_CONFIG(shortcut)
        self.action_new_pedal.setShortcut(QCoreApplication.translate("GfxDevMainWindow", u"Ctrl+N", None))
#endif // QT_CONFIG(shortcut)
        self.action_open_pedal.setText(QCoreApplication.translate("GfxDevMainWindow", u"Open Pedal", None))
#if QT_CONFIG(shortcut)
        self.action_open_pedal.setShortcut(QCoreApplication.translate("GfxDevMainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.action_save_pedal.setText(QCoreApplication.translate("GfxDevMainWindow", u"Save Pedal", None))
#if QT_CONFIG(shortcut)
        self.action_save_pedal.setShortcut(QCoreApplication.translate("GfxDevMainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.action_quit.setText(QCoreApplication.translate("GfxDevMainWindow", u"Quit", None))
#if QT_CONFIG(shortcut)
        self.action_quit.setShortcut(QCoreApplication.translate("GfxDevMainWindow", u"Ctrl+Q", None))
#endif // QT_CONFIG(shortcut)
        self.action_close_pedal.setText(QCoreApplication.translate("GfxDevMainWindow", u"Close Pedal", None))
#if QT_CONFIG(shortcut)
        self.action_close_pedal.setShortcut(QCoreApplication.translate("GfxDevMainWindow", u"Ctrl+Shift+Q", None))
#endif // QT_CONFIG(shortcut)
        self.menu_help.setTitle(QCoreApplication.translate("GfxDevMainWindow", u"Help", None))
        self.menu_file.setTitle(QCoreApplication.translate("GfxDevMainWindow", u"File", None))
    # retranslateUi

