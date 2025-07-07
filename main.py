# main.py

import sys
from PyQt6.QtWidgets import QApplication, QMessageBox
from interface.main_interface import *  # Importing MyApp from interface.py

if __name__ == '__main__':
    app = QApplication(sys.argv)  # Basic Structure
    window = MyApp()  # Initialize the app
    window.show()  # Show the main window
    sys.exit(app.exec())  # Running the Application