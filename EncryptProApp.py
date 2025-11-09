import sys
import os
import traceback

from PyQt5 import QtCore, QtGui, QtWidgets
import logging
from algorithms import CaesarCipher, Rot13Cipher, PlayfairCipher, RailFenceCipher, RowTranspositionCipher, HillCipher, SubstitutionCipher, VigenereCipher, AESCipher, ChrisWayV1Cipher, ChrisWayV2Cipher
import random
import string
import secrets
import math
import base64

# Helper to load icons with fallback
ICON_COLORS = {
    'lock': '#4EC2F7',
    'caesar': '#FFB347',
    'playfair': '#FF6961',
    'railfence': '#A3A1FB',
    'rowtrans': '#77DD77',
    'hill': '#F49AC2',
    'substitution': '#FFD700',
    'vigenere': '#779ECB',
    'rsa': '#C23B22',
    'aes': '#03C03C',
    'rot13': '#836953',
    'favorite': '#FF69B4',
    'info': '#4EC2F7',
    'close': '#FF6961',
    'encrypt': '#4464AD',
    'decrypt': '#4CAF50',
    'load': '#4EC2F7',
    'delete': '#FF6961',
    'dark_mode': '#22223B',
    'light_mode': '#F7F7F7',
    'new': '#4EC2F7',
    'save': '#FFD700',
    'history': '#A3A1FB',
    'help': '#FFD700',
    'settings': '#A3A1FB',
    'clear': '#FFB347',
    'load_file': '#4EC2F7',
    'generate': '#03C03C',
    'copy': '#FFD700',
    'save_file': '#FFD700',
    'browse': '#4EC2F7',
    'files_tab': '#A3A1FB',
    'export': '#FFD700',
    'stars3': '#FFD700',
    'checkmark': '#4CAF50',
    'dropdown': '#4EC2F7',
    'arrow_up': '#4EC2F7',
    'arrow_down': '#4EC2F7',
    'eye': '#4EC2F7',
    'eye_crossed': '#FF6961',
}

def load_icon(name, size=24, force_letter=False):
    path = os.path.join('icons', f'{name}.png')
    if os.path.exists(path) and not force_letter:
        return QtGui.QIcon(path)
    # Draw a colored placeholder pixmap with a letter
    color = ICON_COLORS.get(name, '#888888')
    pixmap = QtGui.QPixmap(size, size)
    pixmap.fill(QtGui.QColor(color))
    painter = QtGui.QPainter(pixmap)
    painter.setPen(QtCore.Qt.white)
    font = QtGui.QFont('Arial', int(size/2))
    font.setBold(True)
    painter.setFont(font)
    painter.drawText(pixmap.rect(), QtCore.Qt.AlignCenter, name[0].upper())
    painter.end()
    return QtGui.QIcon(pixmap)

