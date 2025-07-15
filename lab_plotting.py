from lab_builder import *  # Ensure this module contains necessary functions and classes

def plotLab(room, cameras, viewable):
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(room.length, room.width))

    # Draw the walls of the room using a collection
    wall_rectangles = [patches.Rectangle((wall.xbl, wall.ybl), wall.length, wall.width,
                                          linewidth=1, edgecolor=hex_codes[0], facecolor=hex_codes[0])
                       for wall in room.walls]
    for rectangle in wall_rectangles:
        ax.add_patch(rectangle)

    # Prepare to plot viewable points
    points = []
    colors = []
    sizes = []
    
    for point, data in viewable.items():
        x, y = point
        n = len(data['cameras'])
        color = hex_codes[n % len(hex_codes)]
        
        points.append((x, y))
        colors.append(color)
        sizes.append(1)  # Size for scatter plot

    # Convert to numpy arrays for more efficient plotting
    points = np.array(points)
    
    # Scatter all points in one go
    ax.scatter(points[:, 0], points[:, 1], color=colors, s=sizes)

    # Plot cameras
    camera_positions = [(camera.x, camera.y) for camera in cameras]
    ax.scatter(*zip(*camera_positions), color='red', s=10)

    # Set limits, labels, and title
    ax.set_xlim(-1, room.length + 1)
    ax.set_ylim(-1, room.width + 1)
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_title(room.name)

    # Display the plot
    plt.show()