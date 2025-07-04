# main_interface.py

import json
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QPushButton,
    QLineEdit, QTextEdit, QVBoxLayout, QHBoxLayout,
    QTabWidget, QMessageBox, QFileDialog
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Implémentation d'un outil de simulation et d'évaluation de la couverture dans un réseau de capteurs visuels")
        self.resize(800, 600)

        # Central Widget and Layout
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        # Create Tabs
        self.tabs = QTabWidget()
        self.first_tab = self.create_first_tab()
        self.second_tab = self.create_second_tab()

        self.tabs.addTab(self.first_tab, "Simulation")
        self.tabs.addTab(self.second_tab, "Results")
        main_layout.addWidget(self.tabs)

    def create_first_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        # Project Title
        title_label = QLabel("Implémentation d'un outil de simulation et d'évaluation de la couverture dans un réseau de capteurs visuels")
        layout.addWidget(title_label)

        # Button to select lab
        self.select_button = QPushButton("Select a Lab (.json)")
        self.select_button.clicked.connect(self.select_file)
        layout.addWidget(self.select_button)

        # Comments area
        self.comments_area = QTextEdit()
        self.comments_area.setReadOnly(True)
        layout.addWidget(self.comments_area)

        # Button to simulate the lab
        self.simulate_button = QPushButton("Simulate the Lab")
        self.simulate_button.clicked.connect(self.simulate_lab)
        self.simulate_button.setEnabled(False)  # Initially disabled
        layout.addWidget(self.simulate_button)

        tab.setLayout(layout)
        return tab

    def create_second_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.results_area = QTextEdit()
        self.results_area.setReadOnly(True)
        layout.addWidget(self.results_area)

        # Button to navigate the simulation
        navigate_button = QPushButton("Navigate the Simulation")
        navigate_button.clicked.connect(self.show_coming_soon)
        layout.addWidget(navigate_button)

        tab.setLayout(layout)
        return tab

    def select_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select JSON File", "", "JSON Files (*.json);;All Files (*)")
        if file_name:
            self.comments_area.append("File selected: " + file_name)
            self.simulate_button.setEnabled(True)  # Enable the simulate button

    def simulate_lab(self):
        # Simulate the lab - Replace this with your actual simulation logic
        simulated_data = self.simulateLab("path/to/your/file.json")  # Replace with the actual file path
        self.display_results(simulated_data)

    def simulateLab(self, file_path):
        # Mock data for demonstration purposes
        return [
            "wall1 from (50, 100) to (50, 300)",
            "wall2 from (50, 300) to (250, 300)",
            "camera1(position=(100, 150), orientation=0°, angle_of_sight=45°, reach=50)",
            "Room(length=600, width=400, area=240000, walls=3, cameras=1)"
        ]

    def display_results(self, results):
        self.results_area.clear()  # Clear previous results
        for line in results:
            self.results_area.append(line)  # Display each result line

    def show_coming_soon(self):
        QMessageBox.information(self, "Coming Soon", "Feature coming soon!")