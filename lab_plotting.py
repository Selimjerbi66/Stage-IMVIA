from lab_builder import *  # Ensure this module contains necessary functions and classes

def plotLab(room, cameras, viewable):
    # Process the room file and set up the lab

    fig, ax = plt.subplots(figsize=(room.length, room.width))  # Width and Height of the plot

    # Draw the walls of the room
    for wall in room.walls:
        print(wall)
        # Create a rectangle patch for each wall
        rectangle = patches.Rectangle(
            (wall.xbl, wall.ybl),  # Bottom-left corner coordinates
            wall.length,           # Length of the rectangle
            wall.width,            # Width of the rectangle
            linewidth=1,           # Thickness of the rectangle's edge
            edgecolor=hex_codes[0],  # Color of the rectangle's edge (red)
            facecolor=hex_codes[0]  # No fill color for the rectangle
        )
        ax.add_patch(rectangle)

    # Set up cameras

    # Loop through each point in the matrix to visualize viewable points
    for point, data in viewable.items():
        x, y = point  # Unpack the tuple (x, y)
        n = len(data['cameras'])  # Number of cameras linked to the point
        color = hex_codes[n % len(hex_codes)]  # Cycle through hex_codes

        # Scatter the point with its respective color
        ax.scatter(x, y, color=color, s=1)

    # Plot cameras on the map
    for camera in cameras:
        ax.scatter(camera.x, camera.y, color='red', s=10)  # Smallest marker size
        ax.text(camera.x, camera.y, camera.name, fontsize=10)

    # Set limits for the x-axis and y-axis
    ax.set_xlim(-1, room.length + 1)  # X-axis limits
    ax.set_ylim(-1, room.width + 1)    # Y-axis limits

    # Add labels and titles
    ax.set_xlabel('X-axis')  # X-axis label
    ax.set_ylabel('Y-axis')  # Y-axis label
    ax.set_title(room.name)   # Title of the plot

    # Display the plot
    plt.show()