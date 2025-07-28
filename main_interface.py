from PyQt6.QtWidgets import QApplication
from main_window import MainWindow


def interface(sys):
    app = QApplication(sys.argv)
    window = MainWindow(app)  # Assuming MainWindow is defined elsewhere in your code
    window.show()
    app.exec()