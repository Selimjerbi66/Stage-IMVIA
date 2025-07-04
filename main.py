# main.py

import sys
from PyQt6.QtWidgets import QApplication
from interface.main_interface import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)  # Basic Setup
    window = MainWindow()  # Basic Setup
    window.show()  # Basic Setup
    sys.exit(app.exec())  # Basic Setup