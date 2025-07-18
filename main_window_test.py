from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTabWidget,
    QPushButton, QTextEdit, QLabel, QFileDialog, QLineEdit, QListWidget
)
from PyQt6.QtCore import Qt
from lab_plotting import *  # Ensure this module contains necessary functions and classes
from connectivity import *  # Ensure this imports ConnectedCams

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulation de caméras de surveillance")
        self.setMinimumSize(600, 900)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        self.tabs = QTabWidget()

        # Tabs
        self.tab_menu = self.setup_tab_menu()
        self.tab_view = self.setup_tab_view()
        self.tab_zones = self.setup_tab_zones()  # New tab for zones
        self.tabs.addTab(self.tab_menu, "🏁 Menu")
        self.tabs.addTab(self.tab_view, "👁️ View")
        self.tabs.addTab(self.tab_zones, "🗺️ Zones")  # Add the new tab
        self.tab_network = self.setup_tab_network()  # Added network tab
        self.tabs.addTab(self.tab_network, "🌐 Network")

        layout.addWidget(self.tabs)

        # Global execution console
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setPlaceholderText("📜 Execution Console")
        layout.addWidget(self.console)

        self.setLayout(layout)

    def setup_tab_menu(self):
        layout = QVBoxLayout()
        ip_label = QLabel("🔗 Camera Network Simulator inside a Building")
        layout.addWidget(ip_label)

        # Buttons to load files
        room_charge = QPushButton("🔌 Load Building")
        room_charge.clicked.connect(self.roomCharge)
        camera_charge = QPushButton("❎ Load Cameras")
        camera_charge.clicked.connect(self.cameraCharge)

        layout.addWidget(room_charge)
        layout.addWidget(camera_charge)

        # Generate Point Matrix button
        generate_matrix = QPushButton("📊 Generate Point Matrix")
        generate_matrix.clicked.connect(self.generatePointMatrix)
        layout.addWidget(generate_matrix)

        w = QWidget()
        w.setLayout(layout)
        return w

    def setup_tab_view(self):
        layout = QVBoxLayout()

        # Button to plot the lab
        plot_lab_button = QPushButton("📈 Plot Lab")
        plot_lab_button.clicked.connect(self.plotLab)
        layout.addWidget(plot_lab_button)

        # Input for point selection
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("ex : (x,y)")
        layout.addWidget(self.ip_input)

        # Button to select point
        select_point = QPushButton("Select Point")
        select_point.clicked.connect(self.selectPoint)
        layout.addWidget(select_point)

        w = QWidget()
        w.setLayout(layout)
        return w

    def setup_tab_zones(self):
        layout = QVBoxLayout()
        
        self.zone_list = QListWidget()  # List widget to display zone names
        self.zone_list.itemClicked.connect(self.showZoneData)  # Connect click event
        layout.addWidget(self.zone_list)

        w = QWidget()
        w.setLayout(layout)
        return w

    def setup_tab_network(self):
        layout = QVBoxLayout()

        # Input for maximum connectivity distance
        self.connectivity_distance_input = QLineEdit()
        self.connectivity_distance_input.setPlaceholderText("exp : 200")
        layout.addWidget(QLabel("Maximum Connectivity Distance"))
        layout.addWidget(self.connectivity_distance_input)

        # Input for obstacle interference
        self.obstacle_interference_input = QLineEdit()
        self.obstacle_interference_input.setPlaceholderText("exp : 10")
        layout.addWidget(QLabel("Obstacle Interference (%)"))
        layout.addWidget(self.obstacle_interference_input)

        # Button for connectivity check
        connectivity_check_button = QPushButton("Connectivity Check")
        connectivity_check_button.clicked.connect(self.checkConnectivity)
        layout.addWidget(connectivity_check_button)

        # List to display networks
        self.network_list = QListWidget()
        self.network_list.itemClicked.connect(self.showNetworkData)
        layout.addWidget(self.network_list)

        # Button to plot connectivity
        plot_connectivity_button = QPushButton("Plot Connectivity")
        plot_connectivity_button.clicked.connect(self.plotConnectivity)
        layout.addWidget(plot_connectivity_button)

        w = QWidget()
        w.setLayout(layout)
        return w

    def checkConnectivity(self):
        try:
            # Retrieve inputs
            max_distance = int(self.connectivity_distance_input.text())
            obstacle_interference = int(self.obstacle_interference_input.text())

            # Call ConnectedCams function
            self.networks, self.camera_coordinates, self.camera_proxi = ConnectedCams(
                self.room, self.cameras, max_distance, obstacle_interference)

            # Populate the network list
            self.network_list.clear()
            for i, network in enumerate(self.networks):
                self.network_list.addItem(f"Network {i + 1}")

            self.console.append("Connectivity check completed.")

        except ValueError:
            self.console.append("Error: Please enter valid integers for distance and interference.")
        except Exception as e:
            self.console.append(f"Error during connectivity check: {e}")

    def showNetworkData(self, item):
        network_index = self.network_list.row(item)
        network = self.networks[network_index]

        camera_info = []
        for cam in network:
            if cam in self.camera_coordinates:
                camera_info.append(f"{cam}: {self.camera_coordinates[cam]}")

        if camera_info:
            self.console.append(f"Network {network_index + 1} Cameras: {', '.join(camera_info)}")
        else:
            self.console.append(f"No cameras found in Network {network_index + 1}.")

    def showZoneData(self, item):
        zone_name = item.text()
        if zone_name in self.data:
            visibility_rate = self.data[zone_name] * 100
        
            if visibility_rate < 80:
                self.console.append(f"{zone_name}: {visibility_rate:.2f}% - Zone cannot be considered visible.")
            else:
                self.console.append(f"{zone_name}: {visibility_rate:.2f}% - Zone is visible.")
        else:
            self.console.append(f"No data found for {zone_name}.")

    def roomCharge(self):
        try:
            self.json_lab_path, _ = QFileDialog.getOpenFileName(self, "Charger un bâtiment", "", "JSON Files (*.json);;All Files (*)")
            if self.json_lab_path:
                self.console.append("Room loaded from: " + self.json_lab_path)
        except Exception as e:
            self.console.append(f"Error loading building: {e}")

    def cameraCharge(self):
        try:
            self.json_cam_path, _ = QFileDialog.getOpenFileName(self, "Charger un réseau de caméras", "", "JSON Files (*.json);;All Files (*)")
            if self.json_cam_path:
                self.console.append("Camera network loaded from: " + self.json_cam_path)
        except Exception as e:
            self.console.append(f"Error loading camera network: {e}")

    def generatePointMatrix(self):
        try:
            self.room = setUpLab(process_room_file(self.json_lab_path))
            self.cameras = setUpCameras(process_cameras_file(self.json_cam_path), self.room)
            self.viewable = self.room.point_matrix(self.cameras)
            self.console.append("Point matrix generated.")
        
            zones = self.room.zones
            self.data = zoneViewer(zones, self.viewable)

            self.zone_list.clear()
            self.zone_list.addItems(self.data.keys())

            self.console.append(f"Visibility data stored in self.data: {self.data}")
        
        except Exception as e:
            self.console.append(f"Error generating point matrix: {e}")

    def selectPoint(self):
        input_text = self.ip_input.text()
        if not (input_text.startswith("(") and input_text.endswith(")")):
            self.console.append("Error: Input must be in the format (x,y).")
            return

        try:
            x_str, y_str = input_text[1:-1].split(",")
            x, y = int(x_str), int(y_str)

            point = (x, y)
            if point in self.viewable:
                self.console.append(f"Point {point} data: {self.viewable[point]}")
            else:
                self.console.append(f"Point {point} is not in the viewable matrix.")
        except ValueError:
            self.console.append("Error: x and y must be integers.")
        except Exception as e:
            self.console.append(f"Unexpected error: {e}")

    def plotLab(self):
        try:
            plotLab(self.room, self.cameras, self.viewable)
        except Exception as e:
            self.console.append(f"Error plotting lab: {e}")

    def plotConnectivity(self):
        try:
            # Call the plotConnectivity function with the room, camera points, and camera proxi
            plotConnectivity(self.room, self.camera_coordinates, self.camera_proxi)
        except Exception as e:
            self.console.append(f"Error plotting connectivity: {e}")