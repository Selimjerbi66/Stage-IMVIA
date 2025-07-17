'''def connectedCams(room,d,w):
    cameras=room.cameras
    walls=room.walls
    camera_names = [camera.name for camera in cameras]
    camera_points = {camera.name: (camera.x, camera.y) for camera in cameras}
    m=0
    listcon=[]
    cams = camera_names
    ll=list()
    while len(cams)!=0:
        m+=m
        ll.append(listcon)
        listcon=[]
        c=cams[0]
        listcon.append(c)
        cams.remove(c)
        for c2 in cams:
            q= obs(camera_points(c),camera_points(c2),walls,room)
            if dist(camera_points(c),camera_points(c2))+q*w <= d:
                listcon.append(c2)
                cams.remove(c2)
        i=1
        while len(cams)!=0 and i <len(listcon):
            c=listcon[i]
            for c2 in cams:
                q=obs(camera_points(c),camera_points(c2),walls,room)
                if dist(camera_points(c),camera_points(c2))+q*w <= d:
                    listcon.append(c2)
                    cams.remove(c2)
            i+=1
    return (ll)'''
def ConnectedCams(room, cameras, d, w):
    cameras
    walls = room.walls
    camera_names = [camera.name for camera in cameras]
    camera_points = {camera.name: (camera.x, camera.y) for camera in cameras}
    networks = []
    
    while camera_names:
        listcon = []
        c = camera_names[0]
        listcon.append(c)
        camera_names.remove(c)

        for c2 in camera_names[:]:  # Create a copy of the list to avoid modification issues
            q = obs(camera_points[c], camera_points[c2], walls, room)
            effective_distance = dist(camera_points[c], camera_points[c2]) + q * w
            if effective_distance <= d:
                listcon.append(c2)
                camera_names.remove(c2)

        networks.append(listcon)

    return networks, camera_points



def dist(p1,p2):
    x1, y1 = p1
    x2, y2 = p2
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2)**0.5
def obs(p1,p2,walls,room):
    count = 0

    for wall in walls:
        if room.line_intersects_rectangle(p1[0], p1[1], p2[0], p2[1], wall):
            count += 1

    return count

