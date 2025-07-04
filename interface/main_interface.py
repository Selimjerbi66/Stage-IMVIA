# main_interface.py

import sys
from PyQt6.QtWidgets import (  # Common Widgets
    QMainWindow, QWidget, QLabel, QPushButton,
    QLineEdit, QTextEdit, QCheckBox, QRadioButton, QComboBox,
    QVBoxLayout, QHBoxLayout, QGridLayout,
    QMenuBar, QMenu, QToolBar, QMessageBox, QFileDialog,
    QTabWidget
)
from PyQt6.QtCore import pyqtSignal, QObject  # Signals and Slots
from PyQt6.QtGui import QAction  # Menus and Toolbars


class MyObject(QObject):  # Signals and Slots
    my_signal = pyqtSignal()

    def trigger_signal(self):
        self.my_signal.emit()


class MainWindow(QMainWindow):  # Main Window Setup
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt6 Comprehensive Example")  # Window title
        self.resize(800, 600)  # Set Window Size

        # Central Widget and Layout
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        # Widgets
        self.label = QLabel("Hello, PyQt6!")
        self.line_edit = QLineEdit()
        self.text_edit = QTextEdit()
        self.check_box = QCheckBox("Check me")
        self.radio_button = QRadioButton("Option 1")
        self.combo_box = QComboBox()
        self.combo_box.addItems(["Option 1", "Option 2", "Option 3"])
        self.button = QPushButton("Click Me")

        # Layout Management
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.check_box)
        h_layout.addWidget(self.radio_button)

        grid_layout = QGridLayout()
        grid_layout.addWidget(self.label, 0, 0)
        grid_layout.addWidget(self.line_edit, 0, 1)
        grid_layout.addWidget(self.combo_box, 1, 0, 1, 2)

        main_layout.addWidget(self.button)
        main_layout.addLayout(h_layout)
        main_layout.addLayout(grid_layout)
        main_layout.addWidget(self.text_edit)

        # Signals and Slots
        self.my_object = MyObject()
        self.my_object.my_signal.connect(lambda: print("Signal received!"))
        self.button.clicked.connect(self.show_message)
        self.line_edit.textChanged.connect(self.my_object.trigger_signal)

        # Menu and Toolbar
        self.menu_bar = QMenuBar()
        file_menu = QMenu("File", self)
        open_action = QAction("Open", self)
        exit_action = QAction("Exit", self)
        file_menu.addAction(open_action)
        file_menu.addAction(exit_action)
        self.menu_bar.addMenu(file_menu)
        self.setMenuBar(self.menu_bar)

        self.toolbar = QToolBar("Main Toolbar")
        save_action = QAction("Save", self)
        self.toolbar.addAction(save_action)
        self.addToolBar(self.toolbar)

        exit_action.triggered.connect(self.close)  # Close Application

        # Tabs
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab1_layout = QVBoxLayout()
        self.tab2_layout = QVBoxLayout()
        self.tab1_label = QLabel("This is Tab 1")
        self.tab2_label = QLabel("This is Tab 2")
        self.tab1_layout.addWidget(self.tab1_label)
        self.tab2_layout.addWidget(self.tab2_label)
        self.tab1.setLayout(self.tab1_layout)
        self.tab2.setLayout(self.tab2_layout)
        self.tabs.addTab(self.tab1, "Tab 1")
        self.tabs.addTab(self.tab2, "Tab 2")
        main_layout.addWidget(self.tabs)

    def show_message(self):  # Dialogs
        QMessageBox.information(self, "Message", "Button Clicked!")

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, "Close", "Are you sure you want to exit?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()