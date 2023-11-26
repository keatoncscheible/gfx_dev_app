# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pedal_builder_main_window.ui'
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

from pyfx.widgets.transport_control_widget import TransportControlWidget

class Ui_PedalBuilderMainWindow(object):
    def setupUi(self, PedalBuilderMainWindow):
        if not PedalBuilderMainWindow.objectName():
            PedalBuilderMainWindow.setObjectName(u"PedalBuilderMainWindow")
        PedalBuilderMainWindow.resize(391, 230)
        self.action_about = QAction(PedalBuilderMainWindow)
        self.action_about.setObjectName(u"action_about")
        self.action_new_pedal = QAction(PedalBuilderMainWindow)
        self.action_new_pedal.setObjectName(u"action_new_pedal")
        self.action_open_pedal = QAction(PedalBuilderMainWindow)
        self.action_open_pedal.setObjectName(u"action_open_pedal")
        self.action_save_pedal = QAction(PedalBuilderMainWindow)
        self.action_save_pedal.setObjectName(u"action_save_pedal")
        self.action_quit = QAction(PedalBuilderMainWindow)
        self.action_quit.setObjectName(u"action_quit")
        self.action_close_pedal = QAction(PedalBuilderMainWindow)
        self.action_close_pedal.setObjectName(u"action_close_pedal")
        self.action_add_knob = QAction(PedalBuilderMainWindow)
        self.action_add_knob.setObjectName(u"action_add_knob")
        self.action_add_footswitch = QAction(PedalBuilderMainWindow)
        self.action_add_footswitch.setObjectName(u"action_add_footswitch")
        self.action_knob_displays = QAction(PedalBuilderMainWindow)
        self.action_knob_displays.setObjectName(u"action_knob_displays")
        self.action_knob_displays.setCheckable(True)
        self.action_footswitch_displays = QAction(PedalBuilderMainWindow)
        self.action_footswitch_displays.setObjectName(u"action_footswitch_displays")
        self.action_footswitch_displays.setCheckable(True)
        self.central_widget = QWidget(PedalBuilderMainWindow)
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

        self.vertical_spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)

        self.verticalLayout.addItem(self.vertical_spacer)

        PedalBuilderMainWindow.setCentralWidget(self.central_widget)
        self.menubar = QMenuBar(PedalBuilderMainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 391, 22))
        self.menu_help = QMenu(self.menubar)
        self.menu_help.setObjectName(u"menu_help")
        self.menu_file = QMenu(self.menubar)
        self.menu_file.setObjectName(u"menu_file")
        self.menu_pedal = QMenu(self.menubar)
        self.menu_pedal.setObjectName(u"menu_pedal")
        self.menu_view = QMenu(self.menubar)
        self.menu_view.setObjectName(u"menu_view")
        PedalBuilderMainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(PedalBuilderMainWindow)
        self.statusbar.setObjectName(u"statusbar")
        PedalBuilderMainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu_file.menuAction())
        self.menubar.addAction(self.menu_pedal.menuAction())
        self.menubar.addAction(self.menu_view.menuAction())
        self.menubar.addAction(self.menu_help.menuAction())
        self.menu_help.addAction(self.action_about)
        self.menu_file.addAction(self.action_new_pedal)
        self.menu_file.addAction(self.action_open_pedal)
        self.menu_file.addAction(self.action_close_pedal)
        self.menu_file.addAction(self.action_save_pedal)
        self.menu_file.addAction(self.action_quit)
        self.menu_file.addSeparator()
        self.menu_pedal.addAction(self.action_add_knob)
        self.menu_pedal.addAction(self.action_add_footswitch)
        self.menu_view.addAction(self.action_knob_displays)
        self.menu_view.addAction(self.action_footswitch_displays)

        self.retranslateUi(PedalBuilderMainWindow)
        self.action_about.triggered.connect(PedalBuilderMainWindow.help__about_cb)
        self.action_new_pedal.triggered.connect(PedalBuilderMainWindow.file__new_pedal_cb)
        self.action_open_pedal.triggered.connect(PedalBuilderMainWindow.file__open_pedal_cb)
        self.action_save_pedal.triggered.connect(PedalBuilderMainWindow.file__save_pedal_cb)
        self.action_quit.triggered.connect(PedalBuilderMainWindow.file__quit_cb)
        self.action_close_pedal.triggered.connect(PedalBuilderMainWindow.file__close_pedal_cb)
        self.action_add_knob.triggered.connect(PedalBuilderMainWindow.pedal__add_knob_cb)
        self.action_add_footswitch.triggered.connect(PedalBuilderMainWindow.pedal__add_footswitch_cb)
        self.action_knob_displays.toggled.connect(PedalBuilderMainWindow.view__knob_displays_cb)
        self.action_footswitch_displays.toggled.connect(PedalBuilderMainWindow.view__footswitch_displays_cb)

        QMetaObject.connectSlotsByName(PedalBuilderMainWindow)
    # setupUi

    def retranslateUi(self, PedalBuilderMainWindow):
        PedalBuilderMainWindow.setWindowTitle(QCoreApplication.translate("PedalBuilderMainWindow", u"Pedal Builder", None))
        self.action_about.setText(QCoreApplication.translate("PedalBuilderMainWindow", u"About", None))