# ----------------------------------------------------------------------
# UI Definition Class (Generated from your XML)
# ----------------------------------------------------------------------
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1136, 814)
        MainWindow.setMinimumSize(QtCore.QSize(1100, 750))
        MainWindow.setWindowIcon(load_icon('lock'))
        MainWindow.setStyleSheet("""
QMainWindow, QWidget {
background-color: #121212;
color: #EEEEEE;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 13px;
}

QFrame, QGroupBox, QTabWidget::pane {
background-color: #1E1E1E;
    border-radius: 12px;
border: 1px solid #2A2A2A;
}

QPushButton {
background-color: #2A2A2A;
color: #EEEEEE;
    border: none;
    border-radius: 8px;
    padding: 10px 18px;
    font-weight: 600;
}

QPushButton:hover {
background-color: #3A3A3A;
}

QPushButton:pressed {
background-color: #454545;
}

QPushButton#execute_operation_btn {
    background-color: #4464AD;
    color: white;
    font-size: 15px;
    border-radius: 10px;
min-height: 48px;
margin: 5px 0;
background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4464AD, stop:1 #5575BE);
}

QPushButton#execute_operation_btn:hover {
background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #5575BE, stop:1 #6686CF);
}

QPushButton#execute_operation_btn.decrypt {
background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4CAF50, stop:1 #5DBF61);
}

QPushButton#execute_operation_btn.decrypt:hover {
background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #5DBF61, stop:1 #6ECF72);
}

QListWidget, QTableWidget {
background-color: #1E1E1E;
color: #EEEEEE;
    border-radius: 8px;
border: 1px solid #2A2A2A;
    padding: 6px;
}

QListWidget::item, QTableWidget::item {
    border-radius: 4px;
    padding: 4px 6px;
    margin: 2px 0;
}

    QListWidget::item:selected, QTableWidget::item:selected {
        background-color: #4464AD;
        color: white;
    }

QListWidget::item:hover, QTableWidget::item:hover {
    background-color: #2A2A2A;
}

    QTextEdit, QLineEdit {
    background-color: #1A1A1A;
    color: #EEEEEE;
    border: 1px solid #2A2A2A;
        border-radius: 8px;
    padding: 10px;
    selection-background-color: #4464AD;
    selection-color: white;
    }

QTextEdit:focus, QLineEdit:focus {
    border: 1px solid #4464AD;
}

    QLabel#app_title {
        color: #4EC2F7;
        font-size: 24px;
        font-weight: bold;
    margin-bottom: 10px;
    }

    QLabel#section_title {
        color: #4EC2F7;
        font-size: 15px;
        font-weight: bold;
    margin-top: 10px;
}

QLabel#input_label, QLabel#output_label {
    color: #4EC2F7;
    font-size: 16px;
    font-weight: bold;
    margin-bottom: 5px;
}

    QProgressBar {
    border: none;
        border-radius: 8px;
    background-color: #1A1A1A;
    height: 10px;
    text-align: center;
    }

    QProgressBar::chunk {
    background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #FF5858, stop:0.5 #FFDE59, stop:1 #4EC2F7);
    border-radius: 8px;
    }

    QTabBar::tab {
    background-color: #1E1E1E;
    color: #EEEEEE;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    padding: 12px 20px;
    margin-right: 4px;
    font-weight: 500;
}

    QTabBar::tab:selected {
        background-color: #4464AD;
    }

    QTabBar::tab:hover:!selected {
    background-color: #2A2A2A;
    }

    QMenuBar, QStatusBar, QToolBar {
    background-color: #121212;
    color: #EEEEEE;
    }

    QMenu {
    background-color: #1E1E1E;
    border: 1px solid #2A2A2A;
    border-radius: 4px;
    }

QMenu::item {
    padding: 5px 20px;
}

    QMenu::item:selected {
        background-color: #4464AD;
    }

    QRadioButton, QCheckBox {
        padding: 6px;
    spacing: 8px;
    }

    QRadioButton::indicator, QCheckBox::indicator {
        width: 18px;
        height: 18px;
    }

QRadioButton::indicator {
    border-radius: 9px;
    border: 2px solid #777777;
    background-color: #1E1E1E;
}

QRadioButton::indicator:checked {
    background-color: #4464AD;
    border: 2px solid #4464AD;
    image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iMTIiIHZpZXdCb3g9IjAgMCAxMiAxMiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48Y2lyY2xlIGN4PSI2IiBjeT0iNiIgcj0iNCIgZmlsbD0id2hpdGUiLz48L3N2Zz4K);
}

    QCheckBox::indicator {
        border-radius: 4px;
    border: 2px solid #777777;
    background-color: #1E1E1E;
    }

    QCheckBox::indicator:checked {
        background-color: #4464AD;
    border: 2px solid #4464AD;
    image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iMTIiIHZpZXdCb3g9IjAgMCAxMiAxMiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cGF0aCBkPSJNMTAgM0w1IDhMMiA1IiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIvPjwvc3ZnPgo=);
}

QScrollBar:vertical {
    border: none;
    background-color: #1A1A1A;
    width: 10px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background-color: #2A2A2A;
    border-radius: 5px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #3A3A3A;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    border: none;
    background-color: #1A1A1A;
    height: 10px;
    margin: 0px;
}

QScrollBar::handle:horizontal {
    background-color: #2A2A2A;
    border-radius: 5px;
    min-width: 20px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #3A3A3A;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

    QToolTip {
    background-color: #2A2A2A;
    color: #EEEEEE;
    border: 1px solid #3A3A3A;
        border-radius: 4px;
    padding: 5px;
    opacity: 220;
}

QGroupBox {
    margin-top: 20px;
    font-weight: bold;
    padding-top: 20px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 10px;
    background-color: #1E1E1E;
}

QComboBox {
    background-color: #2A2A2A;
    border: 1px solid #3A3A3A;
    border-radius: 6px;
    padding: 5px 10px;
    min-height: 25px;
}

QComboBox:hover {
    background-color: #3A3A3A;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 15px;
    border-left-width: 0px;
    border-top-right-radius: 3px;
    border-bottom-right-radius: 3px;
}

QComboBox::down-arrow {
    image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAiIGhlaWdodD0iNiIgdmlld0JveD0iMCAwIDEwIDYiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHBhdGggZD0iTTEgMUw1IDVMOSAxIiBzdHJva2U9IiM3Nzc3NzciIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+PC9zdmc+Cg==);
}

QComboBox QAbstractItemView {
    border: 1px solid #3A3A3A;
    background-color: #2A2A2A;
    border-radius: 0 0 6px 6px;
    outline: 0px;
}

QComboBox QAbstractItemView::item {
    height: 25px;
    padding: 5px;
}

QComboBox QAbstractItemView::item:selected {
    background-color: #4464AD;
    color: white;
}

QSpinBox {
    background-color: #2A2A2A;
    border: 1px solid #3A3A3A;
    border-radius: 6px;
    padding: 5px 10px;
    min-height: 25px;
}

QSpinBox::up-button, QSpinBox::down-button {
    border: none;
    width: 15px;
    background-color: #3A3A3A;
}

QSpinBox::up-button:hover, QSpinBox::down-button:hover {
    background-color: #454545;
}

QTabWidget::pane {
    border-top: 2px solid #4464AD;
    top: -2px;
}

QSplitter::handle {
    background-color: #2A2A2A;
    height: 4px;
    margin: 10px 0;
}

QSplitter::handle:hover {
    background-color: #4464AD;
}

QFrame#input_panel, QFrame#output_panel {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #1E1E1E, stop:1 #222222);
    border: 1px solid #2A2A2A;
    border-radius: 12px;
}

/* Input and output text areas */
QTextEdit {
    background-color: #1A1A1A;
    border: 1px solid #2A2A2A;
    border-radius: 8px;
    padding: 12px;
    selection-background-color: #4464AD;
    selection-color: white;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 14px;
    line-height: 1.5;
}

QTextEdit:focus {
    border: 1px solid #4464AD;
    background-color: #19191F;
}

/* Key input field */
QLineEdit#key_input {
    background-color: #1A1A1A;
    border: 1px solid #2A2A2A;
    border-radius: 8px;
    padding: 10px 12px;
    selection-background-color: #4464AD;
    selection-color: white;
    font-size: 14px;
}

QLineEdit#key_input:focus {
    border: 1px solid #4464AD;
    background-color: #19191F;
}

/* Action buttons in panels */
QPushButton.panel_action {
    background-color: rgba(42, 42, 42, 0.8);
    border-radius: 8px;
    padding: 8px;
    min-width: 32px;
    min-height: 32px;
}

QPushButton.panel_action:hover {
    background-color: rgba(58, 58, 58, 0.9);
    }
    """)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.sidebar = QtWidgets.QFrame(self.centralWidget)
        self.sidebar.setMinimumSize(QtCore.QSize(220, 0))
        self.sidebar.setMaximumSize(QtCore.QSize(220, 16777215))
        self.sidebar.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.sidebar.setFrameShadow(QtWidgets.QFrame.Raised)
        self.sidebar.setObjectName("sidebar")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.sidebar)
        self.verticalLayout_2.setContentsMargins(15, 30, 15, 30)
        self.verticalLayout_2.setSpacing(24)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.titleLayout = QtWidgets.QHBoxLayout()
        self.titleLayout.setObjectName("titleLayout")
        self.app_icon = QtWidgets.QLabel(self.sidebar)
        self.app_icon.setMinimumSize(QtCore.QSize(32, 32))
        self.app_icon.setMaximumSize(QtCore.QSize(32, 32))
        self.app_icon.setText("")
        self.app_icon.setPixmap(load_icon('lock').pixmap(32, 32))
        self.app_icon.setScaledContents(True)
        self.app_icon.setObjectName("app_icon")
        self.titleLayout.addWidget(self.app_icon)
        self.app_title = QtWidgets.QLabel(self.sidebar)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setBold(True)
        self.app_title.setFont(font)
        self.app_title.setAlignment(QtCore.Qt.AlignCenter)
        self.app_title.setObjectName("app_title")
        self.titleLayout.addWidget(self.app_title)
        self.verticalLayout_2.addLayout(self.titleLayout)
        self.line = QtWidgets.QFrame(self.sidebar)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_2.addWidget(self.line)
        self.algo_label = QtWidgets.QLabel(self.sidebar)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        self.algo_label.setFont(font)
        self.algo_label.setObjectName("algo_label")
        self.verticalLayout_2.addWidget(self.algo_label)

        # Replace algorithm list with dropdown
        self.algorithm_dropdown = QtWidgets.QComboBox(self.sidebar)
        self.algorithm_dropdown.setObjectName("algorithm_dropdown")
        self.algorithm_dropdown.setMinimumHeight(36)
        self.algorithm_dropdown.setStyleSheet("""
        QComboBox {
            background-color: #2A2A2A;
            color: #EEEEEE;
            border: 1px solid #3A3A3A;
            border-radius: 8px;
            padding: 5px 15px;
            font-size: 14px;
        }
        QComboBox:hover {
            background-color: #3A3A3A;
            border: 1px solid #4464AD;
        }
        QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 30px;
            border-left-width: 0px;
            border-top-right-radius: 8px;
            border-bottom-right-radius: 8px;
        }
    """)

        # Add algorithm options to dropdown
        algo_options = [
            'Caesar Cipher',
            'Playfair Cipher',
            'Rail Fence',
            'Row Transposition',
            'Hill Cipher',
            'Substitution Cipher',
            'Vigenère Cipher',
            'Chris Way Cipher V1',
            'Chris Way Cipher V2',
            'AES',
            'ROT13',
        ]

        for algo in algo_options:
            self.algorithm_dropdown.addItem(algo)
        self.verticalLayout_2.addWidget(self.algorithm_dropdown) # Add dropdown to layout AFTER populating

        # Key label and input below algorithm dropdown
        self.key_label_sidebar = QtWidgets.QLabel(self.sidebar)
        self.key_label_sidebar.setObjectName("key_label_sidebar")
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        self.key_label_sidebar.setFont(font)
        self.key_label_sidebar.setText("KEY")
        self.verticalLayout_2.addWidget(self.key_label_sidebar)

        # Add key input field to sidebar
        self.key_input_sidebar = QtWidgets.QLineEdit(self.sidebar)
        self.key_input_sidebar.setObjectName("key_input_sidebar")
        self.key_input_sidebar.setPlaceholderText("Enter key or password")
        self.key_input_sidebar.setMinimumHeight(36)
        self.key_input_sidebar.setEchoMode(QtWidgets.QLineEdit.Password)
        self.key_input_sidebar.setStyleSheet("""
            QLineEdit {
                background-color: #1A1A1A;
                color: #EEEEEE;
                border: 1px solid #2A2A2A;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #4464AD;
            }
        """)
        self.verticalLayout_2.addWidget(self.key_input_sidebar)

        # Button layout for key operations
        self.key_buttons_layout = QtWidgets.QHBoxLayout()
        self.key_buttons_layout.setObjectName("key_buttons_layout")

        # Toggle password visibility
        self.show_password_btn_sidebar = QtWidgets.QPushButton(self.sidebar)
        self.show_password_btn_sidebar.setIcon(load_icon('eye', 18))
        self.show_password_btn_sidebar.setObjectName("show_password_btn_sidebar")
        self.show_password_btn_sidebar.setCheckable(True)
        self.show_password_btn_sidebar.setToolTip("Show/Hide Password")
        self.show_password_btn_sidebar.setMaximumWidth(40)

        # Generate key button
        self.generate_key_btn_sidebar = QtWidgets.QPushButton(self.sidebar)
        self.generate_key_btn_sidebar.setText("Generate")
        self.generate_key_btn_sidebar.setIcon(load_icon('generate', 18))
        self.generate_key_btn_sidebar.setObjectName("generate_key_btn_sidebar")
        self.generate_key_btn_sidebar.setToolTip("Generate algorithm-specific key")

        # Add buttons to layout
        self.key_buttons_layout.addWidget(self.show_password_btn_sidebar)
        self.key_buttons_layout.addWidget(self.generate_key_btn_sidebar)

        self.verticalLayout_2.addLayout(self.key_buttons_layout)

        # Add spacing before operation mode
        self.verticalLayout_2.addSpacing(20)

        self.op_label = QtWidgets.QLabel(self.sidebar)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        self.op_label.setFont(font)
        self.op_label.setObjectName("op_label")
        self.verticalLayout_2.addWidget(self.op_label)

        self.operationLayout = QtWidgets.QVBoxLayout()
        self.operationLayout.setSpacing(10)
        self.operationLayout.setObjectName("operationLayout")
        self.encrypt_radio = QtWidgets.QRadioButton(self.sidebar)
        self.encrypt_radio.setIcon(load_icon('encrypt', 20))
        self.encrypt_radio.setChecked(True)
        self.encrypt_radio.setObjectName("encrypt_radio")
        self.operationLayout.addWidget(self.encrypt_radio)
        self.decrypt_radio = QtWidgets.QRadioButton(self.sidebar)
        self.decrypt_radio.setIcon(load_icon('decrypt', 20))
        self.decrypt_radio.setObjectName("decrypt_radio")
        self.operationLayout.addWidget(self.decrypt_radio)
        self.verticalLayout_2.addLayout(self.operationLayout)
        self.execute_operation_btn = QtWidgets.QPushButton(self.sidebar)
        self.execute_operation_btn.setMinimumSize(QtCore.QSize(0, 48))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setBold(True)
        font.setPointSize(11) # Larger font
        self.execute_operation_btn.setFont(font)
        self.execute_operation_btn.setIcon(load_icon('encrypt', 24))
        self.execute_operation_btn.setIconSize(QtCore.QSize(24, 24))
        self.execute_operation_btn.setObjectName("execute_operation_btn")
        self.execute_operation_btn.setProperty("class", "encrypt")
        self.execute_operation_btn.setStyleSheet("""
padding: 12px 0;
font-size: 16px;
text-align: left;
padding-left: 24px;
margin: 15px 0;
""")
        self.verticalLayout_2.addWidget(self.execute_operation_btn)
        self.line_2 = QtWidgets.QFrame(self.sidebar)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_2.addWidget(self.line_2)
        self.appearance_label = QtWidgets.QLabel(self.sidebar)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        self.appearance_label.setFont(font)
        self.appearance_label.setObjectName("appearance_label")
        self.verticalLayout_2.addWidget(self.appearance_label)
        self.appearanceLayout = QtWidgets.QHBoxLayout()
        self.appearanceLayout.setObjectName("appearanceLayout")
        self.dark_mode_btn = QtWidgets.QPushButton(self.sidebar)
        self.dark_mode_btn.setText("")
        self.dark_mode_btn.setIcon(load_icon('dark_mode', 18))
        self.dark_mode_btn.setObjectName("dark_mode_btn")
        self.appearanceLayout.addWidget(self.dark_mode_btn)
        self.light_mode_btn = QtWidgets.QPushButton(self.sidebar)
        self.light_mode_btn.setText("")
        self.light_mode_btn.setIcon(load_icon('light_mode', 18))
        self.light_mode_btn.setObjectName("light_mode_btn")
        self.appearanceLayout.addWidget(self.light_mode_btn)
        self.verticalLayout_2.addLayout(self.appearanceLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.status_title = QtWidgets.QLabel(self.sidebar)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        self.status_title.setFont(font)
        self.status_title.setObjectName("status_title")
        self.verticalLayout_2.addWidget(self.status_title)
        self.status_label = QtWidgets.QLabel(self.sidebar)
        self.status_label.setObjectName("status_label")
        self.verticalLayout_2.addWidget(self.status_label)
        self.operation_progress = QtWidgets.QProgressBar(self.sidebar)
        self.operation_progress.setProperty("value", 0)
        self.operation_progress.setTextVisible(False)
        self.operation_progress.setObjectName("operation_progress")
        self.verticalLayout_2.addWidget(self.operation_progress)
        self.horizontalLayout.addWidget(self.sidebar)
        self.main_panel = QtWidgets.QWidget(self.centralWidget)
        self.main_panel.setObjectName("main_panel")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.main_panel)
        self.verticalLayout.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout.setSpacing(15)
        self.verticalLayout.setObjectName("verticalLayout")
        self.toolbarLayout = QtWidgets.QHBoxLayout()
        self.toolbarLayout.setObjectName("toolbarLayout")
        self.save_result_btn = QtWidgets.QPushButton(self.main_panel)
        self.save_result_btn.setIcon(load_icon('save', 20))
        self.save_result_btn.setObjectName("save_result_btn")
        self.toolbarLayout.addWidget(self.save_result_btn)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.toolbarLayout.addItem(spacerItem1)
        self.help_btn = QtWidgets.QPushButton(self.main_panel)
        self.help_btn.setIcon(load_icon('help', 20))
        self.help_btn.setObjectName("help_btn")
        self.toolbarLayout.addWidget(self.help_btn)
        self.settings_btn = QtWidgets.QPushButton(self.main_panel)
        self.settings_btn.setIcon(load_icon('settings', 20))
        self.settings_btn.setObjectName("settings_btn")
        self.toolbarLayout.addWidget(self.settings_btn)
        self.verticalLayout.addLayout(self.toolbarLayout)
        self.main_tab_widget = QtWidgets.QTabWidget(self.main_panel)
        self.main_tab_widget.setIconSize(QtCore.QSize(16, 16))
        self.main_tab_widget.setObjectName("main_tab_widget")
        self.encrypt_tab = QtWidgets.QWidget()
        self.encrypt_tab.setObjectName("encrypt_tab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.encrypt_tab)
        self.verticalLayout_3.setSpacing(15)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.main_splitter = QtWidgets.QSplitter(self.encrypt_tab)
        self.main_splitter.setOrientation(QtCore.Qt.Vertical)
        self.main_splitter.setHandleWidth(10)
        self.main_splitter.setObjectName("main_splitter")
        self.input_panel = QtWidgets.QFrame(self.main_splitter)
        self.input_panel.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.input_panel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.input_panel.setObjectName("input_panel")
        self.inputPanelLayout = QtWidgets.QVBoxLayout(self.input_panel)
        self.inputPanelLayout.setContentsMargins(20, 20, 20, 20)
        self.inputPanelLayout.setSpacing(16)
        self.inputPanelLayout.setObjectName("inputPanelLayout")
        self.inputHeaderLayout = QtWidgets.QHBoxLayout()
        self.inputHeaderLayout.setObjectName("inputHeaderLayout")
        self.inputHeaderLayout.setSpacing(10)
        self.input_label = QtWidgets.QLabel(self.input_panel)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(True)
        self.input_label.setFont(font)
        self.input_label.setObjectName("input_label")
        self.inputHeaderLayout.addWidget(self.input_label)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.inputHeaderLayout.addItem(spacerItem2)
        self.clear_input_btn = QtWidgets.QPushButton(self.input_panel)
        self.clear_input_btn.setText("")
        self.clear_input_btn.setIcon(load_icon('clear', 18))
        self.clear_input_btn.setIconSize(QtCore.QSize(18, 18))
        self.clear_input_btn.setObjectName("clear_input_btn")
        self.clear_input_btn.setProperty("class", "panel_action")
        self.inputHeaderLayout.addWidget(self.clear_input_btn)
        self.load_input_btn = QtWidgets.QPushButton(self.input_panel)
        self.load_input_btn.setText("")
        self.load_input_btn.setIcon(load_icon('load_file', 18))
        self.load_input_btn.setIconSize(QtCore.QSize(18, 18))
        self.load_input_btn.setObjectName("load_input_btn")
        self.load_input_btn.setProperty("class", "panel_action")
        self.inputHeaderLayout.addWidget(self.load_input_btn)
        self.inputPanelLayout.addLayout(self.inputHeaderLayout)
        self.input_text_edit = QtWidgets.QTextEdit(self.input_panel)
        self.input_text_edit.setObjectName("input_text_edit")
        self.inputPanelLayout.addWidget(self.input_text_edit)
        self.key_panel = QtWidgets.QFrame(self.input_panel)
        self.key_panel.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.key_panel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.key_panel.setObjectName("key_panel")
        self.keyPanelLayout = QtWidgets.QVBoxLayout(self.key_panel)
        self.keyPanelLayout.setObjectName("keyPanelLayout")
        self.key_label = QtWidgets.QLabel(self.key_panel)
        self.key_label.setObjectName("key_label")
        self.keyPanelLayout.addWidget(self.key_label)
        self.key_input_layout = QtWidgets.QHBoxLayout()
        self.key_input_layout.setObjectName("key_input_layout")
        self.key_input = QtWidgets.QLineEdit(self.key_panel)
        self.key_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.key_input.setObjectName("key_input")
        self.key_input_layout.addWidget(self.key_input)
        self.show_password_btn = QtWidgets.QPushButton(self.key_panel)
        self.show_password_btn.setText("")
        self.show_password_btn.setIcon(load_icon('eye', 18))
        self.show_password_btn.setCheckable(True)
        self.show_password_btn.setObjectName("show_password_btn")
        self.key_input_layout.addWidget(self.show_password_btn)

        # Remove duplicate generate_key_btn and keep only random_key_btn
        self.random_key_btn = QtWidgets.QPushButton(self.key_panel)
        self.random_key_btn.setText(" Random Key")
        self.random_key_btn.setIcon(load_icon('generate', 18))
        self.random_key_btn.setObjectName("random_key_btn")
        self.random_key_btn.setToolTip("Generate a completely random secure key")
        self.key_input_layout.addWidget(self.random_key_btn)
        self.keyPanelLayout.addLayout(self.key_input_layout)
        self.strength_meter_layout = QtWidgets.QHBoxLayout()
        self.strength_meter_layout.setObjectName("strength_meter_layout")
        self.key_strength_meter = QtWidgets.QProgressBar(self.key_panel)
        self.key_strength_meter.setMaximumSize(QtCore.QSize(16777215, 8))
        self.key_strength_meter.setStyleSheet("""QProgressBar {
    background-color: #252538;
    border-radius: 4px;
    }
    QProgressBar::chunk {
    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #FF5858, stop:0.5 #FFDE59, stop:1 #4EC2F7);
    border-radius: 3px;
    }""")
        self.key_strength_meter.setProperty("value", 50)
        self.key_strength_meter.setTextVisible(False)
        self.key_strength_meter.setObjectName("key_strength_meter")
        self.strength_meter_layout.addWidget(self.key_strength_meter)
        self.strength_label = QtWidgets.QLabel(self.key_panel)
        self.strength_label.setObjectName("strength_label")
        self.strength_meter_layout.addWidget(self.strength_label)
        self.keyPanelLayout.addLayout(self.strength_meter_layout)
        self.key_requirements_label = QtWidgets.QLabel(self.key_panel)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setItalic(True)
        self.key_requirements_label.setFont(font)
        self.key_requirements_label.setObjectName("key_requirements_label")
        self.keyPanelLayout.addWidget(self.key_requirements_label)
        self.inputPanelLayout.addWidget(self.key_panel)
        self.output_panel = QtWidgets.QFrame(self.main_splitter)
        self.output_panel.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.output_panel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.output_panel.setObjectName("output_panel")
        self.outputPanelLayout = QtWidgets.QVBoxLayout(self.output_panel)
        self.outputPanelLayout.setContentsMargins(20, 20, 20, 20)
        self.outputPanelLayout.setSpacing(16)
        self.outputPanelLayout.setObjectName("outputPanelLayout")
        self.outputHeaderLayout = QtWidgets.QHBoxLayout()
        self.outputHeaderLayout.setObjectName("outputHeaderLayout")
        self.output_label = QtWidgets.QLabel(self.output_panel)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        font.setBold(True)
        self.output_label.setFont(font)
        self.output_label.setObjectName("output_label")
        self.outputHeaderLayout.addWidget(self.output_label)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.outputHeaderLayout.addItem(spacerItem3)
        self.copy_output_btn = QtWidgets.QPushButton(self.output_panel)
        self.copy_output_btn.setText("")
        self.copy_output_btn.setIcon(load_icon('copy', 18))
        self.copy_output_btn.setObjectName("copy_output_btn")
        self.outputHeaderLayout.addWidget(self.copy_output_btn)
        self.save_output_btn = QtWidgets.QPushButton(self.output_panel)
        self.save_output_btn.setText("")
        self.save_output_btn.setIcon(load_icon('save_file', 18))
        self.save_output_btn.setObjectName("save_output_btn")
        self.outputHeaderLayout.addWidget(self.save_output_btn)
        self.outputPanelLayout.addLayout(self.outputHeaderLayout)
        self.output_text_edit = QtWidgets.QTextEdit(self.output_panel)
        self.output_text_edit.setReadOnly(True)
        self.output_text_edit.setObjectName("output_text_edit")
        self.outputPanelLayout.addWidget(self.output_text_edit)
        self.verticalLayout_3.addWidget(self.main_splitter)
        icon_tab_encrypt = QtGui.QIcon()
        icon_tab_encrypt.addPixmap(QtGui.QPixmap("icons/lock.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.main_tab_widget.addTab(self.encrypt_tab, icon_tab_encrypt, "")
        self.file_operations_tab = QtWidgets.QWidget()
        self.file_operations_tab.setObjectName("file_operations_tab")
        self.verticalLayout_file_tab = QtWidgets.QVBoxLayout(self.file_operations_tab)
        self.verticalLayout_file_tab.setContentsMargins(0,0,0,0)
        self.verticalLayout_file_tab.setObjectName("verticalLayout_file_tab")
        self.file_operations_panel = QtWidgets.QFrame(self.file_operations_tab)
        self.file_operations_panel.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.file_operations_panel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.file_operations_panel.setObjectName("file_operations_panel")
        self.fileOperationsLayout = QtWidgets.QVBoxLayout(self.file_operations_panel)
        self.fileOperationsLayout.setContentsMargins(15, 15, 15, 15)
        self.fileOperationsLayout.setSpacing(10)
        self.fileOperationsLayout.setObjectName("fileOperationsLayout")
        self.file_op_title = QtWidgets.QLabel(self.file_operations_panel)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        font.setBold(True)
        self.file_op_title.setFont(font)
        self.file_op_title.setObjectName("file_op_title")
        self.fileOperationsLayout.addWidget(self.file_op_title)
        self.file_buttons_layout = QtWidgets.QHBoxLayout()
        self.file_buttons_layout.setObjectName("file_buttons_layout")
        self.select_files_btn = QtWidgets.QPushButton(self.file_operations_panel)
        self.select_files_btn.setIcon(load_icon('files_tab', 18))
        self.select_files_btn.setObjectName("select_files_btn")
        self.file_buttons_layout.addWidget(self.select_files_btn)
        self.select_folder_btn = QtWidgets.QPushButton(self.file_operations_panel)
        self.select_folder_btn.setIcon(load_icon('files_tab', 18))
        self.select_folder_btn.setObjectName("select_folder_btn")
        self.file_buttons_layout.addWidget(self.select_folder_btn)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.file_buttons_layout.addItem(spacerItem4)
        self.batch_mode_label = QtWidgets.QLabel(self.file_operations_panel)
        self.batch_mode_label.setObjectName("batch_mode_label")
        self.file_buttons_layout.addWidget(self.batch_mode_label)
        self.batch_mode_checkbox = QtWidgets.QCheckBox(self.file_operations_panel)
        self.batch_mode_checkbox.setText("")
        self.batch_mode_checkbox.setObjectName("batch_mode_checkbox")
        self.file_buttons_layout.addWidget(self.batch_mode_checkbox)
        self.fileOperationsLayout.addLayout(self.file_buttons_layout)
        self.file_list = QtWidgets.QListWidget(self.file_operations_panel)
        self.file_list.setAcceptDrops(True)
        self.file_list.setDragEnabled(True)
        self.file_list.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.file_list.setAlternatingRowColors(True)
        self.file_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.file_list.setIconSize(QtCore.QSize(16, 16))
        self.file_list.setObjectName("file_list")
        self.fileOperationsLayout.addWidget(self.file_list)
        self.file_actions_layout = QtWidgets.QHBoxLayout()
        self.file_actions_layout.setObjectName("file_actions_layout")
        self.clear_files_btn = QtWidgets.QPushButton(self.file_operations_panel)
        self.clear_files_btn.setIcon(load_icon('clear', 18))
        self.clear_files_btn.setObjectName("clear_files_btn")
        self.file_actions_layout.addWidget(self.clear_files_btn)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.file_actions_layout.addItem(spacerItem5)
        self.output_dir_label = QtWidgets.QLabel(self.file_operations_panel)
        self.output_dir_label.setObjectName("output_dir_label")
        self.file_actions_layout.addWidget(self.output_dir_label)
        self.output_dir_input = QtWidgets.QLineEdit(self.file_operations_panel)
        self.output_dir_input.setReadOnly(True)
        self.output_dir_input.setObjectName("output_dir_input")
        self.file_actions_layout.addWidget(self.output_dir_input)
        self.browse_output_btn = QtWidgets.QPushButton(self.file_operations_panel)
        self.browse_output_btn.setText("")
        self.browse_output_btn.setIcon(load_icon('browse', 18))
        self.browse_output_btn.setObjectName("browse_output_btn")
        self.file_actions_layout.addWidget(self.browse_output_btn)
        self.fileOperationsLayout.addLayout(self.file_actions_layout)

        # Add a process files button
        self.process_files_btn = QtWidgets.QPushButton(self.file_operations_panel)
        self.process_files_btn.setIcon(load_icon('encrypt', 20))
        self.process_files_btn.setText(" Process Files")
        self.process_files_btn.setMinimumHeight(40)
        self.process_files_btn.setObjectName("process_files_btn")
        self.process_files_btn.setStyleSheet("""
        QPushButton#process_files_btn {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4464AD, stop:1 #5575BE);
            color: white;
            font-size: 14px;
            font-weight: bold;
            border-radius: 8px;
        }
        QPushButton#process_files_btn:hover {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #5575BE, stop:1 #6686CF);
        }
    """)
        self.fileOperationsLayout.addWidget(self.process_files_btn)

        self.verticalLayout_file_tab.addWidget(self.file_operations_panel)
        icon_tab_file = QtGui.QIcon()
        icon_tab_file.addPixmap(QtGui.QPixmap("icons/files_tab.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.main_tab_widget.addTab(self.file_operations_tab, icon_tab_file, "")
        self.history_tab = QtWidgets.QWidget()
        self.history_tab.setObjectName("history_tab")
        self.history_layout_outer = QtWidgets.QVBoxLayout(self.history_tab)
        self.history_layout_outer.setContentsMargins(15, 15, 15, 15)
        self.history_layout_outer.setSpacing(10)
        self.history_layout_outer.setObjectName("history_layout_outer")
        self.history_actions_layout = QtWidgets.QHBoxLayout()
        self.history_actions_layout.setObjectName("history_actions_layout")
        self.history_filter_combo = QtWidgets.QComboBox(self.history_tab)
        self.history_filter_combo.setObjectName("history_filter_combo")
        self.history_filter_combo.addItem("")
        self.history_filter_combo.addItem("")
        self.history_filter_combo.addItem("")
        self.history_actions_layout.addWidget(self.history_filter_combo)
        self.history_search = QtWidgets.QLineEdit(self.history_tab)
        self.history_search.setClearButtonEnabled(True)
        self.history_search.setObjectName("history_search")
        self.history_actions_layout.addWidget(self.history_search)
        self.clear_history_btn = QtWidgets.QPushButton(self.history_tab)
        self.clear_history_btn.setIcon(load_icon('clear', 18))
        self.clear_history_btn.setObjectName("clear_history_btn")
        self.history_actions_layout.addWidget(self.clear_history_btn)
        self.export_history_btn = QtWidgets.QPushButton(self.history_tab)
        self.export_history_btn.setIcon(load_icon('export', 18))
        self.export_history_btn.setObjectName("export_history_btn")
        self.history_actions_layout.addWidget(self.export_history_btn)
        self.history_layout_outer.addLayout(self.history_actions_layout)
        self.history_table = QtWidgets.QTableWidget(self.history_tab)
        self.history_table.setAlternatingRowColors(True)
        self.history_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.history_table.setSortingEnabled(True)
        self.history_table.setObjectName("history_table")
        self.history_table.setColumnCount(5)
        self.history_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.history_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.history_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.history_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.history_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.history_table.setHorizontalHeaderItem(4, item)
        self.history_table.horizontalHeader().setStretchLastSection(True)
        self.history_layout_outer.addWidget(self.history_table)
        self.load_history_actions_layout = QtWidgets.QHBoxLayout()
        self.load_history_actions_layout.setObjectName("load_history_actions_layout")
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.load_history_actions_layout.addItem(spacerItem6)
        self.load_history_item_btn = QtWidgets.QPushButton(self.history_tab)
        self.load_history_item_btn.setIcon(load_icon('load', 18))
        self.load_history_item_btn.setObjectName("load_history_item_btn")
        self.load_history_actions_layout.addWidget(self.load_history_item_btn)
        self.history_layout_outer.addLayout(self.load_history_actions_layout)
        icon_tab_history = QtGui.QIcon()
        icon_tab_history.addPixmap(QtGui.QPixmap("icons/history.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.main_tab_widget.addTab(self.history_tab, icon_tab_history, "")
        self.verticalLayout.addWidget(self.main_tab_widget)
        self.horizontalLayout.addWidget(self.main_panel)
        self.horizontalLayout.setStretch(1, 1)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1136, 28))
        self.menuBar.setObjectName("menuBar")
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        self.main_tab_widget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "EncryptPro"))
        self.app_title.setText(_translate("MainWindow", "EncryptPro"))
        self.algo_label.setText(_translate("MainWindow", "ALGORITHMS"))

        # Algorithm dropdown
        # Already populated in setupUi

        # Key input
        self.key_label_sidebar.setText(_translate("MainWindow", "KEY"))
        self.key_input_sidebar.setPlaceholderText(_translate("MainWindow", "Enter key or password"))
        self.show_password_btn_sidebar.setToolTip(_translate("MainWindow", "Show/Hide Password"))
        self.generate_key_btn_sidebar.setToolTip(_translate("MainWindow", "Generate Key"))

        self.op_label.setText(_translate("MainWindow", "OPERATION MODE"))
        self.encrypt_radio.setText(_translate("MainWindow", " Encrypt"))
        self.decrypt_radio.setText(_translate("MainWindow", " Decrypt"))
        self.execute_operation_btn.setText(_translate("MainWindow", " ENCRYPT"))
        self.appearance_label.setText(_translate("MainWindow", "APPEARANCE"))
        self.dark_mode_btn.setText(_translate("MainWindow", " Dark"))
        self.light_mode_btn.setText(_translate("MainWindow", " Light"))
        self.status_title.setText(_translate("MainWindow", "STATUS"))
        self.status_label.setText(_translate("MainWindow", "Ready"))
        self.save_result_btn.setToolTip(_translate("MainWindow", "Save Result"))
        self.save_result_btn.setText(_translate("MainWindow", " Save"))
        self.help_btn.setToolTip(_translate("MainWindow", "Help"))
        self.help_btn.setText(_translate("MainWindow", " Help"))
        self.settings_btn.setToolTip(_translate("MainWindow", "Settings"))
        self.settings_btn.setText(_translate("MainWindow", " Settings"))
        self.input_label.setText(_translate("MainWindow", "INPUT"))
        self.clear_input_btn.setToolTip(_translate("MainWindow", "Clear Input Text"))
        self.load_input_btn.setToolTip(_translate("MainWindow", "Load Input from File"))
        self.input_text_edit.setPlaceholderText(_translate("MainWindow", "Enter text to encrypt or decrypt..."))
        self.key_label.setText(_translate("MainWindow", "Encryption Key:"))
        self.key_input.setPlaceholderText(_translate("MainWindow", "Enter key or password"))
        self.show_password_btn.setToolTip(_translate("MainWindow", "Show/Hide Password"))
        self.random_key_btn.setToolTip(_translate("MainWindow", "Generate Completely Random Key"))
        self.strength_label.setText(_translate("MainWindow", "Medium"))
        self.key_requirements_label.setText(_translate("MainWindow", "Minimum length: 8 chars | Recommended: 12+ with mixed case, numbers, symbols"))
        self.output_label.setText(_translate("MainWindow", "OUTPUT"))
        self.copy_output_btn.setToolTip(_translate("MainWindow", "Copy Output Text"))
        self.save_output_btn.setToolTip(_translate("MainWindow", "Save Output to File"))
        self.output_text_edit.setPlaceholderText(_translate("MainWindow", "Encrypted or decrypted result will appear here..."))
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.encrypt_tab), _translate("MainWindow", "Encryption/Decryption"))
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.file_operations_tab), _translate("MainWindow", "File Operations")) # Added for file_operations_tab
        self.file_op_title.setText(_translate("MainWindow", "File Operations"))
        self.select_files_btn.setText(_translate("MainWindow", " Select Files"))
        self.select_folder_btn.setText(_translate("MainWindow", " Select Folder"))
        self.batch_mode_label.setText(_translate("MainWindow", "Batch Mode:"))
        self.clear_files_btn.setText(_translate("MainWindow", " Clear Files")) # Added for clear_files_btn
        self.output_dir_label.setText(_translate("MainWindow", "Output Directory:")) # Added for output_dir_label
        self.browse_output_btn.setToolTip(_translate("MainWindow", "Browse Output Directory")) # Added for browse_output_btn

        self.history_filter_combo.setItemText(0, _translate("MainWindow", "All Operations"))
        self.history_filter_combo.setItemText(1, _translate("MainWindow", "Encryption"))
        self.history_filter_combo.setItemText(2, _translate("MainWindow", "Decryption"))
        self.history_search.setPlaceholderText(_translate("MainWindow", "Search history (e.g., by date, algorithm, filename)..."))
        self.clear_history_btn.setText(_translate("MainWindow", " Clear History"))
        self.export_history_btn.setText(_translate("MainWindow", " Export"))
        item = self.history_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Date"))
        item = self.history_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Algorithm"))
        item = self.history_table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Operation"))
        item = self.history_table.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Content/File"))
        item = self.history_table.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Actions"))
        self.load_history_item_btn.setText(_translate("MainWindow", " Load Selected"))
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.history_tab), _translate("MainWindow", "History"))

