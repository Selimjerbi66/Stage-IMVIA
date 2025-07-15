import math
from mathematical.camfield import *
import matplotlib.pyplot as plt  # Importer la bibliothèque pyplot de matplotlib pour la visualisation
import matplotlib.patches as patches
import numpy as np  # Importer numpy pour la manipulation de tableaux numériques
class Room:
    def __init__(self, name, length, width, walls=None):
        self.name = name
        self.length = int(length)
        self.width = int(width)
        self.walls = [
            Wall("side1", 0, 0, length, 0, 1),      # Bottom wall
            Wall("side2",length, 0, length, width, 1),  # Right wall
            Wall("side3",length, width, 0, width, 1),   # Top wall
            Wall("side4",0, width, 0, 0, 1)           # Left wall
        ]
        if walls is not None:
            self.walls.extend(walls)  # Add additional walls if provided
        self.points = [(x, y) for x in range(length + 1) for y in range(width + 1)]
    def area(self):
        return self.length * self.width

    def approximate_points(self, camera):
        point_list = []

    # Extract camera attributes for better readability
        camera_x = camera.x
        camera_y = camera.y
        camera_range = camera.range

    # Calculate bounds based on camera position and range
        min_x = max(0, camera_x - camera_range)
        max_x = min(self.length, camera_x + camera_range)
        min_y = max(0, camera_y - camera_range)
        max_y = min(self.width, camera_y + camera_range)

    # Iterate over the range of sight within the calculated bounds
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                point_list.append((x, y))

        return point_list


    def visible_points_by_camera(self, camera):
    # Use a list comprehension for better performance and readability
        return [point for point in self.approximate_points(camera) if self.is_visible(camera, point)]


    def is_visible(self, camera, point):
        x, y = point
        distance_squared = (x - camera.x) ** 2 + (y - camera.y) ** 2

    # Early exit if the point is out of the camera's range (using squared distance)
        if distance_squared > camera.range ** 2:
            return False

    # Check for intersection with walls
        if any(self.line_intersects_rectangle(camera.x, camera.y, x, y, wall) for wall in self.walls):
            return False

        angle_to_point = self.calculate_angle(camera, point) % 360
        left_angle, right_angle = camera.get_field_of_view()

    # Normalize camera angles
        left_angle %= 360
        right_angle %= 360

    # Check if the angle to the point is within the camera's field of view
        if left_angle < right_angle:
            return left_angle <= angle_to_point <= right_angle
        else:
        # Handle wrap-around case
            return angle_to_point >= left_angle or angle_to_point <= right_angle

    def calculate_angle(self, camera, point):
        return math.degrees(math.atan2(point[1] - camera.y, point[0] - camera.x))

    def orientation(self, p, q, r):
        """ Determine the orientation of the triplet (p, q, r).
            0 -> p, q and r are collinear
            1 -> Clockwise
            2 -> Counterclockwise
        """
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            return 0
        return 1 if val > 0 else 2

    def on_segment(self, p, q, r):
        """ Check if point q lies on the line segment 'pr' """
    # Check for collinearity using the area method
        area = (p[0] * (r[1] - q[1]) +
                r[0] * (q[1] - p[1]) +
                q[0] * (p[1] - r[1]))
    
        if area != 0:  # Points are not collinear
            return False

    # Check if q is within the bounding box defined by p and r
        if (min(p[0], r[0]) <= q[0] <= max(p[0], r[0]) and
            min(p[1], r[1]) <= q[1] <= max(p[1], r[1])):
            return True
    
        return False

    def do_lines_intersect(self, p1, p2, p3, p4):
        """ Check if line segments p1p2 and p3p4 intersect. """
        o1 = self.orientation(p1, p2, p3)
        o2 = self.orientation(p1, p2, p4)
        o3 = self.orientation(p3, p4, p1)
        o4 = self.orientation(p3, p4, p2)

        # General case
        if o1 != o2 and o3 != o4:
            return True

        # Special cases for collinear points
        if o1 == 0 and self.on_segment(p1, p3, p2): return True
        if o2 == 0 and self.on_segment(p1, p4, p2): return True
        if o3 == 0 and self.on_segment(p3, p1, p4): return True
        if o4 == 0 and self.on_segment(p4, p2, p3): return True

        return False

    def line_intersects_rectangle(self, xl1, yl1, xl2, yl2, wall):
        """ Check if the line segment intersects with the rectangle. """

        p1, p2, p3, p4 = corners_coordinates(wall.length, wall.width, wall.xbl, wall.ybl)
        seg_start = (xl1, yl1)
        seg_end = (xl2, yl2)

        # Check intersection with each edge of the rectangle
        return (self.do_lines_intersect(p1, p2, seg_start, seg_end) or
                self.do_lines_intersect(p2, p3, seg_start, seg_end) or
                self.do_lines_intersect(p3, p4, seg_start, seg_end) or
                self.do_lines_intersect(p4, p1, seg_start, seg_end))

    def check_alignments(self, cameras):
        camView = camViewer(self, cameras)
        file = open('undesired.txt', 'w')  # Open file for writing
        for camera_name, points in camView:
            camera = next((cam for cam in cameras if cam.name == camera_name), None)
            if camera is None:
                continue
        
        # Convert points to a set for efficient removal
            to_remove = set()

        # Iterate over pairs of points
            for p1 in points:
                for p2 in points:
                    if p1 != p2:  # Avoid checking the same point
                        p = (camera.x, camera.y)
                        q = (p2[0], p2[1])
                        r = (p1[0], p1[1])
                        if self.on_segment(p, q, r):
                        # Determine which point to remove: the closer one
                            dist_p1 = (p1[0] - camera.x) ** 2 + (p1[1] - camera.y) ** 2
                            dist_p2 = (p2[0] - camera.x) ** 2 + (p2[1] - camera.y) ** 2

                            # Print the equation of the line
                            print(f"Camera at {p}, Point1 at {r}, Point2 at {q}")
                            print(f"Equation: Line through {p} and {q}")
                            # Save messages to the file
                            file.write(f"Camera at {p}, Point1 at {r}, Point2 at {q}\n")
                            file.write(f"Equation: Line through {p} and {q}\n")
                            if dist_p1 < dist_p2:
                                print(f"Removing Point1 {p1} (closer to camera). Aligned with Point2 {p2}.")
                                file.write(f"Removing Point1 {p1} (closer to camera). Aligned with Point2 {p2}.\n")
                                to_remove.add(p1)  # Remove the closer point
                            else:
                                print(f"Removing Point2 {p2} (closer to camera). Aligned with Point1 {p1}.")
                                file.write(f"Removing Point2 {p2} (closer to camera). Aligned with Point1 {p1}.\n")
                                to_remove.add(p2)  # Remove the closer point

        # Remove intermediary points from the list of points
            points[:] = [point for point in points if point not in to_remove]

        return camView

    def point_matrix(self, cameras):
        matrix = {}

        for camera in cameras:
        # Get visible points for the current camera once
            visible_points = self.visible_points_by_camera(camera)

        # Use a set to avoid redundant entries
            camera_name = camera.name
            for point in visible_points:
                if point in matrix:
                    matrix[point]['cameras'].append(camera_name)
                else:
                    matrix[point] = {'cameras': [camera_name]}  # Initialize with the camera name

        return matrix
    def compatibleCamera(self, camera, reject_list):
    # Check if the camera is within the room dimensions
        if not (0 <= camera.x <= self.length and 0 <= camera.y <= self.width):
            reject_list.append(camera)
            return False, reject_list
    
    # Check if the camera is on any wall
        for wall in self.walls:
            if wall.point_on_rectangle(camera.x, camera.y):
                reject_list.append(camera)
                return False, reject_list

        return True, reject_list
    def compatibleCameraSet(self, cameras):
        reject_list = []  # Initialize the reject list

        for camera in cameras:
            is_compatible, reject_list = self.compatibleCamera(camera, reject_list)
            if not is_compatible:
                return False  # Return False immediately if any camera is incompatible

        return True  # All cameras are compatible

    def __str__(self):
        return (f"Room(length={self.length}, width={self.width}, "
                f"area={self.area()}, walls={len(self.walls)})")


