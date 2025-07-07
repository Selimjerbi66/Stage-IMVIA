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
def setUpCameras(matrix):
    Cameras=[]
    for i in matrix:
        Cameras.append(Camera(i[0],i[1],i[2],i[3],i[4],i[5]))
        print(Camera(i[0],i[1],i[2],i[3],i[4],i[5]))
    return Cameras