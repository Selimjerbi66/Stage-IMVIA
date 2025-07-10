from files.room_reader import *
from files.camera_reader import *
from mathematical.mathAlg import *
def setUpLab(matrix):
    Walls=[]
    x=0
    for i in matrix[2]:
        print (x)
        Walls.append(Wall(i[0],i[1],i[2],i[3],i[4],i[5]))
        print(Wall(i[0],i[1],i[2],i[3],i[4],i[5]))
        x+=1
    Room(matrix[0],matrix[1][0],matrix[1][1],Walls)
    print(Room(matrix[0],int(matrix[1][0]),int(matrix[1][1]),Walls))
    return Room(matrix[0],int(matrix[1][0]),int(matrix[1][1]),Walls)
def setUpCameras(matrix, Room):
    Cameras=[]
    test = True
    rejected_list = []
    for i in matrix:
        test, rejected_list =Room.compatibleCamera(Camera(i[0],i[1],i[2],i[3],i[4],i[5]), rejected_list)
        if test:
            Cameras.append(Camera(i[0], i[1], i[2], i[3], i[4], i[5]))
        print(Camera(i[0],i[1],i[2],i[3],i[4],i[5]))
    print("here is the list of rejected cameras due to their positions")
    for i in rejected_list:
        print(i.name, ' : (', i.x,',',i.y,')')
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