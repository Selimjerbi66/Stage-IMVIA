from files.room_reader import *
from files.camera_reader import *
from mathematical.mathAlg import *
def setUpLab(matrix):
    Walls=[]
    x=0
    for i in matrix[2]:
        print (x)
        Walls.append(Wall(i[0],i[1],i[2],i[3],i[4]))
        print(Wall(i[0],i[1],i[2],i[3],i[4]))
        x+=1
    Room(matrix[0],matrix[1][0],matrix[1][1],Walls)
    print(Room(matrix[0],int(matrix[1][0]),int(matrix[1][1]),Walls))
    return Room
def setUpCameras(matrix):
    Cameras=[]
    for i in matrix:
        Cameras.append(Camera(i[0],i[1],i[2],i[3],i[4],i[5]))
        print(Camera(i[0],i[1],i[2],i[3],i[4],i[5]))
def buildLab(room_json_path, cameras_json_path):
    room_list = process_room_file(room_json_path)
    cameras_list = process_cameras_file(cameras_json_path)
    setUpLab(room_list)
    setUpCameras(cameras_list)

buildLab("roomexp.json","files\cameraexp.json")