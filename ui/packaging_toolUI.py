# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'packaging_toolUI.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(891, 620)
        font = QFont()
        font.setFamily(u"Microsoft YaHei")
        font.setBold(False)
        font.setWeight(50)
        MainWindow.setFont(font)
        MainWindow.setStyleSheet(u"\n"
"QWidget\n"
"{\n"
"    color: rgb(0, 0, 0);\n"
"    background-color:white;\n"
"}\n"
"\n"
"QWidget:item:hover\n"
"{\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #D1DBCB, stop: 1 #b2b6af);\n"
"    color: #000000;\n"
"}\n"
"\n"
"QWidget:item:selected\n"
"{\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #D1DBCB, stop: 1 #b2b6af);\n"
"}\n"
"\n"
"\n"
"QWidget:disabled\n"
"{\n"
"    color: #404040;\n"
"    background-color: #323232;\n"
"}\n"
"\n"
"QAbstractItemView\n"
"{\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #4d4d4d, stop: 0.1 #646464, stop: 1 #5d5d5d);\n"
"}\n"
"\n"
"QWidget:focus\n"
"{\n"
"    /*border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0\n"
"     #D1DBCB, stop: 1 #b2b6af);*/\n"
"}\n"
"\n"
"QLineEdit\n"
"{\n"
"    background-color:transparent;\n"
"    padding: 1px;\n"
"    border-style: solid;\n"
"    border: 2px solid rgb(85, 170, 255);\n"
"    border-radius: 5;\n"
"}\n"
"\n"
""
                        "QLineEdit:hover{\n"
"	border: 3px solid\n"
"\n"
"}\n"
"\n"
"QPushButton\n"
"{\n"
"    color: black;\n"
"    background-color: transparent;\n"
"    border-width: 2px;\n"
"    border-color: rgb(85, 170, 255);\n"
"    border-style: solid;\n"
"    border-radius: 6;\n"
"    padding: 3px;\n"
"    font-size: 12px;\n"
"    padding-left: 5px;\n"
"    padding-right: 5px;\n"
"}\n"
"\n"
"QPushButton:pressed\n"
"{\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d2d, stop: 0.1 #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252525);\n"
"}\n"
"\n"
"\n"
"QPushButton:disabled\n"
"{\n"
"    border-color:transparent;\n"
"    background-color: transparent;\n"
"	color : transparent;\n"
"}\n"
"\n"
"\n"
"\n"
"QComboBox\n"
"{\n"
"    selection-background-color: #fdf6e3;\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1 #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646);\n"
"    border-style: solid;\n"
"    border: 1px solid #1e1e1e"
                        ";\n"
"    border-radius: 5;\n"
"}\n"
"\n"
"QComboBox:hover,QPushButton:hover\n"
"{\n"
"    border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0\n"
"    #D1DBCB, stop: 1 #b2b6af);\n"
"}\n"
"\n"
"\n"
"QComboBox:on\n"
"{\n"
"    padding-top: 3px;\n"
"    padding-left: 4px;\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d2d, stop: 0.1 #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252525);\n"
"    selection-background-color: #fdf6e3;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView\n"
"{\n"
"    border: 2px solid darkgray;\n"
"    selection-background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1,\n"
"     stop: 0 #D1DBCB, stop: 1 #b2b6af);\n"
"}\n"
"\n"
"QComboBox::drop-down\n"
"{\n"
"     subcontrol-origin: padding;\n"
"     subcontrol-position: top right;\n"
"     width: 15px;\n"
"\n"
"     border-left-width: 0px;\n"
"     border-left-color: darkgray;\n"
"     border-left-style: solid; /* just a single line */\n"
"     border-top-right-radius: 3px; /"
                        "* same radius as the QComboBox */\n"
"     border-bottom-right-radius: 3px;\n"
" }\n"
"\n"
"QComboBox::down-arrow\n"
"{\n"
"     image: url(:/down_arrow.png);\n"
"}\n"
"\n"
"QGroupBox:focus\n"
"{\n"
"border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0\n"
"#D1DBCB, stop: 1 #b2b6af);\n"
"}\n"
"\n"
"QTextEdit:focus\n"
"{\n"
"    border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0\n"
"    #D1DBCB, stop: 1 #b2b6af);\n"
"}\n"
"\n"
"QScrollArea:focus {\n"
"border: 1px solid black;\n"
"}\n"
"\n"
"QScrollBar:horizontal {\n"
"     border: 1px solid #222222;\n"
"     background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0.0 #121212, stop: 0.2 #282828, stop: 1 #484848);\n"
"     height: 7px;\n"
"     margin: 0px 16px 0 16px;\n"
"}\n"
"\n"
"QScrollBar::handle:horizontal\n"
"{\n"
"      background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0\n"
"      #D1DBCB, stop: 0.5 #b2b6af, stop: 1 #D1DBCB);\n"
"      min-height: 20px;\n"
"      border-radius: 2px;\n"
"}\n"
"\n"
""
                        "QScrollBar::add-line:horizontal {\n"
"      border: 1px solid #1b1b19;\n"
"      border-radius: 2px;\n"
"      background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0\n"
"      #D1DBCB, stop: 1 #b2b6af);\n"
"      width: 14px;\n"
"      subcontrol-position: right;\n"
"      subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::sub-line:horizontal {\n"
"      border: 1px solid #1b1b19;\n"
"      border-radius: 2px;\n"
"      background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0\n"
"      #D1DBCB, stop: 1 #b2b6af);\n"
"      width: 14px;\n"
"     subcontrol-position: left;\n"
"     subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::right-arrow:horizontal, QScrollBar::left-arrow:horizontal\n"
"{\n"
"      border: 1px solid black;\n"
"      width: 1px;\n"
"      height: 1px;\n"
"      background: white;\n"
"}\n"
"\n"
"QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal\n"
"{\n"
"      background: none;\n"
"}\n"
"\n"
"QScrollBar:vertical\n"
"{\n"
"      background: QLinearGradien"
                        "t( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0.0 #121212, stop: 0.2 #282828, stop: 1 #484848);\n"
"      width: 7px;\n"
"      margin: 16px 0 16px 0;\n"
"      border: 1px solid #222222;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical\n"
"{\n"
"      background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0\n"
"      #D1DBCB, stop: 0.5 #b2b6af, stop: 1 #D1DBCB);\n"
"      min-height: 20px;\n"
"      border-radius: 2px;\n"
"}\n"
"\n"
"QScrollBar::add-line:vertical\n"
"{\n"
"      border: 1px solid #1b1b19;\n"
"      border-radius: 2px;\n"
"      background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0\n"
"      #D1DBCB, stop: 1 #b2b6af);\n"
"      height: 14px;\n"
"      subcontrol-position: bottom;\n"
"      subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::sub-line:vertical\n"
"{\n"
"      border: 1px solid #1b1b19;\n"
"      border-radius: 2px;\n"
"      background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #b2b6af,\n"
"      stop: 1 #D1DBCB);\n"
"      height: 14px;\n"
"      subcontrol-pos"
                        "ition: top;\n"
"      subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical\n"
"{\n"
"      border: 1px solid black;\n"
"      width: 1px;\n"
"      height: 1px;\n"
"      background: white;\n"
"}\n"
"\n"
"\n"
"QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical\n"
"{\n"
"      background: none;\n"
"}\n"
"\n"
"QTextEdit\n"
"{\n"
"    background-color: transparent;\n"
"}\n"
"\n"
"QPlainTextEdit\n"
"{\n"
"    background-color: transparent;\n"
"}\n"
"\n"
"QHeaderView::section\n"
"{\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #616161, stop: 0.5 #505050, stop: 0.6 #434343, stop:1 #656565);\n"
"    color: white;\n"
"    padding-left: 4px;\n"
"    border: 1px solid #6c6c6c;\n"
"}\n"
"\n"
"QCheckBox:disabled\n"
"{\n"
"color: #414141;\n"
"}\n"
"\n"
"QDockWidget::title\n"
"{\n"
"    text-align: center;\n"
"    spacing: 3px; /* spacing between items in the tool bar */\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, "
                        "stop:0 #323232, stop: 0.5 #242424, stop:1 #323232);\n"
"}\n"
"\n"
"QDockWidget::close-button, QDockWidget::float-button\n"
"{\n"
"    text-align: center;\n"
"    spacing: 1px; /* spacing between items in the tool bar */\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #323232, stop: 0.5 #242424, stop:1 #323232);\n"
"}\n"
"\n"
"QDockWidget::close-button:hover, QDockWidget::float-button:hover\n"
"{\n"
"    background: #242424;\n"
"}\n"
"\n"
"QDockWidget::close-button:pressed, QDockWidget::float-button:pressed\n"
"{\n"
"    padding: 1px -1px -1px 1px;\n"
"}\n"
"\n"
"QMainWindow::separator\n"
"{\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #161616, stop: 0.5 #151515, stop: 0.6 #212121, stop:1 #343434);\n"
"    color: white;\n"
"    padding-left: 4px;\n"
"    border: 1px solid #4c4c4c;\n"
"    spacing: 3px; /* spacing between items in the tool bar */\n"
"}\n"
"\n"
"QMainWindow::separator:hover\n"
"{\n"
"\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, "
                        "y2:1, stop:0 #b2b6af,\n"
"    stop:0.5 #b56c17 stop:1 #D1DBCB);\n"
"    color: white;\n"
"    padding-left: 4px;\n"
"    border: 1px solid #6c6c6c;\n"
"    spacing: 3px; /* spacing between items in the tool bar */\n"
"}\n"
"\n"
"QToolBar {\n"
"    border: 1px transparent #323232;\n"
"    background: 1px solid #323232;\n"
"}\n"
"\n"
"QToolBar::handle\n"
"{\n"
"     spacing: 3px; /* spacing between items in the tool bar */\n"
"     background: url(:/images/handle.png);\n"
"}\n"
"\n"
"QMenu::separator\n"
"{\n"
"    height: 2px;\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #161616, stop: 0.5 #151515, stop: 0.6 #212121, stop:1 #343434);\n"
"    color: white;\n"
"    padding-left: 4px;\n"
"    margin-left: 10px;\n"
"    margin-right: 5px;\n"
"}\n"
"\n"
"QProgressBar\n"
"{\n"
"    border: transparent;\n"
"    border-radius: 5px;\n"
"    text-align: right;\n"
"}\n"
"\n"
"QProgressBar::chunk\n"
"{\n"
"    background-color:rgb(85, 170, 255);\n"
"    width: 2.15px;\n"
"    margin: 0.5px;\n"
"}"
                        "\n"
"\n"
"QTabBar::tab {\n"
"    color: #b1b1b1;\n"
"    border: 1px solid #444;\n"
"    border-bottom-style: none;\n"
"    background-color: #323232;\n"
"    padding-left: 10px;\n"
"    padding-right: 10px;\n"
"    padding-top: 3px;\n"
"    padding-bottom: 2px;\n"
"    margin-right: -1px;\n"
"}\n"
"\n"
"QTabWidget::pane {\n"
"    border: 1px solid #444;\n"
"    top: 1px;\n"
"}\n"
"\n"
"QTabBar::tab:last\n"
"{\n"
"    margin-right: 0; /* the last selected tab has nothing to overlap with on the right */\n"
"    border-top-right-radius: 3px;\n"
"}\n"
"\n"
"QTabBar::tab:first:!selected\n"
"{\n"
" margin-left: 0px; /* the last selected tab has nothing to overlap with on the right */\n"
"\n"
"\n"
"    border-top-left-radius: 3px;\n"
"}\n"
"\n"
"QTabBar::tab:!selected\n"
"{\n"
"    color: #b1b1b1;\n"
"    border-bottom-style: solid;\n"
"    margin-top: 3px;\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:1 #212121, stop:.4 #343434);\n"
"}\n"
"\n"
"QTabBar::tab:selected\n"
"{\n"
"    border-top"
                        "-left-radius: 3px;\n"
"    border-top-right-radius: 3px;\n"
"    margin-bottom: 0px;\n"
"}\n"
"\n"
"QTabBar::tab:!selected:hover\n"
"{\n"
"    /*border-top: 2px solid #fdf6e3;\n"
"    padding-bottom: 3px;*/\n"
"    border-top-left-radius: 3px;\n"
"    border-top-right-radius: 3px;\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:1 #212121, stop:0.4 #343434, stop:0.2 #343434, stop:0.1 #fdf6e3);\n"
"}\n"
"\n"
"QRadioButton::indicator:checked, QRadioButton::indicator:unchecked{\n"
"    color: #b1b1b1;\n"
"    background-color: #323232;\n"
"    border: 1px solid #b1b1b1;\n"
"    border-radius: 6px;\n"
"}\n"
"\n"
"QRadioButton::indicator:checked\n"
"{\n"
"    background-color: qradialgradient(\n"
"        cx: 0.5, cy: 0.5,\n"
"        fx: 0.5, fy: 0.5,\n"
"        radius: 1.0,\n"
"        stop: 0.25 #fdf6e3,\n"
"        stop: 0.3 #323232\n"
"    );\n"
"}\n"
"\n"
"QCheckBox::indicator{\n"
"    color: #b1b1b1;\n"
"    background-color: #323232;\n"
"    border: 1px solid #b1b1b1;\n"
"    width: 9"
                        "px;\n"
"    height: 9px;\n"
"}\n"
"\n"
"QRadioButton::indicator\n"
"{\n"
"    border-radius: 6px;\n"
"}\n"
"\n"
"QRadioButton::indicator:hover, QCheckBox::indicator:hover\n"
"{\n"
"    border: 1px solid #fdf6e3;\n"
"}\n"
"\n"
"QCheckBox::indicator:checked\n"
"{\n"
"    image:url(:/images/checkbox.png);\n"
"}\n"
"\n"
"QCheckBox::indicator:disabled, QRadioButton::indicator:disabled\n"
"{\n"
"    border: 1px solid #444;\n"
"}\n"
"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        font1 = QFont()
        font1.setFamily(u"Lithos Pro Regular")
        font1.setPointSize(15)
        font1.setBold(False)
        font1.setItalic(False)
        font1.setUnderline(False)
        font1.setWeight(50)
        self.label_4.setFont(font1)
        self.label_4.setScaledContents(False)
        self.label_4.setWordWrap(False)

        self.verticalLayout.addWidget(self.label_4)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.input_dir_path = QLineEdit(self.centralwidget)
        self.input_dir_path.setObjectName(u"input_dir_path")

        self.horizontalLayout_2.addWidget(self.input_dir_path)

        self.input_dir_browse_pushButton = QPushButton(self.centralwidget)
        self.input_dir_browse_pushButton.setObjectName(u"input_dir_browse_pushButton")
        self.input_dir_browse_pushButton.setMinimumSize(QSize(100, 0))
        self.input_dir_browse_pushButton.setMaximumSize(QSize(80, 16777215))
        self.input_dir_browse_pushButton.setStyleSheet(u"")

        self.horizontalLayout_2.addWidget(self.input_dir_browse_pushButton)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font1)
        self.label_6.setScaledContents(False)
        self.label_6.setWordWrap(False)

        self.verticalLayout.addWidget(self.label_6)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.output_dir_path = QLineEdit(self.centralwidget)
        self.output_dir_path.setObjectName(u"output_dir_path")

        self.horizontalLayout_5.addWidget(self.output_dir_path)

        self.output_dir_browse_pushButton = QPushButton(self.centralwidget)
        self.output_dir_browse_pushButton.setObjectName(u"output_dir_browse_pushButton")
        self.output_dir_browse_pushButton.setMinimumSize(QSize(100, 0))
        self.output_dir_browse_pushButton.setMaximumSize(QSize(80, 16777215))
        self.output_dir_browse_pushButton.setStyleSheet(u"")

        self.horizontalLayout_5.addWidget(self.output_dir_browse_pushButton)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")

        self.horizontalLayout_7.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_6.addWidget(self.label_3)

        self.show_combo = QComboBox(self.centralwidget)
        self.show_combo.addItem("")
        self.show_combo.setObjectName(u"show_combo")
        self.show_combo.setMinimumSize(QSize(100, 0))
        self.show_combo.setMaximumSize(QSize(100, 16777215))
        self.show_combo.setStyleSheet(u"background-color: rgb(85, 170, 255);\n"
"color: rgb(0, 0, 0);")

        self.horizontalLayout_6.addWidget(self.show_combo)


        self.horizontalLayout_7.addLayout(self.horizontalLayout_6)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_7.addWidget(self.label_2)

        self.comboBox = QComboBox(self.centralwidget)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setMinimumSize(QSize(100, 0))
        self.comboBox.setMaximumSize(QSize(80, 16777215))
        self.comboBox.setStyleSheet(u"background-color: rgb(85, 170, 255);\n"
"color: rgb(0, 0, 0);")

        self.horizontalLayout_7.addWidget(self.comboBox)

        self.checkBox = QCheckBox(self.centralwidget)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setLayoutDirection(Qt.RightToLeft)

        self.horizontalLayout_7.addWidget(self.checkBox)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout_7)

        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.dir_treeWidget = QTreeWidget(self.splitter)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.dir_treeWidget.setHeaderItem(__qtreewidgetitem)
        self.dir_treeWidget.setObjectName(u"dir_treeWidget")
        self.dir_treeWidget.setMinimumSize(QSize(0, 0))
        self.dir_treeWidget.setMaximumSize(QSize(300, 16777215))
        self.dir_treeWidget.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.dir_treeWidget.setAlternatingRowColors(False)
        self.dir_treeWidget.setSelectionMode(QAbstractItemView.MultiSelection)
        self.dir_treeWidget.setUniformRowHeights(True)
        self.dir_treeWidget.setAnimated(True)
        self.splitter.addWidget(self.dir_treeWidget)
        self.dir_treeWidget.header().setVisible(False)
        self.log_textEdit = QTextEdit(self.splitter)
        self.log_textEdit.setObjectName(u"log_textEdit")
        self.log_textEdit.setMinimumSize(QSize(0, 400))
        self.log_textEdit.setTabStopWidth(80)
        self.splitter.addWidget(self.log_textEdit)

        self.verticalLayout.addWidget(self.splitter)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.image_progressBar = QProgressBar(self.centralwidget)
        self.image_progressBar.setObjectName(u"image_progressBar")
        self.image_progressBar.setMaximumSize(QSize(16777215, 10))
        self.image_progressBar.setValue(0)

        self.horizontalLayout.addWidget(self.image_progressBar)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.cancel_pushButton = QPushButton(self.centralwidget)
        self.cancel_pushButton.setObjectName(u"cancel_pushButton")
        self.cancel_pushButton.setStyleSheet(u"")

        self.horizontalLayout_3.addWidget(self.cancel_pushButton)

        self.remove_dir_pushButton = QPushButton(self.centralwidget)
        self.remove_dir_pushButton.setObjectName(u"remove_dir_pushButton")
        self.remove_dir_pushButton.setStyleSheet(u"")

        self.horizontalLayout_3.addWidget(self.remove_dir_pushButton)

        self.validate_pushButton = QPushButton(self.centralwidget)
        self.validate_pushButton.setObjectName(u"validate_pushButton")
        self.validate_pushButton.setStyleSheet(u"")

        self.horizontalLayout_3.addWidget(self.validate_pushButton)

        self.create_pushButton = QPushButton(self.centralwidget)
        self.create_pushButton.setObjectName(u"create_pushButton")

        self.horizontalLayout_3.addWidget(self.create_pushButton)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Packager", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Input path", None))
        self.input_dir_path.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Click on browse button to load the source path", None))
        self.input_dir_browse_pushButton.setText(QCoreApplication.translate("MainWindow", u"browse", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Output  path", None))
        self.output_dir_path.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Click on browse button to load the source path", None))
        self.output_dir_browse_pushButton.setText(QCoreApplication.translate("MainWindow", u"browse", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Show", None))
        self.show_combo.setItemText(0, QCoreApplication.translate("MainWindow", u"Select", None))

        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Department", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Select", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"roto", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"paint", None))

        self.checkBox.setText(QCoreApplication.translate("MainWindow", u"Expand", None))
        self.log_textEdit.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.cancel_pushButton.setText(QCoreApplication.translate("MainWindow", u"cancel", None))
        self.remove_dir_pushButton.setText(QCoreApplication.translate("MainWindow", u"Reset", None))
        self.validate_pushButton.setText(QCoreApplication.translate("MainWindow", u"Validate ", None))
        self.create_pushButton.setText(QCoreApplication.translate("MainWindow", u"Publish", None))
    # retranslateUi

