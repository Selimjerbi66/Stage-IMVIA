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
cameras = setUpCameras(process_cameras_file("cameraexp.json"), room)
# Loop through each point in the matrix
camView = room.check_alignments(cameras)
'''
for i in cameras:
    to_view = room.visible_points_by_camera(i)
    for p in to_view:
        ax.scatter(p[0], p[1], color='#FFD700')
'''
print(camView)

for camera_name, points in camView:
    # Find the camera's coordinates
    camera = next((cam for cam in cameras if cam.name == camera_name), None)
    if camera is None or not points:  # Check for None or empty points
        continue
    
    print('length', len(points))
    
    vision = ViewField(camera, points)
    
    # Draw lines from camera to each point
    ax.fill(vision.drawx(), vision.drawy(),color=hex_codes[4], edgecolor=hex_codes[4])  # Call drawy() correctly
    ax.scatter(*vision.cam(), color='red', label=vision.camera_name)  # Mark the camera position
    ax.text(camera.x, camera.y, camera.name, fontsize=9, ha='right')

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
