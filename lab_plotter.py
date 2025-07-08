import matplotlib.pyplot as plt  # Importer la bibliothèque pyplot de matplotlib pour la visualisation
import matplotlib.patches as patches
import numpy as np  # Importer numpy pour la manipulation de tableaux numériques
from lab_builder import *
from mathematical.camfield import *
hex_codes = [
    '#000000',  # Black (lowest intensity)
    '#0000FF',  # Blue
    '#00FFFF',  # Cyan
    '#00FF00',  # Green
    '#FFFF00',  # Yellow
    '#FFD700',  # Gold (high intensity)
    '#FFA500',  # Orange
    '#FF0000',  # Red (high intensity)
    '#FF00FF',  # Magenta
    '#FF1493',  # Deep Pink (high intensity)
    '#FF4500',  # Orange Red (high intensity)
    '#800080'   # Purple
]
json_file_path = "labo.json"  # Replace with your JSON file path
result = process_room_file(json_file_path)
room = setUpLab(result)
fig, ax = plt.subplots(figsize=(room.length,room.width))  # Width: 10 inches, Height: 6 inches
for i in range(len(room.walls)):
    print(room.walls[i])
    # Create a rectangle patch
    rectangle = patches.Rectangle(
        (room.walls[i].xbl, room.walls[i].ybl),     # Bottom-left corner coordinates
        room.walls[i].length,         # Length of the rectangle
        room.walls[i].width,          # Width of the rectangle
        linewidth=1,    # Thickness of the rectangle's edge
        edgecolor=hex_codes[0],  # Color of the rectangle's edge (red)
        facecolor=hex_codes[0]  # No fill color for the rectangle
    )

    # Add the rectangle patch to the axes
    ax.add_patch(rectangle)
cameras = setUpCameras(process_cameras_file("cameraexp.json"), room)
# Loop through each point in the matrix
for i , camera in enumerate(cameras):
    points=outlineView(room.visible_points_by_camera(camera))
    print(i)
    print(points)
    if points:
    # Create a polygon from the points
        polygon = patches.Polygon(points, closed=True, facecolor=hex_codes[2], edgecolor=hex_codes[3], linewidth=1)
    
    # Add the polygon to your plot (assuming you have an `ax` defined)
        ax.add_patch(polygon)

# Set limits for the x-axis and y-axis
ax.set_xlim(-1, room.length + 1)  # X-axis limits
ax.set_ylim(-1, room.width + 1)# Y-axis limits

# Add labels and titles
ax.set_xlabel('X-axis')  # X-axis label
ax.set_ylabel('Y-axis')  # Y-axis label
ax.set_title(room.name) # Title of the plot
# Show grid
#plt.grid()

# Display the plot
plt.show()
