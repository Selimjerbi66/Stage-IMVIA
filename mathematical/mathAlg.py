import math

class Room:
    def __init__(self, name, length, width, walls=None):
        self.name = name
        self.length = int(length)
        self.width = int(width)
        self.walls = [
            Wall("side1", 0, 0, length, 0, 0),      # Bottom wall
            Wall("side2",length, 0, length, width, 0),  # Right wall
            Wall("side3",length, width, 0, width, 0),   # Top wall
            Wall("side4",0, width, 0, 0, 0)           # Left wall
        ]
        if walls is not None:
            self.walls.extend(walls)  # Add additional walls if provided
        self.points = [(x, y) for x in range(length + 1) for y in range(width + 1)]
    def area(self):
        return self.length * self.width
    '''def area_of_field_of_vision(self, camera):
        left_angle, right_angle = camera.get_field_of_view()
        visible_area = 0
        for wall in self.walls:
            if self.line_intersects(camera.x, camera.y, 
                                    camera.x + camera.range * math.cos(math.radians(left_angle)), 
                                    camera.y + camera.range * math.sin(math.radians(left_angle)), 
                                    wall.x1, wall.y1, wall.x2, wall.y2):
                # Calculate intersection points and visible area
                # This will require calculating the intersection points 
                # and possibly creating a polygon of the visible area.
                # For simplicity, assume we calculate the area directly.
                # More complex logic could be added here to handle the polygon.
                intersection_x1 = camera.x + camera.range * math.cos(math.radians(left_angle))
                intersection_y1 = camera.y + camera.range * math.sin(math.radians(left_angle))
                intersection_x2 = camera.x + camera.range * math.cos(math.radians(right_angle))
                intersection_y2 = camera.y + camera.range * math.sin(math.radians(right_angle))
                
                # Calculate area of the triangle formed by the camera and intersection points
                triangle_area = 0.5 * abs(camera.x * (intersection_y1 - intersection_y2) +
                                           intersection_x1 * (intersection_y2 - camera.y) +
                                           intersection_x2 * (camera.y - intersection_y1))
                visible_area += triangle_area

        return visible_area'''
    
    def visible_points_by_camera(self, camera):
        visible = []
        for point in self.points:
            if self.is_visible(camera, point):
                visible.append(point)
        return visible

    def is_visible(self, camera, point):
        x, y = point
        distance = math.hypot(x - camera.x, y - camera.y)
        if distance > camera.range:
            return False

        for wall in self.walls:
            if wall.thickness == 0:

                if self.line_intersects(camera.x, camera.y, x, y, wall.x1, wall.y1, wall.x2, wall.y2):
                    return False
            else:
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
        # Define the rectangle sides using the wall's corners
        sides = [
            (wall.x3, wall.y3, wall.x4, wall.y4),  # Top side
            (wall.x4, wall.y4, wall.x6, wall.y6),  # Right side
            (wall.x6, wall.y6, wall.x5, wall.y5),  # Bottom side
            (wall.x5, wall.y5, wall.x3, wall.y3),  # Left side
        ]
        
        # Check each side for intersection
        for (sx1, sy1, sx2, sy2) in sides:
            if self.line_intersects(xl1, yl1, xl2, yl2, sx1, sy1, sx2, sy2):
                return True
        
        return False
    def line_intersects(self, x1, y1, x2, y2, x3, y3, x4, y4):
        denominator = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)

        if denominator == 0:
            if self.on_segment(x1, y1, x2, y2, x3, y3) or self.on_segment(x1, y1, x2, y2, x4, y4) or self.on_segment(x3, y3, x4, y4, x1, y1) or self.on_segment(x3, y3, x4, y4, x2, y2):
                return True
            return False

        t = ((x3 - x1) * (y2 - y1) - (y3 - y1) * (x2 - x1)) / denominator
        u = -((x4 - x3) * (y3 - y1) - (y4 - y3) * (x3 - x1)) / denominator

        if 0 <= t <= 1 and 0 <= u <= 1:
            intersection_x = x1 + t * (x2 - x1)
            intersection_y = y1 + t * (y2 - y1)
            return self.on_segment(x1, y1, x2, y2, intersection_x, intersection_y) and self.on_segment(x3, y3, x4, y4, intersection_x, intersection_y)

        return False

    def on_segment(self, px, py, qx, qy, rx, ry):
        return min(px, qx) <= rx <= max(px, qx) and min(py, qy) <= ry <= max(py, qy)

    def point_matrix(self, cameras):
        matrix = {}
        
        for point in self.points:
            matrix[point] = {
                'camera_count': 0,
                'cameras': []
            }
        
        for camera in cameras:
            for point in self.points:
                if self.is_visible(camera, point):
                    matrix[point]['camera_count'] += 1
                    matrix[point]['cameras'].append(camera)
        return matrix
    def compatibleCameraSet(self, cameras):
        test = True
        i=0
        while test and i<len(cameras):
            camera=cameras[i]
            if not(0<=camera.x<=self.length and 0<=camera.y<=self.width):
                test=False
        for camera in cameras:
            for wall in self.walls:
                if wall.thickness == 0:
                    if wall.point_on_segment(self, camera.x, camera.y)==True:
                        return False
                else:
                    if wall.point_on_rectangle(self, camera.x, camera.y)==True:
                        return False

        return test


    def __str__(self):
        return (f"Room(length={self.length}, width={self.width}, "
                f"area={self.area()}, walls={len(self.walls)})")


