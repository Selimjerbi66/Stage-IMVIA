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