# ----------------------------------------------------------------------
# Login Dialog Class
# ----------------------------------------------------------------------
class LoginDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("EncryptPro Login")
        # Remove fixed size to allow resizing
        self.setMinimumSize(400, 300)  # Set minimum size instead of fixed
        self.setWindowIcon(load_icon('lock'))
        self.setModal(True)

        # Enable minimize and maximize buttons
        self.setWindowFlags(
            QtCore.Qt.Dialog |
            QtCore.Qt.WindowMinimizeButtonHint |
            QtCore.Qt.WindowMaximizeButtonHint
        )

        # Set dark theme styles
        self.setStyleSheet("""
            QDialog {
                background-color: #121212;
                color: #EEEEEE;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLabel {
                color: #EEEEEE;
                font-size: 14px;
            }
            QLineEdit {
                background-color: #1A1A1A;
                color: #EEEEEE;
                border: 1px solid #2A2A2A;
                border-radius: 8px;
                padding: 10px;
                margin: 5px 0px;
                selection-background-color: #4464AD;
                selection-color: white;
            }
            QLineEdit:focus {
                border: 1px solid #4464AD;
            }
            QPushButton {
                background-color: #2A2A2A;
                color: #EEEEEE;
                border: none;
                border-radius: 8px;
                padding: 10px 18px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #3A3A3A;
            }
            QPushButton:pressed {
                background-color: #454545;
            }
            QPushButton#login_btn {
                background-color: #4464AD;
                color: white;
                font-size: 15px;
                margin-top: 15px;
            }
            QPushButton#login_btn:hover {
                background-color: #5575BE;
            }
        """)

        # Create main layout with responsive margins
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(0)

        # Create a centered widget for better responsiveness
        center_widget = QtWidgets.QWidget()
        center_layout = QtWidgets.QVBoxLayout(center_widget)
        center_layout.setSpacing(15)

        # Add spacers for vertical centering
        main_layout.addStretch(1)
        main_layout.addWidget(center_widget)
        main_layout.addStretch(1)

        # Logo and title
        title_layout = QtWidgets.QHBoxLayout()
        title_layout.setSpacing(15)

        logo = QtWidgets.QLabel()
        logo.setPixmap(load_icon('lock').pixmap(48, 48))
        logo.setFixedSize(48, 48)

        title = QtWidgets.QLabel("EncryptPro Login")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #4EC2F7;")

        title_layout.addStretch(1)
        title_layout.addWidget(logo)
        title_layout.addWidget(title)
        title_layout.addStretch(1)

        center_layout.addLayout(title_layout)
        center_layout.addSpacing(20)

        # Form layout for fields
        form_layout = QtWidgets.QFormLayout()
        form_layout.setLabelAlignment(QtCore.Qt.AlignRight)
        form_layout.setFormAlignment(QtCore.Qt.AlignHCenter)
        form_layout.setSpacing(10)

        # Username
        username_label = QtWidgets.QLabel("Username:")
        self.username_input = QtWidgets.QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        self.username_input.setMinimumWidth(250)
        form_layout.addRow(username_label, self.username_input)

        # Password
        password_label = QtWidgets.QLabel("Password:")
        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter password")
        form_layout.addRow(password_label, self.password_input)

        center_layout.addLayout(form_layout)

        # Login button - centered
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch(1)

        self.login_btn = QtWidgets.QPushButton("Login")
        self.login_btn.setObjectName("login_btn")
        self.login_btn.setMinimumHeight(40)
        self.login_btn.setMinimumWidth(150)
        self.login_btn.clicked.connect(self.attempt_login)

        button_layout.addWidget(self.login_btn)
        button_layout.addStretch(1)
        center_layout.addLayout(button_layout)

        # Status message
        self.status_label = QtWidgets.QLabel("")
        self.status_label.setStyleSheet("color: #FF6961;")
        self.status_label.setAlignment(QtCore.Qt.AlignCenter)
        center_layout.addWidget(self.status_label)

        # Default credentials label
        self.default_creds = QtWidgets.QLabel("Default: username 'user', password '000'")
        self.default_creds.setStyleSheet("color: #777777; font-size: 12px;")
        self.default_creds.setAlignment(QtCore.Qt.AlignCenter)
        center_layout.addWidget(self.default_creds)

        # Set default focus
        self.username_input.setFocus()

        # Set default values
        self.username_input.setText("user")
        self.password_input.setText("000")

        # Connect enter key to login button
        self.username_input.returnPressed.connect(self.login_btn.click)
        self.password_input.returnPressed.connect(self.login_btn.click)

    def attempt_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Check credentials - using hardcoded values as specified
        if username == "user" and password == "000":
            self.accept()  # Login successful
        else:
            self.status_label.setText("Invalid username or password!")
            self.password_input.clear()
            self.password_input.setFocus()

    def resizeEvent(self, event):
        """Handle window resize events to keep content properly positioned"""
        super().resizeEvent(event)
        # You could add custom positioning logic here if needed

