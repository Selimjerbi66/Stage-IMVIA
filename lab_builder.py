from mathematical.mathAlg import *
from files.file_reader import *
def buildLab(matrix):
    rooms=[]
    for room in matrix:
        Walls=[]
        Cameras=[]
        for i in room[2]:
            Walls.append(Wall(i[0],i[1],i[2],i[3],i[4]))
            print(Wall(i[0],i[1],i[2],i[3],i[4]))
        for i in room[3]:
            Cameras.append(Camera(i[0],i[1],i[2],i[3],i[4],i[5]))
            print(Camera(i[0],i[1],i[2],i[3],i[4],i[5]))
        rooms.append(Room(room[0],room[1][0],room[1][1],Walls,Cameras))
        print(Room(room[0],room[1][0],room[1][1],Walls,Cameras))
'''
json_file_path = 'files\lab.json'
converted_data = convert_json_to_list_of_lists(json_file_path)
buildLab(converted_data)
'''