# interface.py

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QTabWidget, QTextEdit)

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Complete PyQt6 Example with Tabs")  # Basic Structure
        self.setGeometry(100, 100, 600, 400)  # Basic Structure

        self.tab_widget = QTabWidget()  # Tabs Structure
        layout = QVBoxLayout(self)  # Layouts
        layout.addWidget(self.tab_widget)  # Add tabs to layout

        self.tab1 = QWidget()  # Tabs Structure
        self.tab2 = QWidget()  # Tabs Structure

        self.tab_widget.addTab(self.tab1, "Tab 1")  # Tabs Structure
        self.tab_widget.addTab(self.tab2, "Tab 2")  # Tabs Structure

        self.setup_tab1()  # Setup for Tab 1
        self.setup_tab2()  # Setup for Tab 2

        self.setLayout(layout)  # Layouts
    
    def setup_tab1(self):
        layout = QVBoxLayout()  # Layouts
        self.label = QLabel("Welcome to Tab 1")  # Widgets
        layout.addWidget(self.label)  # Layouts

        self.button = QPushButton("Show Message", self)  # Widgets
        self.button.clicked.connect(self.on_button_click)  # Signals and Slots
        layout.addWidget(self.button)  # Layouts

        # Terminal-like panel using QTextEdit
        self.terminal_panel = QTextEdit(self)  # Widgets
        self.terminal_panel.setReadOnly(True)  # Make it read-only
        layout.addWidget(self.terminal_panel)  # Layouts

        self.tab1.setLayout(layout)  # Layouts

    def setup_tab2(self):
        layout = QVBoxLayout()  # Layouts
        self.label2 = QLabel("This is Tab 2")  # Widgets
        layout.addWidget(self.label2)  # Layouts
        self.tab2.setLayout(layout)  # Layouts

    def on_button_click(self):
        message = "Hello from Tab 1!"  # Create message
        self.terminal_panel.append(message)  # Output to terminal panel