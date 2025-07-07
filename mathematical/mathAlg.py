import math

class Room:
    def __init__(self, name, length, width, walls=None):
        self.name = name
        self.length = length
        self.width = width
        self.walls = [
            Wall(0, 0, length, 0),      # Bottom wall
            Wall(length, 0, length, width),  # Right wall
            Wall(length, width, 0, width),   # Top wall
            Wall(0, width, 0, 0)           # Left wall
        ]
        if walls is not None:
            self.walls.extend(walls)  # Add additional walls if provided
        self.points = [(x, y) for x in range(length + 1) for y in range(width + 1)]
    def area(self):
        return self.length * self.width
    def area_of_field_of_vision(self, camera):
        left_angle, right_angle = camera.get_field_of_view()
        visible_area = 0
        for wall in self.walls:
            if self.line_intersects(camera.x, camera.y, 
                                    camera.x + camera.reach * math.cos(math.radians(left_angle)), 
                                    camera.y + camera.reach * math.sin(math.radians(left_angle)), 
                                    wall.x1, wall.y1, wall.x2, wall.y2):
                # Calculate intersection points and visible area
                # This will require calculating the intersection points 
                # and possibly creating a polygon of the visible area.
                # For simplicity, assume we calculate the area directly.
                # More complex logic could be added here to handle the polygon.
                intersection_x1 = camera.x + camera.reach * math.cos(math.radians(left_angle))
                intersection_y1 = camera.y + camera.reach * math.sin(math.radians(left_angle))
                intersection_x2 = camera.x + camera.reach * math.cos(math.radians(right_angle))
                intersection_y2 = camera.y + camera.reach * math.sin(math.radians(right_angle))
                
                # Calculate area of the triangle formed by the camera and intersection points
                triangle_area = 0.5 * abs(camera.x * (intersection_y1 - intersection_y2) +
                                           intersection_x1 * (intersection_y2 - camera.y) +
                                           intersection_x2 * (camera.y - intersection_y1))
                visible_area += triangle_area

        return visible_area
    def visible_points_by_camera(self, camera):
        visible = []
        for point in self.points:
            if self.is_visible(camera, point):
                visible.append(point)
        return visible

    def is_visible(self, camera, point):
        x, y = point
        distance = math.hypot(x - camera.x, y - camera.y)
        if distance > camera.reach:
            return False

        for wall in self.walls:
            if self.line_intersects(camera.x, camera.y, x, y, wall.x1, wall.y1, wall.x2, wall.y2):
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
                if wall.point_on_segment(self, camera.x, camera.y)==False:
                    return False
        return test


    def __str__(self):
        return (f"Room(length={self.length}, width={self.width}, "
                f"area={self.area()}, walls={len(self.walls)}, cameras={len(self.cameras)})")


class Wall:
    def __init__(self, name, x1, y1, x2, y2):
        self.name = name
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
    def point_on_segment(self, px, py):
        area = (self.y2 - self.y1) * (px - self.x1) - (self.x2 - self.x1) * (py - self.y1)

        if area != 0:
            return False

        if min(self.x1, self.x2) <= px <= max(self.x1, self.x2) and min(self.y1, self.y2) <= py <= max(self.y1, self.y2):
            return True

        return False
    
    def __str__(self):
        return f"{self.name} from ({self.x1}, {self.y1}) to ({self.x2}, {self.y2})"


class Camera:
    def __init__(self, name, x, y, orientation, angle_of_sight, reach):
        self.name = name
        self.x = x
        self.y = y
        self.orientation = orientation
        self.angle_of_sight = angle_of_sight
        self.reach = reach

    def get_field_of_view(self):
        half_sight = self.angle_of_sight / 2
        left_angle = self.orientation - half_sight
        right_angle = self.orientation + half_sight
        return left_angle, right_angle


    def __str__(self):
        return (f"{self.name}(position=({self.x}, {self.y}), "
                f"orientation={self.orientation}°, "
                f"angle_of_sight={self.angle_of_sight}°, "
                f"reach={self.reach})")

'''
# Example usage
walls = [Wall(10, 10, 90, 10)]
cameras = [
    Camera(x=20, y=20, orientation=0, angle_of_sight=90, reach=30),
    Camera(x=80, y=40, orientation=180, angle_of_sight=90, reach=25)
]

my_room = Room(length=100, width=50, walls=walls, cameras=cameras)

print(my_room)

# Accessing the visibility matrix
my_room.point_matrix()  # Generate the matrix after adding walls and cameras
for point, data in my_room.matrix.items():
    print(f"Point {point}: {data['camera_count']} cameras pointing at it: {data['cameras']}")
'''