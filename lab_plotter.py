import matplotlib.pyplot as plt  # Importer la bibliothèque pyplot de matplotlib pour la visualisation
import numpy as np  # Importer numpy pour la manipulation de tableaux numériques
from lab_builder import *
json_file_path = "labo.json"  # Replace with your JSON file path
result = process_room_file(json_file_path)
room = setUpLab(result)
plt.figure(figsize=(room.length,room.width))
for i in range(len(room.walls)):
    print(room.walls[i])
    plt.plot([room.walls[i].x1,room.walls[i].x2],[room.walls[i].y1,room.walls[i].y2], label = room.walls[i].name)


# Set limits for the x-axis and y-axis
plt.xlim(0, room.length)  # Set x-axis limit
plt.ylim(0, room.width + 1)  # Set y-axis limit

# Add labels and titles
plt.title("Line Segment between Two Points")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")

# Show grid
#plt.grid()

# Display the plot
plt.show()