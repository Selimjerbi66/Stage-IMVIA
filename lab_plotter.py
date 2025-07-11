from lab_builder import *


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
cameras = setUpCameras(process_cameras_file("surveillance.json"), room)
# Loop through each point in the matrix

viewable=room.point_matrix(cameras)
for point, data in viewable.items():
    x, y = point  # Unpack the tuple (x, y)
    n = len(data['cameras'])  # Number of cameras linked to the point
        
        # Use modulo to cycle through hex_codes if there are more cameras than colors
    color = hex_codes[n % len(hex_codes)]  
        
        # Scatter the point with its respective color
    ax.scatter(x, y, color=color, s=1)


for camera in cameras:
    ax.scatter(camera.x, camera.y, color='red', s=10) # Smallest marker size
    ax.text(camera.x, camera.y, camera.name, fontsize=10)

'''
for i in cameras:
    to_view = room.visible_points_by_camera(i)
    for p in to_view:
        print(p)
        ax.scatter(p[0], p[1], color='#FFD700')
'''


# Set limits for the x-axis and y-axis
ax.set_xlim(-1, room.length + 1)  # X-axis limits
ax.set_ylim(-1, room.width + 1)    # Y-axis limits

# Add labels and titles
ax.set_xlabel('X-axis')  # X-axis label
ax.set_ylabel('Y-axis')  # Y-axis label
ax.set_title(room.name)   # Title of the plot

# Show grid if needed
# plt.grid()

# Display the plot
plt.show()