# ----------------------------------------------------------------------
# Main Application Class
# ----------------------------------------------------------------------
class EncryptProApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # Set up logging
        logging.basicConfig(filename='encryptpro.log', level=logging.ERROR)

        # Connect signals to slots (methods)
        self.ui.encrypt_radio.toggled.connect(self.update_execute_button_style)

        # Connect execute button and password visibility toggle
        self.ui.execute_operation_btn.clicked.connect(self.perform_operation)

        # Connect sidebar password toggle and key generation
        self.ui.show_password_btn_sidebar.toggled.connect(self.toggle_password_visibility_sidebar)
        self.ui.generate_key_btn_sidebar.clicked.connect(self.generate_key)

        # Connect algorithm dropdown change event
        self.ui.algorithm_dropdown.currentIndexChanged.connect(self.algorithm_changed)

        # Connect toolbar buttons
        self.ui.save_result_btn.clicked.connect(self.save_output_file)
        self.ui.help_btn.clicked.connect(self.show_help)
        self.ui.settings_btn.clicked.connect(self.show_settings)

        # Connect input panel buttons
        self.ui.clear_input_btn.clicked.connect(self.clear_input)
        self.ui.load_input_btn.clicked.connect(self.load_input_file)
        # Connect sidebar key generation to random key generation
        # self.ui.generate_key_btn_sidebar.clicked.connect(self.generate_key) # Already connected above
        self.ui.random_key_btn.clicked.connect(self.generate_random_key)

        # Connect original password toggle
        self.ui.show_password_btn.toggled.connect(self.toggle_password_visibility)

        # Connect output panel buttons
        self.ui.copy_output_btn.clicked.connect(self.copy_output)
        self.ui.save_output_btn.clicked.connect(self.save_output_file)

        # Connect file operations buttons
        self.ui.select_files_btn.clicked.connect(self.select_files)
        self.ui.select_folder_btn.clicked.connect(self.select_folder)
        self.ui.clear_files_btn.clicked.connect(self.clear_file_list)
        self.ui.browse_output_btn.clicked.connect(self.browse_output_directory)
        self.ui.process_files_btn.clicked.connect(self.process_files)

        # Connect history tab buttons
        self.ui.clear_history_btn.clicked.connect(self.clear_history)
        self.ui.export_history_btn.clicked.connect(self.export_history)
        self.ui.load_history_item_btn.clicked.connect(self.load_history_item)

        # Connect history filter and search
        self.ui.history_filter_combo.currentIndexChanged.connect(self.filter_history)
        self.ui.history_search.textChanged.connect(self.search_history)

        # Connect theme buttons
        self.ui.dark_mode_btn.clicked.connect(lambda: self.set_theme("dark"))
        self.ui.light_mode_btn.clicked.connect(lambda: self.set_theme("light"))

        # Connect key input text changed to update strength meter
        self.ui.key_input.textChanged.connect(self.update_key_strength)
        self.ui.key_input_sidebar.textChanged.connect(self.update_key_strength_and_sync)

        # Initial setup
        self.update_execute_button_style() # Set initial button style

        # History data storage
        self.history_data = []

    def algorithm_changed(self, index):
        """Handler for algorithm dropdown selection change"""
        # Update key requirements or other UI based on selected algorithm
        algo_name = self.ui.algorithm_dropdown.currentText()
        
        # Disable key input for ROT13 and Chris Way Cipher V1
        if algo_name == "ROT13":
            self.ui.key_input_sidebar.setEnabled(False)
            self.ui.key_input_sidebar.setPlaceholderText("ROT13 does not require a key")
            self.ui.generate_key_btn_sidebar.setEnabled(False)
            self.ui.key_requirements_label.setText("ROT13 does not use a key - it's a Caesar cipher with a fixed shift of 13.")
        elif algo_name == "Chris Way Cipher V1":
            self.ui.key_input_sidebar.setEnabled(False)
            self.ui.key_input_sidebar.setPlaceholderText("No key required for V1")
            self.ui.generate_key_btn_sidebar.setEnabled(False)
            self.ui.key_requirements_label.setText("Chris Way Cipher V1 does not require a key - it operates based on character positions.")
        else:
            self.ui.key_input_sidebar.setEnabled(True)
            self.ui.key_input_sidebar.setPlaceholderText("Enter key or password")
            self.ui.generate_key_btn_sidebar.setEnabled(True)
            
            # Update key requirements based on algorithm
            if algo_name == "Caesar Cipher":
                self.ui.key_requirements_label.setText("Key must be an integer from 1 to 25.")
            elif algo_name == "Playfair Cipher":
                self.ui.key_requirements_label.setText("Key must be letters only. Creates a 5×5 matrix (I/J combined).")
            elif algo_name == "Rail Fence":
                self.ui.key_requirements_label.setText("Key must be an integer ≥ 2 (number of rails).")
            elif algo_name == "Row Transposition":
                self.ui.key_requirements_label.setText("Key must be space-separated numbers (e.g., '3 1 2').")
            elif algo_name == "Hill Cipher":
                self.ui.key_requirements_label.setText("Key must be comma-separated integers forming a square matrix (e.g., '2,4,5,9').")
            elif algo_name == "Substitution Cipher":
                self.ui.key_requirements_label.setText("Key must be all 26 letters without repetition.")
            elif algo_name == "Vigenère Cipher":
                self.ui.key_requirements_label.setText("Key must be letters only. Longer keys provide better security.")
            elif algo_name == "Chris Way Cipher V2":
                mode = "Encryption" if self.ui.encrypt_radio.isChecked() else "Decryption"
                if mode == "Encryption":
                    self.ui.key_input_sidebar.setPlaceholderText("Enter public key (min 3 chars)")
                    self.ui.key_requirements_label.setText("Public Key: Use alphabetic characters only (min 3 chars). Click 'Generate' to create a key pair.")
                else:
                    self.ui.key_input_sidebar.setPlaceholderText("Enter private key (min 3 chars)")
                    self.ui.key_requirements_label.setText("Private Key: Use alphabetic characters only (min 3 chars). Click 'Generate' to create a key pair.")
            elif algo_name == "AES":
                self.ui.key_requirements_label.setText("Key: 16/24/32 chars or hex (32/48/64 hex digits, can use '0x' prefix). Using CBC mode with PKCS5Padding and hex output.")
            else:
                self.ui.key_requirements_label.setText("Enter an appropriate key for the selected algorithm.")
                
        # Clear any previous validation messages when changing algorithms
        self.ui.status_label.setText(f"{algo_name} selected. Ready for operation.")
        
        # Update operation progress bar to show ready state
        self.ui.operation_progress.setRange(0, 100)
        self.ui.operation_progress.setValue(0)

    def toggle_password_visibility_sidebar(self, checked):
        """Toggle visibility of password in sidebar key input"""
        if checked:
            self.ui.key_input_sidebar.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.ui.show_password_btn_sidebar.setIcon(load_icon('eye_crossed', 18))
            self.ui.show_password_btn_sidebar.setToolTip("Hide Password")
        else:
            self.ui.key_input_sidebar.setEchoMode(QtWidgets.QLineEdit.Password)
            self.ui.show_password_btn_sidebar.setIcon(load_icon('eye', 18))
            self.ui.show_password_btn_sidebar.setToolTip("Show Password")

    def update_key_strength_and_sync(self, text):
        """Update key strength meter and sync with main key input"""
        # Sync the text to the main key input field
        self.ui.key_input.setText(text)
        # Update strength indication
        self.update_key_strength(text)

    def update_execute_button_style(self):
        if self.ui.encrypt_radio.isChecked():
            self.ui.execute_operation_btn.setText(" ENCRYPT")
            self.ui.execute_operation_btn.setIcon(load_icon('encrypt', 24))
            self.ui.execute_operation_btn.setProperty("class", "encrypt")
        else:
            self.ui.execute_operation_btn.setText(" DECRYPT")
            self.ui.execute_operation_btn.setIcon(load_icon('decrypt', 24))
            self.ui.execute_operation_btn.setProperty("class", "decrypt")

        # Re-apply style to ensure the "class" property change takes effect from the stylesheet
        self.ui.execute_operation_btn.style().unpolish(self.ui.execute_operation_btn)
        self.ui.execute_operation_btn.style().polish(self.ui.execute_operation_btn)
        self.ui.execute_operation_btn.update() # Sometimes helps ensure visual update
        
        # Update the key requirements for Chris Way Cipher V2 based on encrypt/decrypt mode
        algo_name = self.ui.algorithm_dropdown.currentText()
        if algo_name == "Chris Way Cipher V2":
            if self.ui.encrypt_radio.isChecked():
                self.ui.key_input_sidebar.setPlaceholderText("Enter public key (min 3 chars)")
                self.ui.key_requirements_label.setText("Public Key: Use alphabetic characters only (min 3 chars). Click 'Generate' to create a key pair.")
                self.ui.status_label.setText("Ready to encrypt with Chris Way Cipher V2. Use public key.")
            else:
                self.ui.key_input_sidebar.setPlaceholderText("Enter private key (min 3 chars)")
                self.ui.key_requirements_label.setText("Private Key: Use alphabetic characters only (min 3 chars). Click 'Generate' to create a key pair.")
                self.ui.status_label.setText("Ready to decrypt with Chris Way Cipher V2. Use private key.")

    def show_algorithm_info_dialog(self, idx=None): # Parameter 'idx' not used with current dropdown
        algo_name = self.ui.algorithm_dropdown.currentText()
        if not algo_name:
            QtWidgets.QMessageBox.information(self, "No Algorithm Selected",
                                                "Please select an algorithm from the list to view its information.")
            return

        # Placeholder for a more detailed dialog if needed in the future
        # For now, we can use a QMessageBox or a simple custom dialog
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle(f"{algo_name} Information")
        layout = QtWidgets.QVBoxLayout(dialog)

        description_label = QtWidgets.QLabel(f"Detailed description for {algo_name} will go here.")
        security_label = QtWidgets.QLabel(f"Security considerations for {algo_name}.")
        usage_label = QtWidgets.QLabel(f"Common use cases for {algo_name}.")

        layout.addWidget(QtWidgets.QLabel(f"<b>{algo_name}</b>"))
        layout.addWidget(description_label)
        layout.addWidget(security_label)
        layout.addWidget(usage_label)

        close_button = QtWidgets.QPushButton("Close")
        close_button.clicked.connect(dialog.accept)
        layout.addWidget(close_button)

        dialog.exec_()


    def perform_operation(self):
        input_text = self.ui.input_text_edit.toPlainText()
        key = self.ui.key_input_sidebar.text()  # Use the sidebar key input

        # Get selected algorithm from dropdown
        algo_name = self.ui.algorithm_dropdown.currentText()

        if not input_text:
            self.ui.status_label.setText("Error: Input text is empty!")
            QtWidgets.QMessageBox.warning(self, "Error", "Input text cannot be empty.")
            return
            
        # Validate inputs based on algorithm requirements
        validation_error = self.validate_inputs(algo_name, input_text, key)
        if validation_error:
            self.ui.status_label.setText(f"Validation Error: {validation_error}")
            QtWidgets.QMessageBox.warning(self, "Validation Error", validation_error)
            return
            
        mode = "Encryption" if self.ui.encrypt_radio.isChecked() else "Decryption"
        self.ui.status_label.setText(f"Performing {mode} with {algo_name}...")
        # Make the progress bar "busy"
        self.ui.operation_progress.setRange(0, 0)

        # Map algorithm names to classes
        algo_map = {
            "Caesar Cipher": CaesarCipher,
            "Playfair Cipher": PlayfairCipher,
            "Rail Fence": RailFenceCipher,
            "Row Transposition": RowTranspositionCipher,
            "Hill Cipher": HillCipher,
            "Substitution Cipher": SubstitutionCipher,
            "Vigenère Cipher": VigenereCipher,
            "AES": AESCipher,
            "ROT13": Rot13Cipher,
            "Chris Way Cipher V1": ChrisWayV1Cipher,
            "Chris Way Cipher V2": ChrisWayV2Cipher,
        }
        try:
            cipher_class = algo_map.get(algo_name)
            if not cipher_class:
                QtWidgets.QMessageBox.information(self, "Not Implemented", f"{algo_name} is not implemented yet.")
                self.ui.status_label.setText(f"{algo_name} not implemented.")
                return

            if mode == "Encryption":
                # ROT13 must not have a key
                if algo_name == "ROT13":
                    result = cipher_class.encrypt(input_text)
                elif algo_name == "AES":
                    # For AES, use CBC mode and hex output format
                    aes_mode = "CBC"  # Use CBC mode as requested
                    result = cipher_class.encrypt(input_text, key, aes_mode, "hex")
                else:
                    result = cipher_class.encrypt(input_text, key)
            else:
                if algo_name == "ROT13":
                    result = cipher_class.decrypt(input_text)
                else:
                    result = cipher_class.decrypt(input_text, key)
            self.ui.output_text_edit.setText(result)
            self.ui.status_label.setText(f"{mode} successful with {algo_name}.")

            # Add to history
            import datetime
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.history_data.append({
                "date": now,
                "algorithm": algo_name,
                "operation": mode,
                "content": input_text[:50] + ("..." if len(input_text) > 50 else ""),
                "key": key,
                "input": input_text,
                "output": result
            })
            self.update_history_table()

        except Exception as e:
            import traceback
            logging.error(f"Error during {mode} with {algo_name}: {str(e)}\n{traceback.format_exc()}")
            self.ui.output_text_edit.setText(f"Error during operation: {str(e)}")
            self.ui.status_label.setText("Operation failed!")
            QtWidgets.QMessageBox.critical(self, "Operation Error", f"An error occurred: {str(e)}")
        finally:
            # Restore the progress bar to 100% when done
            self.ui.operation_progress.setRange(0, 100)
            self.ui.operation_progress.setValue(100)
            
    def validate_inputs(self, algo_name, input_text, key):
        """Validate inputs based on algorithm requirements before passing to cipher classes.
        Returns error message if validation fails, or None if validation passes."""
        
        # Common validations
        if not input_text:
            return "Input text cannot be empty."
            
        # Algorithm-specific validations
        if algo_name == "Caesar Cipher":
            # Plaintext: Letters only (A-Z or a-z)
            if not all(c.isalpha() or c.isspace() for c in input_text):
                return "Caesar Cipher requires text with letters only (A-Z, a-z, spaces)."
                
            # Key: Integer (1-25)
            if not key or not key.isdigit():
                return "Caesar Cipher requires a numeric key."
            
            key_int = int(key)
            if not (1 <= key_int <= 25):
                return "Caesar Cipher key must be an integer between 1 and 25."
                
        elif algo_name == "Substitution Cipher":
            # Plaintext: Letters only
            if not all(c.isalpha() or c.isspace() for c in input_text):
                return "Substitution Cipher requires text with letters only (A-Z, a-z, spaces)."
                
            # Key: A 26-character unique substitution mapping (no repeats)
            if not key or len(key) != 26:
                return "Substitution Cipher requires a 26-character key."
                
            key_upper = key.upper()
            if not all(c.isalpha() for c in key_upper):
                return "Substitution Cipher key must contain only letters."
                
            if len(set(key_upper)) != 26:
                return "Substitution Cipher key must contain all 26 letters with no repeats."
                
        elif algo_name == "ROT13":
            # Plaintext: Letters only
            if not all(c.isalpha() or c.isspace() for c in input_text):
                return "ROT13 requires text with letters only (A-Z, a-z, spaces)."
                
            # No key required for ROT13
            if key:
                return "ROT13 does not require a key."
                
        elif algo_name == "Playfair Cipher":
            # Plaintext: Letters only (no digits or symbols)
            if not all(c.isalpha() or c.isspace() for c in input_text):
                return "Playfair Cipher requires text with letters only (A-Z, a-z, spaces)."
                
            # Key: Required (letters only)
            if not key:
                return "Playfair Cipher requires a keyword."
                
            if not all(c.isalpha() for c in key):
                return "Playfair Cipher key must contain only letters."
                
        elif algo_name == "Rail Fence":
            # Plaintext: Any characters - no validation needed
            
            # Key: Integer ≥ 2
            if not key or not key.isdigit():
                return "Rail Fence Cipher requires a numeric key."
                
            key_int = int(key)
            if key_int < 2:
                return "Rail Fence Cipher key must be an integer >= 2."
                
        elif algo_name == "Hill Cipher":
            # Plaintext: Letters only
            if not all(c.isalpha() or c.isspace() for c in input_text):
                return "Hill Cipher requires text with letters only (A-Z, a-z, spaces)."
                
            # Key: Square matrix with inverse mod 26
            if not key:
                return "Hill Cipher requires a key matrix."
                
            key_parts = key.split(',')
            if not all(part.strip().isdigit() for part in key_parts):
                return "Hill Cipher key must be comma-separated integers."
                
            # Check if it's a square matrix
            n = int(len(key_parts) ** 0.5)
            if n*n != len(key_parts):
                return "Hill Cipher key must form a square matrix (e.g., 4 numbers for 2x2, 9 for 3x3)."
                
            # Matrix size validation for plaintext
            clean_text = ''.join(c for c in input_text if c.isalpha())
            if len(clean_text) % n != 0:
                return f"Hill Cipher plaintext length must be a multiple of {n} (matrix size)."
                
        elif algo_name == "Vigenère Cipher":
            # Plaintext & key: Letters only
            if not all(c.isalpha() or c.isspace() for c in input_text):
                return "Vigenère Cipher requires text with letters only (A-Z, a-z, spaces)."
                
            if not key:
                return "Vigenère Cipher requires a key."
                
            if not all(c.isalpha() for c in key):
                return "Vigenère Cipher key must contain only letters."
                
        elif algo_name == "Chris Way Cipher V1":
            # Plaintext: Letters only
            if not all(c.isalpha() or c.isspace() for c in input_text):
                return "Chris Way Cipher V1 requires text with letters only (A-Z, a-z, spaces)."
                
            # No key required for V1
            if key:
                return "Chris Way Cipher V1 does not require a key."
                
        elif algo_name == "Chris Way Cipher V2":
            # Plaintext: Letters only
            if not all(c.isalpha() or c.isspace() for c in input_text):
                return "Chris Way Cipher V2 requires text with letters only (A-Z, a-z, spaces)."
                
            # Key validation for V2
            if not key:
                return "Chris Way Cipher V2 requires an alphabetic key."
                
            if not all(c.isalpha() for c in key):
                return "Chris Way Cipher V2 key must contain only letters."
                
            if len(key) < 3:
                return "Chris Way Cipher V2 key should be at least 3 characters long."
                
        elif algo_name == "AES":
            # Key validation for both text and hex formats
            if not key:
                return "AES Cipher requires a key."
                
            # Check if key is in hex format (with or without 0x prefix)
            is_hex = False
            clean_key = key
            if key.startswith('0x'):
                clean_key = key[2:]
                is_hex = True
            elif all(c in "0123456789ABCDEFabcdef" for c in key):
                is_hex = True
                
            if is_hex:
                # Check hex key length for AES-128 (32 chars), AES-192 (48 chars), or AES-256 (64 chars)
                hex_lengths = [32, 48, 64]
                if len(clean_key) not in hex_lengths:
                    return f"Hex AES key must be {', '.join(str(l) for l in hex_lengths)} characters long (current: {len(clean_key)})."
            else:
                # Standard text key
                key_len = len(key)
                if key_len not in [16, 24, 32]:
                    return f"AES text key must be 16, 24, or 32 characters long (current: {key_len})."
        
        # Validation passed
        return None

    def update_history_table(self):
        self.ui.history_table.setRowCount(0)  # Clear table
        for i, entry in enumerate(self.history_data):
            self.ui.history_table.insertRow(i)
            self.ui.history_table.setItem(i, 0, QtWidgets.QTableWidgetItem(entry["date"]))
            self.ui.history_table.setItem(i, 1, QtWidgets.QTableWidgetItem(entry["algorithm"]))
            self.ui.history_table.setItem(i, 2, QtWidgets.QTableWidgetItem(entry["operation"]))
            self.ui.history_table.setItem(i, 3, QtWidgets.QTableWidgetItem(entry["content"]))

            # Create a widget with buttons for actions
            actions_widget = QtWidgets.QWidget()
            actions_layout = QtWidgets.QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(2, 2, 2, 2)
            actions_layout.setSpacing(4)

            view_btn = QtWidgets.QPushButton()
            view_btn.setIcon(load_icon('eye', 16))
            view_btn.setFixedSize(24, 24)
            view_btn.setFlat(True)
            view_btn.setToolTip("View Details")
            view_btn.clicked.connect(lambda _, row=i: self.view_history_item(row))

            delete_btn = QtWidgets.QPushButton()
            delete_btn.setIcon(load_icon('delete', 16))
            delete_btn.setFixedSize(24, 24)
            delete_btn.setFlat(True)
            delete_btn.setToolTip("Delete Entry")
            delete_btn.clicked.connect(lambda _, row=i: self.delete_history_item(row))

            actions_layout.addWidget(view_btn)
            actions_layout.addWidget(delete_btn)
            actions_layout.addStretch()

            self.ui.history_table.setCellWidget(i, 4, actions_widget)

    def clear_history(self):
        if not self.history_data:
            return

        reply = QtWidgets.QMessageBox.question(
            self, "Clear History",
            "Are you sure you want to clear all history?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )
        if reply == QtWidgets.QMessageBox.Yes:
            self.history_data = []
            self.update_history_table()
            self.ui.status_label.setText("History cleared")

    def export_history(self):
        if not self.history_data:
            QtWidgets.QMessageBox.information(self, "No History", "There is no history to export.")
            return

        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Export History", "", "CSV Files (*.csv);;Text Files (*.txt);;All Files (*)")
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    # Write header
                    file.write("Date,Algorithm,Operation,Content\n")
                    # Write data
                    for entry in self.history_data:
                        file.write(f"{entry['date']},{entry['algorithm']},{entry['operation']},{entry['content']}\n")
                self.ui.status_label.setText(f"History exported to {os.path.basename(file_path)}")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error", f"Failed to export history: {str(e)}")
                logging.error(f"Failed to export history: {str(e)}")

    def load_history_item(self):
        selected_rows = self.ui.history_table.selectedItems()
        if not selected_rows:
            QtWidgets.QMessageBox.information(self, "No Selection", "Please select a history item to load.")
            return

        row = selected_rows[0].row()
        entry = self.history_data[row]  # Assuming history_data is up-to-date with table

        # Find the index of the algorithm in the dropdown
        algo_index = self.ui.algorithm_dropdown.findText(entry["algorithm"])
        if algo_index != -1:
            self.ui.algorithm_dropdown.setCurrentIndex(algo_index)
        else:
            # Handle case where algorithm is not in the dropdown (should not happen with current setup)
            self.ui.algorithm_dropdown.setCurrentIndex(0)  # Default to first

        # Set operation mode
        if entry["operation"] == "Encryption":
            self.ui.encrypt_radio.setChecked(True)
        else:
            self.ui.decrypt_radio.setChecked(True)

        # Set input and key
        self.ui.input_text_edit.setText(entry["input"])
        self.ui.key_input_sidebar.setText(entry["key"])  # Use sidebar key input

        # Switch to encryption tab
        self.ui.main_tab_widget.setCurrentIndex(0)
        self.ui.status_label.setText(f"Loaded history item from {entry['date']}")

    def view_history_item(self, row):
        entry = self.history_data[row]

        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("History Item Details")
        dialog.resize(500, 400)

        layout = QtWidgets.QVBoxLayout(dialog)

        # Create labels and fields
        info_layout = QtWidgets.QFormLayout()
        info_layout.addRow("Date:", QtWidgets.QLabel(entry["date"]))
        info_layout.addRow("Algorithm:", QtWidgets.QLabel(entry["algorithm"]))
        info_layout.addRow("Operation:", QtWidgets.QLabel(entry["operation"]))

        # Create text areas for input and output
        input_label = QtWidgets.QLabel("Input:")
        input_text = QtWidgets.QTextEdit()
        input_text.setPlainText(entry["input"])
        input_text.setReadOnly(True)

        output_label = QtWidgets.QLabel("Output:")
        output_text = QtWidgets.QTextEdit()
        output_text.setPlainText(entry["output"])
        output_text.setReadOnly(True)

        key_layout = QtWidgets.QHBoxLayout()
        key_layout.addWidget(QtWidgets.QLabel("Key:"))
        key_text = QtWidgets.QLineEdit(entry["key"])
        key_text.setReadOnly(True)
        key_layout.addWidget(key_text)

        # Add components to layout
        layout.addLayout(info_layout)
        layout.addWidget(input_label)
        layout.addWidget(input_text)
        layout.addWidget(output_label)
        layout.addWidget(output_text)
        layout.addLayout(key_layout)

        # Add close button
        close_button = QtWidgets.QPushButton("Close")
        close_button.clicked.connect(dialog.accept)
        layout.addWidget(close_button)

        dialog.exec_()

    def delete_history_item(self, row):
        reply = QtWidgets.QMessageBox.question(
            self, "Delete History Item",
            "Are you sure you want to delete this history item?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )
        if reply == QtWidgets.QMessageBox.Yes:
            del self.history_data[row]
            self.update_history_table()  # This will re-render with correct indices
            self.ui.status_label.setText("History item deleted")

    def filter_history(self):
        filter_text = self.ui.history_filter_combo.currentText()
        # Filter based on selected filter
        filtered_data = []

        if filter_text == "All Operations":
            filtered_data = self.history_data
        elif filter_text == "Encryption":
            filtered_data = [entry for entry in self.history_data if entry["operation"] == "Encryption"]
        elif filter_text == "Decryption":
            filtered_data = [entry for entry in self.history_data if entry["operation"] == "Decryption"]

        self.ui.history_table.setRowCount(0)  # Clear table

        for i, entry in enumerate(filtered_data):
            self.ui.history_table.insertRow(i)
            self.ui.history_table.setItem(i, 0, QtWidgets.QTableWidgetItem(entry["date"]))
            self.ui.history_table.setItem(i, 1, QtWidgets.QTableWidgetItem(entry["algorithm"]))
            self.ui.history_table.setItem(i, 2, QtWidgets.QTableWidgetItem(entry["operation"]))
            self.ui.history_table.setItem(i, 3, QtWidgets.QTableWidgetItem(entry["content"]))

            # Create action buttons
            actions_widget = QtWidgets.QWidget()
            actions_layout = QtWidgets.QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(2, 2, 2, 2)
            actions_layout.setSpacing(4)

            view_btn = QtWidgets.QPushButton()
            view_btn.setIcon(load_icon('eye', 16))
            view_btn.setFixedSize(24, 24)
            view_btn.setFlat(True)
            view_btn.setToolTip("View Details")

            # Use the original index from history_data for the lambdas
            original_index = self.history_data.index(entry)
            view_btn.clicked.connect(lambda _, idx=original_index: self.view_history_item(idx))

            delete_btn = QtWidgets.QPushButton()
            delete_btn.setIcon(load_icon('delete', 16))
            delete_btn.setFixedSize(24, 24)
            delete_btn.setFlat(True)
            delete_btn.setToolTip("Delete Entry")
            delete_btn.clicked.connect(lambda _, idx=original_index: self.delete_history_item(idx))

            actions_layout.addWidget(view_btn)
            actions_layout.addWidget(delete_btn)
            actions_layout.addStretch()

            self.ui.history_table.setCellWidget(i, 4, actions_widget)

    def search_history(self):
        search_text = self.ui.history_search.text().lower()
        if not search_text:
            self.filter_history()  # Reset to filtered view if search is cleared
            return

        # Determine base data from current filter
        filter_text = self.ui.history_filter_combo.currentText()
        if filter_text == "All Operations":
            base_data = self.history_data
        elif filter_text == "Encryption":
            base_data = [entry for entry in self.history_data if entry["operation"] == "Encryption"]
        elif filter_text == "Decryption":
            base_data = [entry for entry in self.history_data if entry["operation"] == "Decryption"]
        else:  # Should not happen
            base_data = self.history_data

        # Search in various fields
        search_results = []
        for entry in base_data:
            if (search_text in entry["date"].lower() or
                    search_text in entry["algorithm"].lower() or
                    search_text in entry["content"].lower() or
                    (entry.get("filename") and search_text in entry["filename"].lower())  # If filename exists
            ):
                search_results.append(entry)

        # Display search results
        self.ui.history_table.setRowCount(0)  # Clear table

        for i, entry in enumerate(search_results):
            self.ui.history_table.insertRow(i)
            self.ui.history_table.setItem(i, 0, QtWidgets.QTableWidgetItem(entry["date"]))
            self.ui.history_table.setItem(i, 1, QtWidgets.QTableWidgetItem(entry["algorithm"]))
            self.ui.history_table.setItem(i, 2, QtWidgets.QTableWidgetItem(entry["operation"]))
            self.ui.history_table.setItem(i, 3, QtWidgets.QTableWidgetItem(entry["content"]))

            # Create action buttons
            actions_widget = QtWidgets.QWidget()
            actions_layout = QtWidgets.QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(2, 2, 2, 2)
            actions_layout.setSpacing(4)

            view_btn = QtWidgets.QPushButton()
            view_btn.setIcon(load_icon('eye', 16))
            view_btn.setFixedSize(24, 24)
            view_btn.setFlat(True)
            view_btn.setToolTip("View Details")

            # Use the original index from history_data for the lambdas
            original_index = self.history_data.index(entry)
            view_btn.clicked.connect(lambda _, idx=original_index: self.view_history_item(idx))

            delete_btn = QtWidgets.QPushButton()
            delete_btn.setIcon(load_icon('delete', 16))
            delete_btn.setFixedSize(24, 24)
            delete_btn.setFlat(True)
            delete_btn.setToolTip("Delete Entry")
            delete_btn.clicked.connect(lambda _, idx=original_index: self.delete_history_item(idx))

            actions_layout.addWidget(view_btn)
            actions_layout.addWidget(delete_btn)
            actions_layout.addStretch()

            self.ui.history_table.setCellWidget(i, 4, actions_widget)

    def toggle_password_visibility(self, checked):
        if checked:
            self.ui.key_input.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.ui.show_password_btn.setIcon(load_icon('eye_crossed', 18))
            self.ui.show_password_btn.setToolTip("Hide Password")
        else:
            self.ui.key_input.setEchoMode(QtWidgets.QLineEdit.Password)
            self.ui.show_password_btn.setIcon(load_icon('eye', 18))
            self.ui.show_password_btn.setToolTip("Show Password")

    def new_operation(self):
        self.ui.input_text_edit.clear()
        self.ui.output_text_edit.clear()
        self.ui.key_input_sidebar.clear()  # Clear sidebar key input
        self.ui.key_input.clear()  # Clear main panel key input
        self.ui.status_label.setText("Ready for new operation")
        # Reset operation mode to encrypt
        self.ui.encrypt_radio.setChecked(True)
        # Reset progress bar
        self.ui.operation_progress.setValue(0)
        # Focus on input text
        self.ui.input_text_edit.setFocus()
        # Switch to encryption tab if not already there
        self.ui.main_tab_widget.setCurrentIndex(0)

    def save_result(self):
        """Redirect to save_output_file for consistency"""
        self.save_output_file()

    def show_history_tab(self):
        self.ui.main_tab_widget.setCurrentIndex(2)  # Index 2 is the history tab

    def show_help(self):
        help_text = """
        <h2>EncryptPro Help</h2>
        <p>EncryptPro is a cryptographic tool that allows you to encrypt and decrypt text using various algorithms.</p>

        <h3>Basic Usage:</h3>
        <ol>
            <li>Select an algorithm from the dropdown on the left sidebar.</li>
            <li>Choose whether to encrypt or decrypt using the radio buttons.</li>
            <li>Enter the text to process in the 'INPUT' area.</li>
            <li>Enter a key in the 'KEY' field on the sidebar (if required by the algorithm).</li>
            <li>Click the 'ENCRYPT' or 'DECRYPT' button on the sidebar.</li>
            <li>View the result in the 'OUTPUT' area.</li>
        </ol>

        <h3>Features:</h3>
        <ul>
            <li>Support for multiple cryptographic algorithms (Caesar, Playfair, AES, RSA, etc.).</li>
            <li>Text and file encryption/decryption (File operations are on the 'File Operations' tab).</li>
            <li>Operation history tracking on the 'History' tab.</li>
            <li>Key generation assistance (sidebar 'Generate' button).</li>
            <li>Dark and light theme options (sidebar 'APPEARANCE' buttons).</li>
            <li>Key strength meter for password-based keys.</li>
        </ul>

        <p>For more detailed information about specific algorithms, consult external cryptographic resources.</p>
        <p>File operations allow batch processing of files. AES is recommended for binary files.</p>
        """
        msg_box = QtWidgets.QMessageBox(self)
        msg_box.setWindowTitle("EncryptPro Help")
        msg_box.setTextFormat(QtCore.Qt.RichText)
        msg_box.setText(help_text)
        msg_box.setIcon(QtWidgets.QMessageBox.Information)
        # Ensure the QMessageBox uses the application's stylesheet for consistency
        msg_box.setStyleSheet(self.styleSheet())
        msg_box.exec_()

    def show_settings(self):
        settings_dialog = QtWidgets.QDialog(self)
        settings_dialog.setWindowTitle("Settings")
        settings_dialog.resize(400, 300)
        settings_dialog.setStyleSheet(self.styleSheet())  # Apply main window style

        layout = QtWidgets.QVBoxLayout(settings_dialog)

        # Theme settings
        theme_group = QtWidgets.QGroupBox("Theme")
        theme_layout = QtWidgets.QVBoxLayout()
        dark_radio = QtWidgets.QRadioButton("Dark Theme")
        light_radio = QtWidgets.QRadioButton("Light Theme")

        # Check current theme (simplified)
        if "background-color: #121212;" in self.styleSheet().lower():  # Basic check for dark theme
            dark_radio.setChecked(True)
        else:
            light_radio.setChecked(True)

        theme_layout.addWidget(dark_radio)
        theme_layout.addWidget(light_radio)
        theme_group.setLayout(theme_layout)
        layout.addWidget(theme_group)

        # Logging settings (example)
        logging_group = QtWidgets.QGroupBox("Logging")
        logging_layout = QtWidgets.QVBoxLayout()
        log_check = QtWidgets.QCheckBox("Enable detailed logging (Restart may be needed)")
        log_check.setChecked(logging.getLogger().getEffectiveLevel() <= logging.INFO)  # Example check
        log_path_label = QtWidgets.QLabel(
            f"Log file: {logging.getLogger().handlers[0].baseFilename if logging.getLogger().handlers else 'N/A'}")
        logging_layout.addWidget(log_check)
        logging_layout.addWidget(log_path_label)
        logging_group.setLayout(logging_layout)
        layout.addWidget(logging_group)

        # Buttons
        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        buttons.accepted.connect(settings_dialog.accept)
        buttons.rejected.connect(settings_dialog.reject)
        layout.addWidget(buttons)

        if settings_dialog.exec_() == QtWidgets.QDialog.Accepted:
            # Apply settings
            if dark_radio.isChecked():
                self.set_theme("dark")
            else:
                self.set_theme("light")

            if log_check.isChecked():
                logging.getLogger().setLevel(logging.INFO)  # Example: set to INFO
            else:
                logging.getLogger().setLevel(logging.ERROR)  # Example: set back to ERROR
            self.ui.status_label.setText("Settings applied.")

    def update_key_strength(self, text=None):
        key = self.ui.key_input_sidebar.text() if text is None else text  # Use sidebar key for strength
        strength = 0
        if len(key) >= 8:
            strength += 25
        if len(key) >= 12:
            strength += 25
        if any(c.isdigit() for c in key):
            strength += 15
        if any(c.isupper() for c in key) and any(c.islower() for c in key):
            strength += 15
        if any(not c.isalnum() for c in key):  # Check for symbols
            strength += 20

        strength = min(strength, 100)  # Cap at 100
        self.ui.key_strength_meter.setValue(strength)

        if strength < 30:
            strength_text = "Weak"
            self.ui.key_strength_meter.setStyleSheet("""
                        QProgressBar { background-color: #252538; border-radius: 4px; }
                        QProgressBar::chunk { background-color: #FF5858; border-radius: 3px; }
                    """)
        elif strength < 60:
            strength_text = "Medium"
            self.ui.key_strength_meter.setStyleSheet("""
                        QProgressBar { background-color: #252538; border-radius: 4px; }
                        QProgressBar::chunk { background-color: #FFDE59; border-radius: 3px; }
                    """)
        elif strength < 80:
            strength_text = "Strong"
            self.ui.key_strength_meter.setStyleSheet("""
                        QProgressBar { background-color: #252538; border-radius: 4px; }
                        QProgressBar::chunk { background-color: #77DD77; border-radius: 3px; }
                    """)
        else:
            strength_text = "Very Strong"
            self.ui.key_strength_meter.setStyleSheet("""
                        QProgressBar { background-color: #252538; border-radius: 4px; }
                        QProgressBar::chunk { background-color: #4EC2F7; border-radius: 3px; }
                    """)

        self.ui.strength_label.setText(strength_text)

    def set_theme(self, theme):
        # This method implements proper theme switching between dark and light modes
        if theme == "light":
            try:
                # Light theme stylesheet
                light_stylesheet = """
                QMainWindow, QWidget {
                    background-color: #F0F0F0; 
                    color: #121212;
                    font-family: 'Segoe UI', Arial, sans-serif;
                    font-size: 13px;
                }
                
                QFrame, QGroupBox, QTabWidget::pane {
                    background-color: #FFFFFF;
                    border-radius: 12px;
                    border: 1px solid #D0D0D0;
                }
                
                QPushButton {
                    background-color: #E0E0E0;
                    color: #121212;
                    border: 1px solid #C0C0C0;
                    border-radius: 8px;
                    padding: 10px 18px;
                    font-weight: 600;
                }
                
                QPushButton:hover {
                    background-color: #D0D0D0;
                }
                
                QPushButton:pressed {
                    background-color: #C0C0C0;
                }
                
                QPushButton#execute_operation_btn {
                    background-color: #0078D7;
                    color: white;
                    font-size: 15px;
                    border-radius: 10px;
                    min-height: 48px;
                    margin: 5px 0;
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0078D7, stop:1 #1E88E5);
                }
                
                QPushButton#execute_operation_btn:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1E88E5, stop:1 #42A5F5);
                }
                
                QPushButton#execute_operation_btn.decrypt {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #2E7D32, stop:1 #388E3C);
                }
                
                QPushButton#execute_operation_btn.decrypt:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #388E3C, stop:1 #43A047);
                }
                
                QListWidget, QTableWidget {
                    background-color: #FFFFFF;
                    color: #121212;
                    border-radius: 8px;
                    border: 1px solid #D0D0D0;
                    padding: 6px;
                }
                
                QListWidget::item, QTableWidget::item {
                    border-radius: 4px;
                    padding: 4px 6px;
                    margin: 2px 0;
                }
                
                QListWidget::item:selected, QTableWidget::item:selected {
                    background-color: #0078D7;
                    color: white;
                }
                
                QListWidget::item:hover, QTableWidget::item:hover {
                    background-color: #E0E0E0;
                }
                
                QTextEdit, QLineEdit {
                    background-color: #FFFFFF;
                    color: #121212;
                    border: 1px solid #C0C0C0;
                    border-radius: 8px;
                    padding: 10px;
                    selection-background-color: #0078D7;
                    selection-color: white;
                }
                
                QTextEdit:focus, QLineEdit:focus {
                    border: 1px solid #0078D7;
                }
                
                QLabel#app_title {
                    color: #0078D7;
                    font-size: 24px;
                    font-weight: bold;
                    margin-bottom: 10px;
                }
                
                QLabel#section_title {
                    color: #0078D7;
                    font-size: 15px;
                    font-weight: bold;
                    margin-top: 10px;
                }
                
                QLabel#input_label, QLabel#output_label {
                    color: #0078D7;
                    font-size: 16px;
                    font-weight: bold;
                    margin-bottom: 5px;
                }
                
                QProgressBar {
                    border: none;
                    border-radius: 8px;
                    background-color: #E0E0E0;
                    height: 10px;
                    text-align: center;
                }
                
                QProgressBar::chunk {
                    background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #FF5858, stop:0.5 #FFDE59, stop:1 #0078D7);
                    border-radius: 8px;
                }
                
                QTabBar::tab {
                    background-color: #E0E0E0;
                    color: #121212;
                    border-top-left-radius: 8px;
                    border-top-right-radius: 8px;
                    padding: 12px 20px;
                    margin-right: 4px;
                    font-weight: 500;
                }
                
                QTabBar::tab:selected {
                    background-color: #0078D7;
                    color: white;
                }
                
                QTabBar::tab:hover:!selected {
                    background-color: #D0D0D0;
                }
                
                QComboBox {
                    background-color: #E0E0E0;
                    border: 1px solid #C0C0C0;
                    border-radius: 6px;
                    padding: 5px 10px;
                    min-height: 25px;
                    color: #121212;
                }
                
                QComboBox:hover {
                    background-color: #D0D0D0;
                    border: 1px solid #0078D7;
                }
                
                QComboBox QAbstractItemView {
                    border: 1px solid #C0C0C0;
                    background-color: #FFFFFF;
                    border-radius: 0 0 6px 6px;
                    outline: 0px;
                    color: #121212;
                }
                """
                
                # Apply the light stylesheet to the application
                self.setStyleSheet(light_stylesheet)
                self.ui.status_label.setText("Switched to light theme")
                
            except Exception as e:
                logging.error(f"Error applying light theme: {e}")
                self.ui.status_label.setText("Error applying light theme")
        else:  # Dark theme (default)
            try:
                # Get the original dark stylesheet from the UI
                dark_stylesheet = self.ui.centralWidget.styleSheet()
                self.setStyleSheet(dark_stylesheet)
                self.ui.status_label.setText("Switched to dark theme")
            except Exception as e:
                logging.error(f"Error applying dark theme: {e}")
                self.ui.status_label.setText("Error applying dark theme")
        
        # Force UI update
        self.repaint()

    def clear_input(self):
        reply = QtWidgets.QMessageBox.question(
            self, "Clear Input",
            "Are you sure you want to clear the input text?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )
        if reply == QtWidgets.QMessageBox.Yes:
            self.ui.input_text_edit.clear()
            self.ui.status_label.setText("Input cleared")

    def load_input_file(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Select Input File", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    self.ui.input_text_edit.setText(file.read())
                self.ui.status_label.setText(f"Loaded input from {os.path.basename(file_path)}")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error", f"Failed to load file: {str(e)}")
                logging.error(f"Failed to load input file: {str(e)}")

    def generate_key(self):
        # Get currently selected algorithm from dropdown
        algo_name = self.ui.algorithm_dropdown.currentText()
        key = ""

        # Generate key based on algorithm type
        if algo_name == "ROT13":
            QtWidgets.QMessageBox.information(self, "ROT13", "ROT13 does not require a key.")
            self.ui.key_input_sidebar.clear()
            return

        if algo_name == "Caesar Cipher":
            key = str(random.randint(1, 25))
        elif algo_name == "Playfair Cipher":
            # Generate a keyword without repeating letters, then pad if necessary
            alphabet = list(string.ascii_uppercase.replace('J', ''))  # Playfair typically omits J or treats I/J as one
            random.shuffle(alphabet)
            key_len = random.randint(5, 10)
            key = "".join(secrets.choice(string.ascii_uppercase.replace('J', '')) for _ in range(key_len))
            key = "".join(dict.fromkeys(key))  # Remove duplicates while preserving order
        elif algo_name == "Rail Fence":
            key = str(random.randint(2, 10))
        elif algo_name == "Row Transposition":
            cols = random.randint(3, 8)
            key_list = random.sample(range(1, cols + 1), cols)
            key = " ".join(map(str, key_list))  # e.g., "3 1 4 2"
        elif algo_name == "Hill Cipher":
            # Generate a 2x2 or 3x3 invertible matrix over Z_26
            # This is complex to do correctly and ensure invertibility.
            # For demo, provide simple valid keys.
            # A 2x2 example: key = "5 8 17 3" (det = 15 - 136 = -121 === 9 mod 26, gcd(9,26)=1)
            # A 3x3 example is much harder.
            # Using pre-defined simple ones for generation for now.
            if random.choice([True, False]):  # 2x2
                while True:
                    matrix = [random.randint(0, 25) for _ in range(4)]
                    det = (matrix[0] * matrix[3] - matrix[1] * matrix[2]) % 26
                    if math.gcd(det, 26) == 1:
                        key = f"{matrix[0]},{matrix[1]},{matrix[2]},{matrix[3]}"
                        break
            else:  # Placeholder for 3x3, very hard to generate random invertible
                key = "6,24,1,13,16,10,20,17,15"  # Example known invertible 3x3
        elif algo_name == "Substitution Cipher":
            alphabet = list(string.ascii_uppercase)
            random.shuffle(alphabet)
            key = ''.join(alphabet)
        elif algo_name == "Vigenère Cipher":
            length = random.randint(5, 15)
            key = ''.join(secrets.choice(string.ascii_uppercase) for _ in range(length))
        elif algo_name == "Chris Way Cipher V1":
            QtWidgets.QMessageBox.information(self, "Chris Way Cipher V1", 
                                            "Chris Way Cipher V1 does not require a key. It uses character positions for encryption.")
            self.ui.key_input_sidebar.clear()
            return
        elif algo_name == "Chris Way Cipher V2":
            # Generate public and private key pair
            public_key_length = random.randint(6, 12)
            private_key_length = random.randint(6, 12)
            
            public_key = ''.join(secrets.choice(string.ascii_uppercase) for _ in range(public_key_length))
            private_key = ''.join(secrets.choice(string.ascii_uppercase) for _ in range(private_key_length))
            
            # Ask if user wants to use public or private key
            msg_box = QtWidgets.QMessageBox(self)
            msg_box.setWindowTitle("Chris Way Cipher V2 - Key Selection")
            msg_box.setText("Generated key pair for Chris Way Cipher V2:\n\n" +
                           f"Public Key (for encryption): {public_key}\n" +
                           f"Private Key (for decryption): {private_key}\n\n" +
                           "Which key would you like to use?")
            encrypt_btn = msg_box.addButton("Use Public Key (encrypt)", QtWidgets.QMessageBox.YesRole)
            decrypt_btn = msg_box.addButton("Use Private Key (decrypt)", QtWidgets.QMessageBox.NoRole)
            cancel_btn = msg_box.addButton("Cancel", QtWidgets.QMessageBox.RejectRole)
            
            msg_box.exec_()
            
            if msg_box.clickedButton() == cancel_btn:
                return
            elif msg_box.clickedButton() == encrypt_btn:
                key = public_key
                # Set operation to encrypt
                self.ui.encrypt_radio.setChecked(True)
            else:  # decrypt button
                key = private_key
                # Set operation to decrypt
                self.ui.decrypt_radio.setChecked(True)
                
            # Update execute button style based on operation
            self.update_execute_button_style()
            
        elif algo_name == "RSA":
            # RSA key generation is computationally intensive and complex.
            # For a "generate" button, we'd typically show placeholder or pre-generated demo keys.
            # True RSA key gen would involve finding large primes, etc.
            # Example public key (e, N) and private key (d, N)
            # These are extremely small for demo only and not secure.
            QtWidgets.QMessageBox.information(self, "RSA Not Available", 
                                            "RSA has been replaced with Chris Way Ciphers in this version.\n\n"
                                            "Please select either Chris Way Cipher V1 or V2 instead.")
            return
        elif algo_name == "AES":
            # Ask user if they want a text key or hex key
            msg_box = QtWidgets.QMessageBox(self)
            msg_box.setWindowTitle("AES Key Format")
            msg_box.setText("Generate AES key in which format?")
            text_button = msg_box.addButton("Text Key", QtWidgets.QMessageBox.YesRole)
            hex_button = msg_box.addButton("Hex Key (0x prefix)", QtWidgets.QMessageBox.NoRole)
            msg_box.setDefaultButton(text_button)
            msg_box.exec_()
            
            if msg_box.clickedButton() == hex_button:  # Hex key
                # Generate random hex key (32, 48, or 64 hex chars for AES-128, AES-192, AES-256)
                key_size = random.choice([16, 24, 32])  # Bytes (not hex characters)
                hex_key = self.generate_hex_aes_key(key_size)
                key = f"0x{hex_key}"
            else:  # Text key
                # AES keys are typically 128, 192, or 256 bits.
                # Often represented as hex strings or raw bytes. For text input, a passphrase is common.
                # Here, generate a random string suitable as a passphrase.
                key_length = random.choice([16, 24, 32])  # Corresponds to AES-128, AES-192, AES-256 if bytes
                key = ''.join(
                    secrets.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(key_length))
        else:  # Default generic key
            key = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))

        self.ui.key_input_sidebar.setText(key)
        self.ui.status_label.setText(f"Generated key for {algo_name}")
        self.update_key_strength(key)  # Update strength meter as well
        
    def generate_hex_aes_key(self, key_size_bytes):
        """Generate a secure random hexadecimal key for AES encryption.
        
        Args:
            key_size_bytes: Key size in bytes (16, 24, or 32)
            
        Returns:
            str: Hexadecimal string (without 0x prefix)
        """
        try:
            # Generate random bytes
            random_bytes = secrets.token_bytes(key_size_bytes)
            # Convert to hex
            hex_key = random_bytes.hex()
            return hex_key
        except Exception as e:
            logging.error(f"Error generating hex key: {str(e)}")
            # Fallback method
            hex_chars = "0123456789ABCDEF"
            hex_key = ''.join(random.choice(hex_chars) for _ in range(key_size_bytes * 2))
            return hex_key

    def generate_random_key(self):
        """Generate a cryptographically secure random key, more generic than algorithm-specific one"""
        try:
            algo_name = self.ui.algorithm_dropdown.currentText()
            if algo_name == "ROT13":
                QtWidgets.QMessageBox.information(self, "ROT13", "ROT13 does not require a key.")
                self.ui.key_input_sidebar.clear()
                return

            # For most algorithms, a strong passphrase/key string is useful.
            # AES benefits most directly from raw byte strength, but others use it as a seed or literal key.
            key_length = random.choice([16, 24, 32])  # Good lengths for passphrases
            # Using a wide character set for strong random keys
            chars = string.ascii_letters + string.digits + '!@#$%^&*()-_=+[]{};:,.<>/?~`'
            key = ''.join(secrets.choice(chars) for _ in range(key_length))

            # Specific handling if needed, otherwise, the strong random string is generally good.
            if algo_name == "Caesar Cipher":
                key = str(secrets.randbelow(25) + 1)  # Random shift from 1 to 25
            elif algo_name == "Rail Fence":
                key = str(secrets.randbelow(18) + 2)  # Rails from 2 to 20
            elif algo_name == "RSA":  # RSA has very specific key structure
                self.generate_key()  # Fallback to the specific RSA key gen message
                self.ui.status_label.setText(f"Used specific RSA key info for {algo_name}")
                return  # RSA structure is too specific for generic random string

            self.ui.key_input_sidebar.setText(key)
            self.ui.status_label.setText(f"Generated strong random key for {algo_name}")
            self.update_key_strength(key)

        except Exception as e:
            logging.error(f"Error generating random key: {str(e)}")
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to generate random key: {str(e)}")

    def process_files(self):
        # Check if files are selected
        if self.ui.file_list.count() == 0:
            QtWidgets.QMessageBox.warning(self, "No Files", "Please select files to process.")
            return
            
        # Get algorithm from dropdown
        algo_name = self.ui.algorithm_dropdown.currentText()
        
        # Get key from sidebar
        key = self.ui.key_input_sidebar.text()
        
        # Validate key using the same validation function as for text operations
        # For files, we can't validate text content beforehand, but we can validate the key
        validation_error = self.validate_key_only(algo_name, key)
        if validation_error:
            QtWidgets.QMessageBox.warning(self, "Key Validation Error", validation_error)
            return
            
        # Check output directory
        output_dir = self.ui.output_dir_input.text()
        if not output_dir:
            QtWidgets.QMessageBox.warning(self, "No Output Directory", "Please select an output directory.")
            return
            
        # Map algorithm names to classes
        algo_map = {
            "Caesar Cipher": CaesarCipher,
            "Playfair Cipher": PlayfairCipher,
            "Rail Fence": RailFenceCipher,
            "Row Transposition": RowTranspositionCipher,
            "Hill Cipher": HillCipher,
            "Substitution Cipher": SubstitutionCipher,
            "Vigenère Cipher": VigenereCipher,
            "AES": AESCipher,
            "ROT13": Rot13Cipher,
            "Chris Way Cipher V1": ChrisWayV1Cipher,
            "Chris Way Cipher V2": ChrisWayV2Cipher,
        }
        
        cipher_class = algo_map.get(algo_name)
        if not cipher_class:
            QtWidgets.QMessageBox.information(self, "Not Implemented", f"{algo_name} is not implemented yet.")
            return
            
        # Get operation mode
        mode = "Encryption" if self.ui.encrypt_radio.isChecked() else "Decryption"
        
        # Process each file
        processed_files = 0
        errors = 0
        
        # Setup progress dialog
        progress = QtWidgets.QProgressDialog(f"{mode} files...", "Cancel", 0, self.ui.file_list.count(), self)
        progress.setWindowTitle(f"File {mode}")
        progress.setWindowModality(QtCore.Qt.WindowModal)
        
        for i in range(self.ui.file_list.count()):
            if progress.wasCanceled():
                break
                
            progress.setValue(i)
            
            item = self.ui.file_list.item(i)
            file_path = item.data(QtCore.Qt.UserRole)
            file_name = os.path.basename(file_path)
            
            try:
                # Special handling for AES which can handle binary data properly
                if algo_name == "AES":
                    self.process_file_with_aes(file_path, output_dir, key, mode, cipher_class)
                    processed_files += 1
                    continue
                
                # For other algorithms, process as text
                try:
                    # Try to read file as text first
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                except UnicodeDecodeError:
                    # If it fails, warn that only AES supports binary data properly
                    QtWidgets.QMessageBox.warning(
                        self,
                        "Binary File Detected",
                        f"The file {file_name} appears to be binary. Only AES supports binary files properly."
                    )
                    errors += 1
                    continue
                
                # Validate file content for the specific algorithm
                content_error = self.validate_text_content(algo_name, content)
                if content_error:
                    QtWidgets.QMessageBox.warning(
                        self,
                        "File Content Error",
                        f"File '{file_name}': {content_error}"
                    )
                    errors += 1
                    continue
                
                # Process text content
                if mode == "Encryption":
                    if algo_name == "ROT13":
                        result = cipher_class.encrypt(content)
                    elif algo_name == "Chris Way Cipher V1":
                        result = cipher_class.encrypt(content)
                    else:
                        result = cipher_class.encrypt(content, key)
                else:  # Decryption
                    if algo_name == "ROT13":
                        result = cipher_class.decrypt(content)
                    elif algo_name == "Chris Way Cipher V1":
                        result = cipher_class.decrypt(content)
                    else:
                        result = cipher_class.decrypt(content, key)
                
                # Create output file name with appropriate extension
                if algo_name.startswith("Chris Way Cipher"):
                    extension = ".cw1" if algo_name == "Chris Way Cipher V1" else ".cw2"
                    extension += ".enc" if mode == "Encryption" else ".dec"
                else:
                    extension = ".enc" if mode == "Encryption" else ".dec"
                
                output_file = os.path.join(output_dir, f"{file_name}{extension}")
                
                # Write result to output file
                with open(output_file, 'w', encoding='utf-8') as file:
                    file.write(result)
                    
                processed_files += 1
                
                # Add to history
                self.add_file_op_to_history(file_name, algo_name, mode, key)
                
            except Exception as e:
                errors += 1
                logging.error(f"Error processing file {file_name}: {str(e)}")
                QtWidgets.QMessageBox.warning(
                    self,
                    "File Processing Error",
                    f"Error processing {file_name}: {str(e)}"
                )
        
        progress.setValue(self.ui.file_list.count())
        
        # Show summary
        if errors > 0:
            QtWidgets.QMessageBox.warning(
                self, 
                "Processing Complete with Errors", 
                f"Processed {processed_files} files successfully.\n{errors} files had errors. Check the log for details."
            )
        else:
            QtWidgets.QMessageBox.information(
                self, 
                "Processing Complete", 
                f"Successfully processed {processed_files} files.\nOutput saved to: {output_dir}"
            )
        
        self.ui.status_label.setText(f"File {mode} complete: {processed_files} files processed")
    
    def validate_key_only(self, algo_name, key):
        """Validate only the key for file operations."""
        # Algorithm-specific key validations
        if algo_name == "Caesar Cipher":
            # Key: Integer (1-25)
            if not key or not key.isdigit():
                return "Caesar Cipher requires a numeric key."
            
            key_int = int(key)
            if not (1 <= key_int <= 25):
                return "Caesar Cipher key must be an integer between 1 and 25."
                
        elif algo_name == "Substitution Cipher":
            # Key: A 26-character unique substitution mapping (no repeats)
            if not key or len(key) != 26:
                return "Substitution Cipher requires a 26-character key."
                
            key_upper = key.upper()
            if not all(c.isalpha() for c in key_upper):
                return "Substitution Cipher key must contain only letters."
                
            if len(set(key_upper)) != 26:
                return "Substitution Cipher key must contain all 26 letters with no repeats."
                
        elif algo_name == "ROT13":
            # No key required for ROT13
            if key:
                return "ROT13 does not require a key."
                
        elif algo_name == "Playfair Cipher":
            # Key: Required (letters only)
            if not key:
                return "Playfair Cipher requires a keyword."
                
            if not all(c.isalpha() for c in key):
                return "Playfair Cipher key must contain only letters."
                
        elif algo_name == "Rail Fence":
            # Key: Integer ≥ 2
            if not key or not key.isdigit():
                return "Rail Fence Cipher requires a numeric key."
                
            key_int = int(key)
            if key_int < 2:
                return "Rail Fence Cipher key must be an integer >= 2."
                
        elif algo_name == "Hill Cipher":
            # Key: Square matrix with inverse mod 26
            if not key:
                return "Hill Cipher requires a key matrix."
                
            key_parts = key.split(',')
            if not all(part.strip().isdigit() for part in key_parts):
                return "Hill Cipher key must be comma-separated integers."
                
            # Check if it's a square matrix
            n = int(len(key_parts) ** 0.5)
            if n*n != len(key_parts):
                return "Hill Cipher key must form a square matrix (e.g., 4 numbers for 2x2, 9 for 3x3)."
                
            # Matrix size validation for plaintext
            clean_text = ''.join(c for c in input_text if c.isalpha())
            if len(clean_text) % n != 0:
                return f"Hill Cipher plaintext length must be a multiple of {n} (matrix size)."
                
        elif algo_name == "Vigenère Cipher":
            # Key: Letters only
            if not key:
                return "Vigenère Cipher requires a key."
                
            if not all(c.isalpha() for c in key):
                return "Vigenère Cipher key must contain only letters."
                
        elif algo_name == "Chris Way Cipher V1":
            # No key required for V1
            if key:
                return "Chris Way Cipher V1 does not require a key."
                
        elif algo_name == "Chris Way Cipher V2":
            # Key validation for V2
            if not key:
                return "Chris Way Cipher V2 requires an alphabetic key."
                
            if not all(c.isalpha() for c in key):
                return "Chris Way Cipher V2 key must contain only letters."
                
            if len(key) < 3:
                return "Chris Way Cipher V2 key should be at least 3 characters long."
                
        elif algo_name == "AES":
            # Key validation for both text and hex formats
            if not key:
                return "AES Cipher requires a key."
                
            # Check if key is in hex format (with or without 0x prefix)
            is_hex = False
            clean_key = key
            if key.startswith('0x'):
                clean_key = key[2:]
                is_hex = True
            elif all(c in "0123456789ABCDEFabcdef" for c in key):
                is_hex = True
                
            if is_hex:
                # Check hex key length for AES-128 (32 chars), AES-192 (48 chars), or AES-256 (64 chars)
                hex_lengths = [32, 48, 64]
                if len(clean_key) not in hex_lengths:
                    return f"Hex AES key must be {', '.join(str(l) for l in hex_lengths)} characters long (current: {len(clean_key)})."
            else:
                # Standard text key
                key_len = len(key)
                if key_len not in [16, 24, 32]:
                    return f"AES text key must be 16, 24, or 32 characters long (current: {key_len})."
        
        # Validation passed
        return None

    def validate_text_content(self, algo_name, content):
        """Validate only the text content based on algorithm requirements for file operations."""
        # For algorithms that need specific content validation
        if algo_name in ["Caesar Cipher", "Substitution Cipher", "Playfair Cipher", "Hill Cipher", "Vigenère Cipher", "ROT13", "Chris Way Cipher V1", "Chris Way Cipher V2"]:
            # These algorithms require text with letters only
            if not all(c.isalpha() or c.isspace() for c in content):
                return f"{algo_name} requires text with letters only (A-Z, a-z, spaces)."
                
        # For Hill cipher, we need additional validation
        if algo_name == "Hill Cipher":
            # Matrix size validation for plaintext
            key = self.ui.key_input_sidebar.text()
            key_parts = key.split(',')
            n = int(len(key_parts) ** 0.5)
            clean_text = ''.join(c for c in content if c.isalpha())
            if len(clean_text) % n != 0:
                return f"Hill Cipher plaintext length must be a multiple of {n} (matrix size)."
        
        # Other algorithms can handle any text
        return None

    def process_file_with_aes(self, file_path, output_dir, key, mode, cipher_class):
        """Dedicated AES file processing for robust binary handling."""
        file_name = os.path.basename(file_path)
        output_file_name_base = os.path.splitext(file_name)[0]
        import base64

        # Use CBC mode with hex output as requested
        aes_mode = "CBC"
        output_format = "hex"
        
        try:
            with open(file_path, 'rb') as f_in:
                binary_data = f_in.read()

            if mode == "Encryption":
                # The AESCipher.encrypt expects a string, so we base64 encode binary data
                content_to_encrypt = base64.b64encode(binary_data).decode('utf-8')
                
                # Check if key is in hex format
                is_hex_key = key.startswith('0x') or all(c in "0123456789ABCDEFabcdef" for c in key)
                if is_hex_key:
                    # For hex keys, make sure format is correct 
                    if key.startswith('0x'):
                        # Already correctly formatted
                        pass
                    else:
                        # Add 0x prefix for clarity
                        key = '0x' + key
                        self.ui.status_label.setText(f"Using hex key format: {key[:8]}...")
                
                encrypted_data = cipher_class.encrypt(content_to_encrypt, key, aes_mode, output_format)
                # The result is a formatted string with mode prefix, we can save directly
                output_file_path = os.path.join(output_dir, f"{output_file_name_base}.aes.enc")
                with open(output_file_path, 'w', encoding='utf-8') as f_out:
                    f_out.write(encrypted_data)
            else:  # Decryption
                # Read the encrypted data format string
                try:
                    with open(file_path, 'r', encoding='utf-8') as f_in_text:
                        encrypted_data = f_in_text.read()
                except UnicodeDecodeError:
                    raise ValueError(
                        f"File '{file_name}' is not a valid encrypted file format.")

                # Decrypt the data
                decrypted_data_b64 = cipher_class.decrypt(encrypted_data, key)
                # The result should be the base64 encoded binary data
                try:
                    original_binary_data = base64.b64decode(decrypted_data_b64)
                except Exception as e:
                    raise ValueError(f"Failed to decode decrypted data: {str(e)}")

                output_file_path = os.path.join(output_dir, f"{output_file_name_base}.dec")
                with open(output_file_path, 'wb') as f_out:
                    f_out.write(original_binary_data)
                    
            # Add to history
            self.add_file_op_to_history(file_name, "AES", mode, key)
                    
        except Exception as e:
            raise Exception(f"AES processing error for '{file_name}': {e}")

    def add_file_op_to_history(self, filename, algorithm, operation, key):
        import datetime
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history_data.append({
            "date": now,
            "algorithm": algorithm,
            "operation": operation,
            "content": f"File: {filename}",  # Indicate it's a file operation
            "key": "********" if key else "N/A",  # Mask key for file ops in history view for brevity/security
            "input": f"File: {filename}",  # Actual input data not stored for files
            "output": "File operation",  # Actual output data not stored
            "filename": filename  # Store filename for potential search
        })
        self.update_history_table()

    def copy_output(self):
        output_text = self.ui.output_text_edit.toPlainText()
        if not output_text:
            QtWidgets.QMessageBox.information(self, "No Output", "There is no output to copy.")
            return
        QtWidgets.QApplication.clipboard().setText(output_text)
        self.ui.status_label.setText("Output copied to clipboard")

    def save_output_file(self):
        output_text = self.ui.output_text_edit.toPlainText()
        if not output_text:
            QtWidgets.QMessageBox.information(self, "No Output", "There is no output to save.")
            return

        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save Output", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(output_text)
                self.ui.status_label.setText(f"Output saved to {os.path.basename(file_path)}")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error", f"Failed to save file: {str(e)}")
                logging.error(f"Failed to save output file: {str(e)}")

    def select_files(self):
        file_paths, _ = QtWidgets.QFileDialog.getOpenFileNames(
            self, "Select Files", "", "All Files (*)")
        if file_paths:
            for path in file_paths:
                item = QtWidgets.QListWidgetItem(os.path.basename(path))
                item.setData(QtCore.Qt.UserRole, path)  # Store full path in UserRole
                item.setToolTip(path)  # Show full path on hover
                self.ui.file_list.addItem(item)
            self.ui.status_label.setText(f"Added {len(file_paths)} files to list.")

    def select_folder(self):
        folder_path = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Select Folder Containing Files")
        if folder_path:
            count = 0
            try:
                for f_name in os.listdir(folder_path):
                    full_f_path = os.path.join(folder_path, f_name)
                    if os.path.isfile(full_f_path):
                        item = QtWidgets.QListWidgetItem(f_name)
                        item.setData(QtCore.Qt.UserRole, full_f_path)
                        item.setToolTip(full_f_path)
                        self.ui.file_list.addItem(item)
                        count += 1
                self.ui.status_label.setText(f"Added {count} files from folder '{os.path.basename(folder_path)}'.")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error", f"Failed to read folder contents: {str(e)}")
                logging.error(f"Failed to read folder: {str(e)}")

    def clear_file_list(self):
        if self.ui.file_list.count() > 0:
            reply = QtWidgets.QMessageBox.question(
                self, "Clear File List",
                "Are you sure you want to clear all files from the list?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.No
            )
            if reply == QtWidgets.QMessageBox.Yes:
                self.ui.file_list.clear()
                self.ui.status_label.setText("File list cleared.")

    def browse_output_directory(self):
        folder_path = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Select Output Directory for Processed Files")
        if folder_path:
            self.ui.output_dir_input.setText(folder_path)
            self.ui.status_label.setText(f"Output directory set to: {folder_path}")

class EncryptProApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_ui()
        self.history_data = []

    # ----------------------------------------------------------------------
    # Algorithm List Item Widget (Not used with QComboBox, but kept for reference)
    # ----------------------------------------------------------------------
    class AlgorithmListItemWidget(QtWidgets.QWidget):
        def __init__(self, name, parent=None):
            super().__init__(parent)
            layout = QtWidgets.QHBoxLayout(self)
            layout.setContentsMargins(8, 4, 8, 4)
            layout.setSpacing(12)
            # No icon label
            self.name_label = QtWidgets.QLabel(name)
            self.name_label.setStyleSheet("font-size: 14px; font-weight: 500; color: #EEEEEE;")
            self.name_label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
            # self.name_label.setMinimumWidth(80) # Adjust as needed
            # self.name_label.setMaximumWidth(150) # Adjust as needed
            self.name_label.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
            self.name_label.setWordWrap(False)
            self.name_label.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
            self.name_label.setMinimumHeight(28)
            self.name_label.setMaximumHeight(28)
            self.name_label.setToolTip(name)
            layout.addWidget(self.name_label, 1)  # Stretch factor for name_label

            self.info_btn = QtWidgets.QPushButton()
            self.info_btn.setIcon(load_icon('info', 18))
            self.info_btn.setIconSize(QtCore.QSize(18, 18))
            self.info_btn.setFixedSize(28, 28)
            self.info_btn.setFlat(True)  # Makes it look less like a full button
            self.info_btn.setStyleSheet("""
                    QPushButton { border-radius: 14px; background-color: transparent; }
                    QPushButton:hover { background-color: rgba(255,255,255,0.1); }
                    QPushButton:pressed { background-color: rgba(255,255,255,0.2); }
                """)
            self.info_btn.setToolTip("Algorithm Information (Placeholder)")
            layout.addWidget(self.info_btn)
            self.setLayout(layout)

    # ----------------------------------------------------------------------
    # Application Execution
    # ----------------------------------------------------------------------
    if __name__ == "__main__":
        app = QtWidgets.QApplication(sys.argv)

        # Show login dialog
        login_dialog = LoginDialog()
        # Apply stylesheet to login dialog as well for consistency
        # login_dialog.setStyleSheet(Ui_MainWindow().centralWidget.styleSheet()) # This is a bit hacky way to get the stylesheet
        # A better way is to have the QSS available globally or pass it

        if login_dialog.exec_() == QtWidgets.QDialog.Accepted:
            # Login successful, show main application
            window = EncryptProApp()
            window.show()
            sys.exit(app.exec_())
        else:
            # User cancelled login
            sys.exit(0)