from PyQt6.QtWidgets import QApplication
import sys
from main_window_test import MainWindow

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
