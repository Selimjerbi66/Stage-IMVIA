import sys  # Basic Setup
from PyQt6.QtWidgets import (  # Basic Setup
    QApplication, QMainWindow, QWidget, QLabel, QPushButton,  # Common Widgets
    QLineEdit, QTextEdit, QCheckBox, QRadioButton, QComboBox,  # Common Widgets
    QVBoxLayout, QHBoxLayout, QGridLayout,  # Layouts
    QMenuBar, QMenu, QToolBar, QMessageBox, QFileDialog,  # Menus and Toolbars, Dialogs
    QTabWidget  # Creating a Tabbed Interface
)
from PyQt6.QtCore import pyqtSignal, QObject  # Signals and Slots
from PyQt6.QtGui import QAction  # Menus and Toolbars

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Implémentation d'un outil de simulation et d'évaluation de la couverture dans un réseau de capteurs visuels")
        self.resize(800, 600)

        
