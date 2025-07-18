def ConnectedCams(room, cameras, d, w):
    try:
        # Ensure w is less than or equal to 100
        if w > 100:
            raise ValueError("w must be less than or equal to 100.")

        walls = room.walls
        camera_points = {camera.name: (camera.x, camera.y) for camera in cameras}
        networks = []
        camera_proxi = {camera.name: [] for camera in cameras}  # Initialize camera_proxi

        # Use a set to track processed cameras
        processed_cameras = set()

        # Function to perform BFS
        def bfs(start_camera):
            queue = [start_camera]  # Start with the initial camera
            connected_cameras = []  # To store the connected cameras
            while queue:
                current_camera = queue.pop(0)
                if current_camera in processed_cameras:
                    continue  # Skip already processed cameras

                connected_cameras.append(current_camera)
                processed_cameras.add(current_camera)

                # Check connectivity with all other cameras
                for c2 in camera_points:
                    if c2 in processed_cameras or c2 == current_camera:
                        continue  # Skip already processed or the same camera

                    q = obs(camera_points[current_camera], camera_points[c2], walls, room)
                    total_interference = (1 - w / 100) ** q
                    distance = dist(camera_points[current_camera], camera_points[c2])
                    effective_connectivity_distance = d * total_interference

                    if distance <= effective_connectivity_distance:
                        queue.append(c2)  # Add to queue for further exploration

            return connected_cameras

        # Iterate through all cameras
        for c in camera_points:
            if c not in processed_cameras:
                listcon = bfs(c)  # Get all connected cameras starting from c
                if listcon:
                    networks.append(listcon)  # Add the network to the list

        # Calculate camera_proxi after determining networks
        camera_proxi = proxicharger(room, camera_proxi, camera_points, d, w)

        return networks, camera_points, camera_proxi  # Return the new variable

    except ValueError as e:
        print(f"ValueError: {e}")
        return [], {}, {}
def dist(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

def obs(p1, p2, walls, room):
    count = 0
    for wall in walls:
        if room.line_intersects_rectangle(p1[0], p1[1], p2[0], p2[1], wall):
            count += 1
    return count




    return count
def proxicharger(room, camera_proxi, camera_points, d, w):
    # Initialize camera_points and camera_proxi
    walls = room.walls

    # Iterate through each pair of cameras
    for c1 in camera_points:
        for c2 in camera_points:
            if c1 != c2:  # Avoid self-comparison
                q = obs(camera_points[c1], camera_points[c2], walls, room)
                total_interference = (1 - w / 100) ** q
                distance = dist(camera_points[c1], camera_points[c2])
                print('distance between',c1,' and ',c2," is : ", distance)
                effective_connectivity_distance = d * total_interference

                # Check the condition for connectivity
                if distance <= effective_connectivity_distance:
                    camera_proxi[c1].append((c2, distance, effective_connectivity_distance, q))

    return camera_proxi
'''
def ConnectedCams(room, cameras, d, w):
    # Ensure w is less than or equal to 100
    if w > 100:
        raise ValueError("w must be less than or equal to 100.")
    
    walls = room.walls
    camera_points = {camera.name: (camera.x, camera.y) for camera in cameras}
    cams = list(camera_points.keys())
    networks = []
    camera_proxi = {camera.name: [] for camera in cameras}  # Initialize camera_proxi
    print("1")
    while cams:

        c1 = cams[0]
        listcon = [c1]
        cams.remove(c1)

        # First connectivity check for c1
        for c2 in cams[:]:  # Use a copy to avoid modification issues
            q = obs(c1, c2, walls, room)
            total_interference = (1 - w / 100) ** q
            distance = dist(camera_points[c1], camera_points[c2])
            print('distance between', c1, ' and ', c2, " is : ", distance)
            effective_connectivity_distance = d * total_interference
            if distance <= effective_connectivity_distance:
                listcon.append(c2)
                cams.remove(c2)

        # Check connectivity for cameras already in listcon
        for c1 in listcon[1:]:  # Skip the first camera as it's already processed
            for c2 in cams[:]:  # Use a copy to avoid modification issues
                q = obs(c1, c2, walls, room)
                total_interference = (1 - w / 100) ** q
                distance = dist(camera_points[c1], camera_points[c2])
                print('distance between', c1, ' and ', c2, " is : ", distance)
                effective_connectivity_distance = d * total_interference
                if distance <= effective_connectivity_distance:
                    listcon.append(c2)
                    cams.remove(c2)

        networks.append(listcon)

    camera_proxi = proxicharger(room, camera_proxi, camera_points, d, w)

    return networks, camera_points, camera_proxi  # Return the new variable
    '''



'''     for c1 in camera_points:
        listcon = [c1]
        for c2 in camera_points:
            if c2 == c1:
                continue
            q = obs(camera_points[c1], camera_points[c2], walls, room)
            total_interference = (1 - w / 100) ** q
            distance = dist(camera_points[c1], camera_points[c2])
            print('distance between',c1,' and ',c2," is : ", distance)
            effective_connectivity_distance = d * total_interference

            if distance <= effective_connectivity_distance:
                listcon.append(c2)
        networks.append(listcon)

        # Calculate camera_proxi after determining networks
    print('here')
    camera_proxi = proxicharger(room, camera_proxi, camera_points, d, w)

    return networks, camera_points, camera_proxi  # Return the new variable'''

