def outlineView(viewlist):
    newlist=[]
    for p in viewlist:
        if not( (p[0],p[1]-1) in viewlist and (p[0],p[1]) in viewlist):
            newlist.append(p)
    return(newlist)
def camViewer(room, cameras):
    s=[]
    for i in cameras:
        to_view = room.visible_points_by_camera(i)
        s.append((i.name,to_view))
        '''print(s)'''
    return (s)
def zoneViewer(zones, matrix):
    data=dict()
    for zone in zones:
        data[zone.name]=zone.visibility_rate(matrix)
    return data
def zoned(zones, point):
    """
    Check if the given point is within any of the specified zones.

    Args:
        zones (list): A list of Zone objects.
        point (tuple): A tuple representing the point (x, y).

    Returns:
        bool: True if the point is within any zone, False otherwise.
    """
    for zone in zones:
        if zone.interval(point):
            return True
    return False

def closeCam(point, matrix, cameras):
    """
    Find the index of the closest camera to the given point based on the visibility matrix.

    Args:
        point (tuple): A tuple representing the point (x, y).
        matrix (dict): The visibility matrix.
        cameras (list): A list of camera objects.

    Returns:
        int: The index of the closest camera, or None if no camera is visible.
    """
    if point not in matrix:
        return None  # Point not in the matrix

    # Get the list of cameras that can see the point
    visible_cameras = matrix[point]['cameras']
    closest_camera_index = None
    closest_distance_squared = float('inf')

    # Iterate through the list of cameras
    for camera in cameras:
        # Check if the camera can see the point
        if camera.name in visible_cameras:
            # Calculate the squared distance from the camera to the point
            distance_squared = (camera.x - point[0]) ** 2 + (camera.y - point[1]) ** 2

            # Check if this camera is the closest one based on squared distance
            if distance_squared < closest_distance_squared:
                closest_distance_squared = distance_squared
                closest_camera_index = camera.index  # Store the index instead of the name

    return closest_camera_index
