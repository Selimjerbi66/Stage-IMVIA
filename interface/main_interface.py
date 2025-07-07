from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QTabWidget, QTextEdit)
class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Réseau de cameras de surveillance")  # Basic Structure
        self.setGeometry(100, 100, 600, 400)  # Basic Structure

        self.tab_widget = QTabWidget()  # Tabs Structure
        layout = QVBoxLayout(self)  # Layouts
        layout.addWidget(self.tab_widget)  # Add tabs to layout
        
        self.tab1 = QWidget()  # Tabs Structure
        self.tab2 = QWidget()  # Tabs Structure
        