import matplotlib.pyplot as plt
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTabWidget,
    QPushButton, QTextEdit, QLabel, QFileDialog, QLineEdit, QListWidget, QHBoxLayout
)
from PyQt6.QtGui import QPixmap  # Import QPixmap
from PyQt6.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from lab_plotting import *  # Ensure this module contains necessary functions and classes
from connectivity import *  # Ensure this imports ConnectedCams
from briefing import *


class PlotWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)

        # Label to display cursor coordinates
        self.cursor_label = QLabel("Cursor Position: ")

        # Layout setup
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.cursor_label)  # Add the label to the layout

        # Create button layouts
        button_layout1 = QHBoxLayout()
        self.btn_up = QPushButton("Up")
        self.btn_down = QPushButton("Down")
        self.btn_left = QPushButton("Left")
        self.btn_right = QPushButton("Right")

        # Connect buttons to their functions
        self.btn_up.clicked.connect(lambda: self.pan(0, 10))  # Move up
        self.btn_down.clicked.connect(lambda: self.pan(0, -10))  # Move down
        self.btn_left.clicked.connect(lambda: self.pan(-10, 0))  # Move left
        self.btn_right.clicked.connect(lambda: self.pan(10, 0))  # Move right

        # Add first row of buttons
        button_layout1.addWidget(self.btn_up)
        button_layout1.addWidget(self.btn_down)
        button_layout1.addWidget(self.btn_left)
        button_layout1.addWidget(self.btn_right)

        # Create second row of buttons
        button_layout2 = QHBoxLayout()
        self.btn_zoom_in = QPushButton("Zoom In")
        self.btn_zoom_out = QPushButton("Zoom Out")

        # Connect second row buttons to their functions
        self.btn_zoom_in.clicked.connect(self.zoom_in)
        self.btn_zoom_out.clicked.connect(self.zoom_out)

        # Add second row of buttons
        button_layout2.addWidget(self.btn_zoom_in)
        button_layout2.addWidget(self.btn_zoom_out)

        # Add button layouts to the main layout
        layout.addLayout(button_layout1)  # First row of buttons
        layout.addLayout(button_layout2)  # Second row of buttons
        self.setLayout(layout)

        # Initial limits for the plot
        self.original_xlim = None
        self.original_ylim = None

        # Connect the motion event
        self.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)

    def plot(self, x, y, title, xlabel, ylabel):
        self.ax.clear()
        self.ax.plot(x, y)
        self.ax.set_title(title)
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)
        self.canvas.draw()

        # Extract original limits after plotting
        self.original_xlim = self.ax.get_xlim()
        self.original_ylim = self.ax.get_ylim()

    def on_mouse_move(self, event):
        """Update cursor label with current coordinates."""
        if event.inaxes:  # Check if the mouse is within the axes
            x, y = event.xdata, event.ydata  # Get the coordinates
            self.cursor_label.setText(f"Cursor Position: ({x:.2f}, {y:.2f})")

    def zoom_in(self):
        """Zoom in on the plot."""
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        self.ax.set_xlim([xlim[0] * 0.9, xlim[1] * 0.9])
        self.ax.set_ylim([ylim[0] * 0.9, ylim[1] * 0.9])
        self.canvas.draw()

    def zoom_out(self):
        """Zoom out on the plot."""
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        self.ax.set_xlim([xlim[0] * 1.1, xlim[1] * 1.1])
        self.ax.set_ylim([ylim[0] * 1.1, ylim[1] * 1.1])
        self.canvas.draw()

    def pan(self, dx, dy):
        """Pan the plot in the specified direction."""
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        self.ax.set_xlim([xlim[0] + dx, xlim[1] + dx])
        self.ax.set_ylim([ylim[0] + dy, ylim[1] + dy])
        self.canvas.draw()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulation de caméras de surveillance")
        self.setMinimumSize(600, 900)
        self.setWindowIcon(QIcon("cctv_1061924.png"))
        self.current_rate = 80  # Initialize the default rate
        self.max_distance = 250
        self.obstacle_interference=10
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        self.tabs = QTabWidget()

        # Tabs
        self.tab_menu = self.setup_tab_menu()
        self.tab_view = self.setup_tab_view()
        self.tab_zones = self.setup_tab_zones()
        self.tab_network = self.setup_tab_network()
        self.tab_brief = self.setup_tab_brief()  # New Brief tab

        self.tabs.addTab(self.tab_menu, "🏁 Menu")
        self.tabs.addTab(self.tab_view, "👁️ View")
        self.tabs.addTab(self.tab_zones, "🗺️ Zones")
        self.tabs.addTab(self.tab_network, "🌐 Network")
        self.tabs.addTab(self.tab_brief, "🌐 Brief")

        layout.addWidget(self.tabs)

        # Global execution console
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setPlaceholderText("📜 Execution Console")
        layout.addWidget(self.console)

        self.setLayout(layout)

    def setup_tab_menu(self):
        layout = QVBoxLayout()


        ip_label = QLabel("🔗 Camera Network Simulator")
        layout.addWidget(ip_label)

        # Add the first image
        image_label_1 = QLabel()
        pixmap1 = QPixmap("logo-imvia.png")  # Path to the first image
        image_label_1.setPixmap(pixmap1)
        image_label_1.setScaledContents(True)
        image_label_1.setFixedSize(412, 100)  # Set size as needed

        layout.addWidget(image_label_1)

        # Add the second image
        image_label_2 = QLabel()
        pixmap2 = QPixmap("Polytech_DIJON.png")  # Path to the second image
        image_label_2.setPixmap(pixmap2)
        image_label_2.setScaledContents(True)
        image_label_2.setFixedSize(321, 100)  # Set size as needed
        layout.addWidget(image_label_2)

        # Combine text into a single QLabel with HTML line breaks
        combined_text = (
        "Realized by: Selim Jerbi<br>"
        "Under the tutelage of: Wahabou Abdou<br>"
        "Project made at IMVIA<br>"
        "As an internship for Polytech Dijon<br>"
        "07/2025"
    )
        text_label = QLabel(combined_text)
        text_label.setOpenExternalLinks(True)  # Enable HTML rendering
        layout.addWidget(text_label)

        

        # Buttons to load files
        room_charge = QPushButton("🏢 Load Building")
        room_charge.clicked.connect(self.roomCharge)
        camera_charge = QPushButton("📷 Load Cameras")
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
        self.ip_input.setPlaceholderText("ex : x y")
        layout.addWidget(self.ip_input)

        # Button to select point
        select_point = QPushButton("📍 Select Point")
        select_point.clicked.connect(self.selectPoint)
        layout.addWidget(select_point)

        # Create the plot widget and add it to the layout
        self.plot_widget = PlotWidget()
        layout.addWidget(self.plot_widget)

        # Add this in the setup_tab_view method
        save_plot_button = QPushButton("💾 Save Plot")
        save_plot_button.clicked.connect(self.savePlot)
        layout.addWidget(save_plot_button)

        w = QWidget()
        w.setLayout(layout)
        return w

    def setup_tab_zones(self):
        layout = QVBoxLayout()
        
        self.zone_list = QListWidget()  # List widget to display zone names
        self.zone_list.itemClicked.connect(self.showZoneData)  # Connect click event
        layout.addWidget(self.zone_list)

        # Input for the rate
        self.rate_input = QLineEdit()
        self.rate_input.setPlaceholderText("Enter rate (0-100)")
        layout.addWidget(self.rate_input)

        # Button to apply the rate
        apply_rate_button = QPushButton("✅ Apply Rate")
        apply_rate_button.clicked.connect(self.applyRate)
        layout.addWidget(apply_rate_button)

        self.zoner = QTextEdit()
        self.zoner.setReadOnly(True)
        self.zoner.setPlaceholderText("📜 Zone Data Lister")
        layout.addWidget(self.zoner)

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

        # Button for Connectivity Network
        connectivity_network_button = QPushButton("🌐 Connectivity Network")
        connectivity_network_button.clicked.connect(self.connectivityNetwork)
        layout.addWidget(connectivity_network_button)

        # List to display networks
        self.network_list = QListWidget()
        self.network_list.itemClicked.connect(self.showNetworkData)
        layout.addWidget(self.network_list)

        # Create the plot network widget and add it to the layout
        self.plot_network_widget = PlotWidget()
        layout.addWidget(self.plot_network_widget)

        # Save network plot button
        save_network_plot_button = QPushButton("💾 Save Network Plot")
        save_network_plot_button.clicked.connect(self.saveNetworkPlot)
        layout.addWidget(save_network_plot_button)

        w = QWidget()
        w.setLayout(layout)
        return w

    def setup_tab_brief(self):
        """Setup the Brief tab with a button and result display."""
        layout = QVBoxLayout()

        brief_start_button = QPushButton("🔍 Brief Start")
        brief_start_button.clicked.connect(self.show_brief_results)  # Connect to the result function
        layout.addWidget(brief_start_button)

        # Result labels to display the results
        self.results_labels = [QLabel() for _ in range(4)]
        for label in self.results_labels:
            layout.addWidget(label)

        w = QWidget()
        w.setLayout(layout)
        return w

    def show_brief_results(self):
        """Calculate and display the results using the imported functions."""
        try:
            total_points = self.room.points  # Assuming self.room has a points attribute
        except Exception as e:
            self.results_labels[0].setText(f"Error in total points: {e}")
        else:
            try:
                points = list(self.viewable.keys())  # Assuming self.viewable is a dict
                coverage = visual_coverage(total_points, points)
                self.results_labels[0].setText(f"Visual Coverage: {coverage:.2f}%")
            except Exception as e:
                self.results_labels[0].setText(f"Error calculating coverage: {e}")

        try:
            redundancy_values = list(self.viewable.values())  # Assuming self.viewable.values() is a list
            red = redundancy(redundancy_values)
            self.results_labels[1].setText(f"Redundancy: {red:.2f}%")
        except Exception as e:
            self.results_labels[1].setText(f"Error calculating redundancy: {e}")

        try:
            zone_avg = zonepercent(self.data.values())
            self.results_labels[2].setText(f"Zone Average: {zone_avg:.2f}%")
        except Exception as e:
            self.results_labels[2].setText(f"Error calculating zone average: {e}")

        try:
            network_count = networks_number(self.networks)  # Assuming self.networks is a list
            self.results_labels[3].setText(f"Number of Networks: {network_count}")
        except Exception as e:
            self.results_labels[3].setText(f"Error counting networks: {e}")

    def devConnectivity(self):
        """Calculate connectivity and set instance variables."""
        try:
            # Retrieve inputs and assign to instance variables with defaults
            self.max_distance = int(self.connectivity_distance_input.text()) if self.connectivity_distance_input.text() else 250
            self.obstacle_interference = int(self.obstacle_interference_input.text()) if self.obstacle_interference_input.text() else 10

            # Call ConnectedCams function
            self.networks, self.camera_coordinates, self.camera_proxi = ConnectedCams(
                self.room, self.cameras, self.max_distance, self.obstacle_interference)

            self.console.append("Connectivity calculation completed.")

        except ValueError:
            self.console.append("Error: Please enter valid integers for distance and interference.")
        except Exception as e:
            self.console.append(f"Error during connectivity calculation: {e}")

    def checkConnectivity(self):
        """Calculate connectivity and populate the network list with the current connectivity data."""
        try:
            # Retrieve inputs and assign to instance variables with defaults
            self.max_distance = int(self.connectivity_distance_input.text()) if self.connectivity_distance_input.text() else 250
            self.obstacle_interference = int(self.obstacle_interference_input.text()) if self.obstacle_interference_input.text() else 10

            # Call ConnectedCams function
            self.networks, self.camera_coordinates, self.camera_proxi = ConnectedCams(
                self.room, self.cameras, self.max_distance, self.obstacle_interference)

            self.console.append("Connectivity calculation completed.")

            # Populate the network list with the current connectivity data
            self.network_list.clear()
            for i, _ in enumerate(self.networks):
                self.network_list.addItem(f"Network {i + 1}")

            self.console.append("Network list populated.")

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

    def applyRate(self):
        input_rate = self.rate_input.text().strip()  # Get input and strip whitespace
        default_rate = 80  # Default rate

        if not input_rate:  # If input is empty, use default rate
            self.zoner.append("Invalid input: please enter a number.")
        else:
            try:
                rate = float(input_rate)  # Convert to float
                if 0 <= rate <= 100:  # Check if the rate is between 0 and 100
                    self.current_rate = rate
                else:
                    self.zoner.append("Rate must be between 0 and 100")
                    return
            except ValueError:
                self.zoner.append("Invalid input: please enter a number.")
                return
        if input_rate:
            self.zoner.append(f"Rate applied: {self.current_rate}")

    def showZoneData(self, item):
        zone_name = item.text()
        if zone_name in self.data:
            visibility_rate = self.data[zone_name] * 100
        
            if visibility_rate < self.current_rate:
                self.zoner.append(f"{zone_name}: {visibility_rate:.2f}% - Zone cannot be considered visible.")
            else:
                self.zoner.append(f"{zone_name}: {visibility_rate:.2f}% - Zone is visible.")
        else:
            self.zoner.append(f"No data found for {zone_name}.")

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
            
            # Generate the point matrix
            self.room = setUpLab(process_room_file(self.json_lab_path))
            self.cameras = setUpCameras(process_cameras_file(self.json_cam_path), self.room)
            self.viewable = self.room.point_matrix(self.cameras)
            self.console.append("Point matrix generated.")

            zones = self.room.zones
            self.data = zoneViewer(zones, self.viewable)

            self.zone_list.clear()
            self.zone_list.addItems(self.data.keys())

            self.console.append(f"Visibility data stored in self.data: {self.data}")

            # Now, calculate connectivity
            self.devConnectivity()  # Call to update networks and camera data


        except Exception as e:
            self.console.append(f"Error generating point matrix: {e}")

    def selectPoint(self):
        input_text = self.ip_input.text().strip()  # Strip leading/trailing whitespace
        if ' ' not in input_text:
            self.console.append("Error: Input must be in the format 'x y'.")
            return

        try:
            x_str, y_str = input_text.split()
        
            # Convert to integers
            x, y = int(x_str), int(y_str)

            point = (x, y)  # Create the point tuple
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
            self.plot_widget.ax.clear()  # Clear the existing plot
            plotLab(self.room, self.cameras, self.viewable, self.plot_widget.ax)  # Call the imported plotLab function
            self.plot_widget.canvas.draw()  # Refresh the canvas to show the updated plot
            plt.close()  # Close the figure to free resources
        except Exception as e:
            self.console.append(f"Error plotting lab: {e}")

    def plotConnectivity(self):
        try:
            self.plot_network_widget.ax.clear()  # Clear the existing plot
            plotConnectivity(self.room, self.camera_coordinates, self.camera_proxi, self.plot_network_widget.ax)  # Call the imported plotConnectivity function
            self.plot_network_widget.canvas.draw()  # Refresh the canvas to show the updated plot
            plt.close()  # Close the figure to free resources
        except Exception as e:
            self.console.append(f"Error plotting connectivity: {e}")
    def connectivityNetwork(self):
        try:
            # First, perform the connectivity check
            self.checkConnectivity()  # Call the existing method

            # Then, plot the connectivity
            self.plotConnectivity()  # Call the existing method
        except Exception as e:
            self.console.append(f"Error during connectivity check and plotting: {e}")

    def savePlot(self):
        try:
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Plot", "", "PNG Files (*.png);;JPEG Files (*.jpg);;All Files (*)")
            if file_path:
                self.plot_widget.figure.savefig(file_path)  # Save the actual plot
                self.console.append(f"Plot saved to: {file_path}")
        except Exception as e:
            self.console.append(f"Error saving plot: {e}")

    def saveNetworkPlot(self):
        try:
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Network Plot", "", "PNG Files (*.png);;JPEG Files (*.jpg);;All Files (*)")
            if file_path:
                self.plot_network_widget.figure.savefig(file_path)  # Save the actual network plot
                self.console.append(f"Network plot saved to: {file_path}")
        except Exception as e:
            self.console.append(f"Error saving network plot: {e}")