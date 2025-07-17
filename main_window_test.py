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
        self.tab_network = self.setup_tab_network()  # Just added
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
        room_charge.clicked.connect(self.roomCharge)  # Corrected
        camera_charge = QPushButton("❎ Load Cameras")
        camera_charge.clicked.connect(self.cameraCharge)  # Corrected

        layout.addWidget(room_charge)
        layout.addWidget(camera_charge)

        # Generate Point Matrix button
        generate_matrix = QPushButton("📊 Generate Point Matrix")
        generate_matrix.clicked.connect(self.generatePointMatrix)  # Corrected
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
        self.connectivity_distance_input.setPlaceholderText("exp : 200")  # Just added
        layout.addWidget(QLabel("Maximum Connectivity Distance"))  # Just added
        layout.addWidget(self.connectivity_distance_input)  # Just added

        # Input for obstacle interference
        self.obstacle_interference_input = QLineEdit()
        self.obstacle_interference_input.setPlaceholderText("exp : 10")  # Just added
        layout.addWidget(QLabel("Obstacle Interference (%)"))  # Just added
        layout.addWidget(self.obstacle_interference_input)  # Just added

        # Button for connectivity check
        connectivity_check_button = QPushButton("Connectivity Check")  # Just added
        connectivity_check_button.clicked.connect(self.checkConnectivity)  # Just added
        layout.addWidget(connectivity_check_button)  # Just added

        # List to display networks
        self.network_list = QListWidget()  # Just added
        self.network_list.itemClicked.connect(self.showNetworkData)  # Just added
        layout.addWidget(self.network_list)  # Just added

        w = QWidget()
        w.setLayout(layout)
        return w

    # Just added: Function to check connectivity
    def checkConnectivity(self):
        try:
            # Retrieve inputs
            max_distance = int(self.connectivity_distance_input.text())  # Just added
            obstacle_interference = int(self.obstacle_interference_input.text())  # Just added

            # Call ConnectedCams function
            self.networks, self.camera_coordinates = ConnectedCams(self.room, self.cameras, max_distance, obstacle_interference)  # Just added

            # Populate the network list
            self.network_list.clear()  # Just added
            for i, network in enumerate(self.networks):
                self.network_list.addItem(f"Network {i + 1}")  # Just added
            
            self.console.append("Connectivity check completed.")  # Just added

        except Exception as e:
            self.console.append(f"Error during connectivity check: {e}")  # Just added

    # Just added: Function to show network data
    def showNetworkData(self, item):
        network_index = self.network_list.row(item)  # Get the index of the clicked network
        network = self.networks[network_index]  # Get the cameras in this network

        camera_info = []  # Just added: Initialize a list to store camera info
        for cam in network:
            if cam in self.camera_coordinates:  # Just added: Check if the camera exists in the coordinates
                camera_info.append(f"{cam}: {self.camera_coordinates[cam]}")  # Just added

        if camera_info:
            self.console.append(f"Network {network_index + 1} Cameras: {', '.join(camera_info)}")  # Just added
        else:
            self.console.append(f"No cameras found in Network {network_index + 1}.")  # Just added

    def showZoneData(self, item):
        zone_name = item.text()  # Get the text of the clicked item
        if zone_name in self.data:
            visibility_rate = self.data[zone_name] * 100  # Convert to percentage
        
            if visibility_rate < 80:
                self.console.append(f"{zone_name}: {visibility_rate:.2f}% - Zone cannot be considered visible.")
            else:
                self.console.append(f"{zone_name}: {visibility_rate:.2f}% - Zone is visible.")
        else:
            self.console.append(f"No data found for {zone_name}.")

    def roomCharge(self):
        # Open file dialog to load a room file
        self.json_lab_path, _ = QFileDialog.getOpenFileName(self, "Charger un bâtiment", "", "JSON Files (*.json);;All Files (*)")
        if self.json_lab_path:
            self.console.append("Room loaded from: " + self.json_lab_path)

    def cameraCharge(self):
        # Open file dialog to load a camera file
        self.json_cam_path, _ = QFileDialog.getOpenFileName(self, "Charger un réseau de caméras", "", "JSON Files (*.json);;All Files (*)")
        if self.json_cam_path:
            self.console.append("Camera network loaded from: " + self.json_cam_path)

    def generatePointMatrix(self):
        # Generate room and cameras
        try:
            self.room = setUpLab(process_room_file(self.json_lab_path))
            self.cameras = setUpCameras(process_cameras_file(self.json_cam_path), self.room)
            self.viewable = self.room.point_matrix(self.cameras)
            self.console.append("Point matrix generated.")
        
            # Use the zones from the room
            zones = self.room.zones
            self.data = zoneViewer(zones, self.viewable)  # Create self.data

            # Populate the zone list in the zones tab
            self.zone_list.clear()  # Clear previous entries
            self.zone_list.addItems(self.data.keys())  # Add new zone names

            self.console.append(f"Visibility data stored in self.data: {self.data}")
        
        except Exception as e:
            self.console.append(f"Error generating point matrix: {e}")

    def selectPoint(self):
        input_text = self.ip_input.text()
        # Validate input format
        if not (input_text.startswith("(") and input_text.endswith(")")):
            self.console.append("Error: Input must be in the format (x,y).")
            return

        try:
            # Extract x and y values
            x_str, y_str = input_text[1:-1].split(",")
            x, y = int(x_str), int(y_str)

            # Create tuple and check in viewable
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
        # Call the plotLab function with room, cameras, and viewable
        plotLab(self.room, self.cameras, self.viewable)