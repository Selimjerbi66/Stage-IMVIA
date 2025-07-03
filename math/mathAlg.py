class Room:
    def __init__(self, length, width):
        # Initialize the room's dimensions
        self.length = length
        self.width = width
        self.walls = []

    def area(self):
        # Calculate the area of the room
        return self.length * self.width

    def add_wall(self, x1, y1, x2, y2):
        # Check if points are within room boundaries
        if self.is_within_bounds(x1, y1) and self.is_within_bounds(x2, y2):
            wall = Wall(x1, y1, x2, y2)
            self.walls.append(wall)
        else:
            raise ValueError("Wall points must be within the room boundaries.")

    def is_within_bounds(self, x, y):
        # Check if a point is within the room
        return 0 <= x <= self.length and 0 <= y <= self.width

    def __str__(self):
        return f"Room(length={self.length}, width={self.width}, area={self.area()}, walls={len(self.walls)})"


class Wall:
    def __init__(self, x1, y1, x2, y2):
        # Initialize the wall's endpoints
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def __str__(self):
        return f"Wall from ({self.x1}, {self.y1}) to ({self.x2}, {self.y2})"


# Usage example
my_room = Room(10, 15)
my_room.add_wall(2, 3, 5, 3)  # Valid wall
print(my_room)

try:
    my_room.add_wall(12, 3, 15, 3)  # Invalid wall
except ValueError as e:
    print(e)