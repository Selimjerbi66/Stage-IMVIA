from lab_builder import *  # Ensure this module contains necessary functions and classes

def plotLab(room, cameras, viewable):
    # Create figure and axis
    _, ax = plt.subplots(figsize=(room.length, room.width))

# Draw zones
    for zone in room.zones:
    # Create a rectangle patch for each zone
        zone_rectangle = patches.Rectangle(
        (zone.blc[0], zone.blc[1]),  # Bottom-left corner coordinates
        zone.length,                 # Length of the rectangle
        zone.width,                  # Width of the rectangle
        linewidth=1,                 # Thickness of the rectangle's edge
        edgecolor=hex_codes[5],      # Edge color for zones
        facecolor=hex_codes[5]       # Fill color for zones
        )
        ax.add_patch(zone_rectangle)
        ax.text(
        zone.blc[0],                  # X position (bottom-left corner)
        zone.blc[1],                  # Y position (bottom-left corner)
        zone.name,                    # Zone name
        ha='left',                    # Horizontal alignment
        va='bottom',                  # Vertical alignment
        color='white'                 # Text color (adjust as needed)
    )

    # Draw the walls of the room using a collection
    wall_rectangles = [patches.Rectangle((wall.xbl, wall.ybl), wall.length, wall.width, linewidth=1, edgecolor=hex_codes[0], facecolor=hex_codes[0]) for wall in room.walls]
    for rectangle in wall_rectangles:
        ax.add_patch(rectangle)

    # Prepare to plot viewable points
    points = []
    colors = []
    sizes = []
    for point, _ in viewable.items():
        x, y = point  # Unpack the point tuple
        n = closeCam(point, viewable, cameras)
        if zoned(room.zones,point):
            color = hex_codes_new[n % len(hex_codes_new)]
        else:
            color = hex_codes[n % len(hex_codes)]  # Use original hex codes

    # You can now use (x, y, color) as needed, e.g., for plotting

        
        
        points.append((x, y))
        colors.append(color)
        sizes.append(1)  # Size for scatter plot

    # Convert to numpy arrays for more efficient plotting
    points = np.array(points)
    
    # Scatter all points in one go
    ax.scatter(points[:, 0], points[:, 1], color=colors, s=sizes)

    # Plot cameras
    camera_positions = [(camera.x, camera.y) for camera in cameras]
    camera_names=[camera.name for camera in cameras]
    ax.scatter(*zip(*camera_positions), color='red', s=10)
    # Add camera names
    for (x, y), name in zip(camera_positions, camera_names):
        ax.text(x, y, name, fontsize=10, ha='center', va='bottom',)

    # Set limits, labels, and title
    ax.set_xlim(-1, room.length + 1)
    ax.set_ylim(-1, room.width + 1)
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_title(room.name)

    # Display the plot
    plt.show()

def plotConnectivity(room, camera_points, camera_proxi):
    # Create figure and axis
    _, ax = plt.subplots(figsize=(room.length, room.width))

    # Draw walls of the room
    wall_rectangles = [patches.Rectangle((wall.xbl, wall.ybl), wall.length, wall.width, linewidth=1, edgecolor='black', facecolor='black') for wall in room.walls]
    for rectangle in wall_rectangles:
        ax.add_patch(rectangle)

    # Plot cameras
    camera_positions = [(camera_points[name][0], camera_points[name][1]) for name in camera_points]
    camera_names = list(camera_points.keys())
    
    # Scatter camera positions
    ax.scatter(*zip(*camera_positions), color='red', s=50)  # Larger size for visibility
    print(camera_proxi)
    # Draw links between cameras and annotate with distance, effective distance, and obstacles
    for camera_name, links in camera_proxi.items():
        for linked_camera, distance, effective_distance, obstacles in links:
            if distance <= effective_distance:
                # Get the positions
                pos1 = camera_points[camera_name]
                pos2 = camera_points[linked_camera]

            # Draw the line between the two cameras
                ax.plot([pos1[0], pos2[0]], [pos1[1], pos2[1]], color='blue', linestyle='--', alpha=0.5)

            # Annotate with distance, effective distance, and obstacles
                mid_x = (pos1[0] + pos2[0]) / 2
                mid_y = (pos1[1] + pos2[1]) / 2
                annotation = f'Dist: {distance:.2f}, Eff: {effective_distance:.2f}, Obst: {obstacles}'
                ax.text(mid_x, mid_y, annotation, fontsize=8, ha='center', va='center')

    # Set limits, labels, and title
    ax.set_xlim(-1, room.length + 1)
    ax.set_ylim(-1, room.width + 1)
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_title(f'Connectivity Network Inside {room.name}')

    # Display the plot
    plt.show()