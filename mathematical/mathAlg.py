import math
from mathematical.camfield import *
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

    # Iterate over the range of sight
        for i in range(- camera.range, camera.range + 1):
            for j in range(- camera.range, camera.range + 1):
            # Calculate the actual coordinates based on camera position
                x = camera.x + i
                y = camera.y + j
            
            # Check if the point is within the room's limits
                if 0 <= x < self.length and 0 <= y < self.width:
                    point_list.append((x, y))
    
        return point_list


    def visible_points_by_camera(self, camera):
        visible = []
        for point in self.approximate_points(camera):
            if self.is_visible(camera, point):
                print (point)
                visible.append(point)
        return visible


    def is_visible(self, camera, point):
        x, y = point
        distance = math.hypot(x - camera.x, y - camera.y)
        if distance > camera.range:
            return False

        for wall in self.walls:
            if self.line_intersects_rectangle(camera.x, camera.y, x, y, wall):
                return False
                
        angle_to_point = self.calculate_angle(camera, point)
        left_angle, right_angle = camera.get_field_of_view()

        angle_to_point = angle_to_point % 360
        left_angle = left_angle % 360
        right_angle = right_angle % 360

        if left_angle < right_angle:
            return left_angle <= angle_to_point <= right_angle
        else:
            return angle_to_point >= left_angle or angle_to_point <= right_angle

    def calculate_angle(self, camera, point):
        return math.degrees(math.atan2(point[1] - camera.y, point[0] - camera.x))
    def line_intersects_rectangle(self, xl1, yl1, xl2, yl2, wall):
    # Calculate rectangle corners based on bottom-left corner, length, and width
        xbl, ybl = wall.xbl, wall.ybl
        xbr = xbl + wall.length  # Bottom-right corner
        ytl = ybl + wall.width   # Top-left corner y-coordinate

    # Define the rectangle sides using the calculated corners
        sides = [
        (xbl, ytl, xbr, ytl),  # Top side
        (xbr, ybl, xbr, ytl),  # Right side
        (xbl, ybl, xbr, ybl),   # Bottom side
        (xbl, ybl, xbl, ytl)    # Left side
    ]
    
    # Check each side for intersection
        for (sx1, sy1, sx2, sy2) in sides:
            if self.line_intersects(xl1, yl1, xl2, yl2, sx1, sy1, sx2, sy2):
                return True

        return False
    def line_intersects(self, x1, y1, x2, y2, x3, y3, x4, y4):
    # Calculate the denominator
        denominator = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)

    # Check if lines are parallel
        if denominator == 0:
        # Check if any endpoint is on the other segment
            return (self.on_segment(x1, y1, x2, y2, x3, y3) or
                    self.on_segment(x1, y1, x2, y2, x4, y4) or
                    self.on_segment(x3, y3, x4, y4, x1, y1) or
                    self.on_segment(x3, y3, x4, y4, x2, y2))

    # Calculate t and u
        t = ((x3 - x1) * (y2 - y1) - (y3 - y1) * (x2 - x1)) / denominator
        u = -((x4 - x3) * (y3 - y1) - (y4 - y3) * (x3 - x1)) / denominator

    # Check if the intersection point lies within both segments
        if 0 <= t <= 1 and 0 <= u <= 1:
            intersection_x = x1 + t * (x2 - x1)
            intersection_y = y1 + t * (y2 - y1)
            return self.on_segment(x1, y1, x2, y2, intersection_x, intersection_y) and self.on_segment(x3, y3, x4, y4, intersection_x, intersection_y)

        return False

    def on_segment(self, px, py, qx, qy, rx, ry):
    # Check if point (rx, ry) is on the segment (px, py) to (qx, qy)
        return min(px, qx) <= rx <= max(px, qx) and min(py, qy) <= ry <= max(py, qy)

    def check_alignments(self, cameras):
        camView=camViewer(self, cameras)
        for camera_name, points in camView:
            camera = next((cam for cam in cameras if cam.name == camera_name), None)
            if camera is None:
                continue
            
            # Convert points to a set for efficient removal
            to_remove = set()

            for p1 in points:
                for p2 in points:
                    if p1 != p2:  # Avoid checking the same point
                        if self.on_segment(camera.x, camera.y, p1[0], p1[1], p2[0], p2[1]):
                            to_remove.add(p2)  # Add intermediary point to remove set

            # Remove intermediary points from the list of points
            points[:] = [point for point in points if point not in to_remove]

        return camView

    def point_matrix(self, cameras):
        matrix = {}
    
        for camera in cameras:
        # Get visible points for the current camera once
            visible_points = self.visible_points_by_camera(camera)
        
            for point in visible_points:
                if point not in matrix:
                    matrix[point] = {
                        'camera_count': 0,
                        'cameras': []
                    }
                matrix[point]['camera_count'] += 1
                matrix[point]['cameras'].append(camera.name)
    
        return matrix
    def compatibleCameraSet(self, cameras):
        test = True
        i=0
        while test and i<len(cameras):
            camera=cameras[i]
            print(i)
            if not(0<=camera.x<=self.length and 0<=camera.y<=self.width):
                test=False
            i+=1
        for camera in cameras:
            for wall in self.walls:
                if wall.point_on_rectangle(camera.x, camera.y)==True:
                    return False

        return test


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
        bottom_right = (max(x1, x2), y1 - y_offset)
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