class Wall:
    def __init__(self, name, x1, y1, x2, y2, thickness):
        self.name = name
        self.x1 = int(x1)
        self.y1 = int(y1)
        self.x2 = int(x2)
        self.y2 = int(y2)
        self.thickness = int(thickness)
        # Calculate corners of the rectangle
        if thickness !=0:
            
            self.length, self.width, self.xbl, self.ybl = calculate_corners(x1, y1, x2, y2, thickness)

    def point_on_segment(self, px, py):
        area = (self.y2 - self.y1) * (px - self.x1) - (self.x2 - self.x1) * (py - self.y1)

        if area != 0:
            return False

        if min(self.x1, self.x2) <= px <= max(self.x1, self.x2) and min(self.y1, self.y2) <= py <= max(self.y1, self.y2):
            return True

        return False
    def point_on_rectangle(self, px, py):
        # Extract the bottom-left corner and dimensions
        xbl = self.xbl  # Bottom-left x-coordinate
        ybl = self.ybl  # Bottom-left y-coordinate
        length = self.length
        width = self.width  # Width of the rectangle

        # Check if the point is within the rectangle's bounds
        inside = (xbl <= px <= xbl + length) and (ybl <= py <= ybl + width)

        return inside
    def __str__(self):
        return (f"Length: {self.length}, Width: {self.width}, "
                f"Bottom-left corner: ({self.xbl}, {self.ybl})")