#if QT_CONFIG(shortcut)
        self.action_about.setShortcut(QCoreApplication.translate("PedalBuilderMainWindow", u"Ctrl+Shift+/", None))
#endif // QT_CONFIG(shortcut)
        self.action_new_pedal.setText(QCoreApplication.translate("PedalBuilderMainWindow", u"New Pedal", None))
#if QT_CONFIG(shortcut)
        self.action_new_pedal.setShortcut(QCoreApplication.translate("PedalBuilderMainWindow", u"Ctrl+N", None))
#endif // QT_CONFIG(shortcut)
        self.action_open_pedal.setText(QCoreApplication.translate("PedalBuilderMainWindow", u"Open Pedal", None))
#if QT_CONFIG(shortcut)
        self.action_open_pedal.setShortcut(QCoreApplication.translate("PedalBuilderMainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.action_save_pedal.setText(QCoreApplication.translate("PedalBuilderMainWindow", u"Save Pedal", None))
#if QT_CONFIG(shortcut)
        self.action_save_pedal.setShortcut(QCoreApplication.translate("PedalBuilderMainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.action_quit.setText(QCoreApplication.translate("PedalBuilderMainWindow", u"Quit", None))
#if QT_CONFIG(shortcut)
        self.action_quit.setShortcut(QCoreApplication.translate("PedalBuilderMainWindow", u"Ctrl+Q", None))
#endif // QT_CONFIG(shortcut)
        self.action_close_pedal.setText(QCoreApplication.translate("PedalBuilderMainWindow", u"Close Pedal", None))
#if QT_CONFIG(shortcut)
        self.action_close_pedal.setShortcut(QCoreApplication.translate("PedalBuilderMainWindow", u"Ctrl+Shift+Q", None))
#endif // QT_CONFIG(shortcut)
        self.action_add_knob.setText(QCoreApplication.translate("PedalBuilderMainWindow", u"Add Knob", None))
#if QT_CONFIG(shortcut)
        self.action_add_knob.setShortcut(QCoreApplication.translate("PedalBuilderMainWindow", u"Ctrl+1", None))
#endif // QT_CONFIG(shortcut)
        self.action_add_footswitch.setText(QCoreApplication.translate("PedalBuilderMainWindow", u"Add Footswitch", None))
#if QT_CONFIG(shortcut)
        self.action_add_footswitch.setShortcut(QCoreApplication.translate("PedalBuilderMainWindow", u"Ctrl+2", None))
#endif // QT_CONFIG(shortcut)
        self.action_knob_displays.setText(QCoreApplication.translate("PedalBuilderMainWindow", u"Knob Displays", None))
#if QT_CONFIG(shortcut)
        self.action_knob_displays.setShortcut(QCoreApplication.translate("PedalBuilderMainWindow", u"Ctrl+K", None))
#endif // QT_CONFIG(shortcut)
        self.action_footswitch_displays.setText(QCoreApplication.translate("PedalBuilderMainWindow", u"Footswitch Displays", None))
#if QT_CONFIG(shortcut)
        self.action_footswitch_displays.setShortcut(QCoreApplication.translate("PedalBuilderMainWindow", u"Ctrl+F", None))
#endif // QT_CONFIG(shortcut)
        self.menu_help.setTitle(QCoreApplication.translate("PedalBuilderMainWindow", u"Help", None))
        self.menu_file.setTitle(QCoreApplication.translate("PedalBuilderMainWindow", u"File", None))
        self.menu_pedal.setTitle(QCoreApplication.translate("PedalBuilderMainWindow", u"Pedal", None))
        self.menu_view.setTitle(QCoreApplication.translate("PedalBuilderMainWindow", u"View", None))
    # retranslateUi

