from files.room_reader import *
from files.camera_reader import *
from mathematical.mathAlg import *
def setUpLab(matrix):
    # Create Wall objects using a list comprehension
    Walls = [Wall(wall_data[0], wall_data[1], wall_data[2], wall_data[3], wall_data[4], wall_data[5]) for wall_data in matrix[2]]
    
    # Create Zone objects from the matrix[3]
    Zones = [Zone(zone_data[0], zone_data[1], zone_data[2], zone_data[3], zone_data[4]) for zone_data in matrix[3]]
    
    # Create and return the Room object
    return Room(matrix[0], int(matrix[1][0]), int(matrix[1][1]), Walls, Zones)
def setUpCameras(matrix, Room):
    Cameras=[]
    test = True
    rejected_list = []
    for i in matrix:
        test, rejected_list =Room.compatibleCamera(Camera(i[0],i[1],i[2],i[3],i[4],i[5]), rejected_list)
        if test:
            Cameras.append(Camera(i[0], i[1], i[2], i[3], i[4], i[5], len(Cameras)))
        '''print(Camera(i[0],i[1],i[2],i[3],i[4],i[5]))'''
    '''if len(rejected_list) != 0:
        print("here is the list of rejected cameras due to their positions")
    for i in rejected_list:
        print(i.name, ' : (', i.x,',',i.y,')')'''
    return Cameras

'''
json_file_path = "labo.json"  # Replace with your JSON file path
result = process_room_file(json_file_path)
room = setUpLab(result)
cameras = setUpCameras(process_cameras_file("cameraexp.json"),room)
s=[]
for i in cameras:
    print(i)
    to_view = room.visible_points_by_camera(i)
    s.append((i.name,to_view))
    print(to_view)
print(s)
'''