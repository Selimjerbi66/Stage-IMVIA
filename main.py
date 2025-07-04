# main.py

import sys
from PyQt6.QtWidgets import QApplication
from interface.main_interface import MainWindow  # Importing the MainWindow class

if __name__ == '__main__':
    app = QApplication(sys.argv)  # Create QApplication
    window = MainWindow()  # Initialize MainWindow
    window.show()  # Show the main window
    sys.exit(app.exec())  # Start the event loop