def calculate_corners(x1, y1, x2, y2, thickness):
    # Determine if the line is horizontal or vertical
    if y1 == y2:  # Horizontal line
        y_offset = thickness / 2
        top_left = (min(x1, x2), y1 + y_offset)
        top_right = (max(x1, x2), y1 + y_offset)
        bottom_left = (min(x1, x2), y1 - y_offset)
    elif x1 == x2:  # Vertical line
        x_offset = thickness / 2
        top_left = (x1 - x_offset, max(y1, y2))
        top_right = (x1 + x_offset, max(y1, y2))
        bottom_left = (x1 - x_offset, min(y1, y2))
    else:
        raise ValueError("The line must be either horizontal or vertical.")

    # Calculate length and width from corners
    length = abs(top_right[0] - top_left[0])  # Length follows the x-axis
    width = abs(top_left[1] - bottom_left[1])  # Width follows the y-axis

    bottom_left_corner = bottom_left  # Bottom-left corner is already defined

    return length, width, bottom_left_corner[0], bottom_left_corner[1]
def corners_coordinates(length, width, bottom_left_x, bottom_left_y):
    """ Calculate the coordinates of the rectangle corners.

    Args:
        length (float): The length of the rectangle.
        width (float): The width of the rectangle.
        bottom_left_x (float): The x-coordinate of the bottom-left corner.
        bottom_left_y (float): The y-coordinate of the bottom-left corner.

    Returns:
        list: A list of tuples representing the corners in the order:
        (bottom-left, bottom-right, upper-right, upper-left).
    """
    bl = (bottom_left_x, bottom_left_y)
    br = (bottom_left_x + length, bottom_left_y)
    ur = (bottom_left_x + length, bottom_left_y + width)
    ul = (bottom_left_x, bottom_left_y + width)
    
    return [bl, br, ur, ul]
class Camera:
    def __init__(self, name, x, y, orientation, angle_of_sight, range):
        self.name = name
        self.x = x
        self.y = y
        self.pos = (x,y)
        self.orientation = orientation
        self.angle_of_sight = angle_of_sight
        self.range = range

    def get_field_of_view(self):
        half_sight = self.angle_of_sight / 2
        left_angle = self.orientation - half_sight
        right_angle = self.orientation + half_sight
        return left_angle, right_angle


    def __str__(self):
        return (f"{self.name}(position=({self.x}, {self.y}), "
                f"orientation={self.orientation}°, "
                f"angle_of_sight={self.angle_of_sight}°, "
                f"range={self.range})")




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
'''
# Example usage
walls = [Wall(10, 10, 90, 10)]
cameras = [
    Camera(x=20, y=20, orientation=0, angle_of_sight=90, range=30),
    Camera(x=80, y=40, orientation=180, angle_of_sight=90, range=25)
]

my_room = Room(length=100, width=50, walls=walls, cameras=cameras)

print(my_room)

# Accessing the visibility matrix
my_room.point_matrix()  # Generate the matrix after adding walls and cameras
for point, data in my_room.matrix.items():
    print(f"Point {point}: {data['camera_count']} cameras pointing at it: {data['cameras']}")
'''