class Wall:
    def __init__(self, name, x1, y1, x2, y2, thickness=0):
        self.name = name
        self.x1 = int(x1)
        self.y1 = int(y1)
        self.x2 = int(x2)
        self.y2 = int(y2)
        if thickness ==0 :
            self.thickness = int(thickness)
        # Calculate corners of the rectangle
        if thickness !=0:
            
            self.x3, self.y3, self.x4, self.y4, self.x5, self.y5, self.x6, self.y6 = calculate_corners(x1, y1, x2, y2, thickness)

    def point_on_segment(self, px, py):
        area = (self.y2 - self.y1) * (px - self.x1) - (self.x2 - self.x1) * (py - self.y1)

        if area != 0:
            return False

        if min(self.x1, self.x2) <= px <= max(self.x1, self.x2) and min(self.y1, self.y2) <= py <= max(self.y1, self.y2):
            return True

        return False
    def point_on_rectangle(self, px, py):
    # Create a list of corners
        corners = [
        (self.x3, self.y3),  # Top-left
        (self.x4, self.y4),  # Top-right
        (self.x6, self.y6),  # Bottom-right
        (self.x5, self.y5),  # Bottom-left
        ]

    # Use the ray-casting algorithm to check if the point is inside the polygon
        inside = False
        n = len(corners)
    
        for i in range(n):
            x1, y1 = corners[i]
            x2, y2 = corners[(i + 1) % n]
        
        # Check if the point is within the y-bounds of the edge
            if ((y1 > py) != (y2 > py)) and (px < (x2 - x1) * (py - y1) / (y2 - y1) + x1):
                inside = not inside

        return inside
    def __str__(self):
        return f"{self.name} from ({self.x1}, {self.y1}) to ({self.x2}, {self.y2})"
def calculate_corners(x1, y1, x2, y2, thickness):
    # Calculate the angle of the wall
        dx = x2 - x1
        dy = y2 - y1
        angle = math.atan2(dy, dx)

        # Calculate the half thickness offset
        half_thickness = thickness / 2

        # Calculate the offsets using the angle
        offset_x = half_thickness * math.cos(angle + math.pi / 2)  # Perpendicular direction
        offset_y = half_thickness * math.sin(angle + math.pi / 2)

        # Calculate the corners of the rectangle
        x3 = x1 + offset_x
        y3 = y1 + offset_y
        x4 = x2 + offset_x
        y4 = y2 + offset_y
        x5 = x1 - offset_x
        y5 = y1 - offset_y
        x6 = x2 - offset_x
        y6 = y2 - offset_y

        return x3, y3, x4, y4, x5, y5, x6, y6

class Camera:
    def __init__(self, name, x, y, orientation, angle_of_sight, range):
        self.name = name
        self.x = x
        self.y = y
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