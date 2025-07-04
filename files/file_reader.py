import json

def convert_json_to_list_of_lists(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)

    result = []

    for room, details in data.items():
        room_list = [room]
        
        # Extract length and width as integers
        size_info = details[0]
        room_list.append([int(size_info['length']), int(size_info['width'])])
        
        # Extract walls
        walls_list = []
        walls = details[1]['walls']
        for wall in walls:
            for wall_name, coordinates in wall.items():
                wall_data = [wall_name]
                wall_data.extend(int(coordinates[0][key]) for key in ['x1', 'y1', 'x2', 'y2'])  # Convert to int
                walls_list.append(wall_data)
        room_list.append(walls_list)
        
        # Extract cameras
        cameras_list = []
        cameras = details[2]['cameras']
        for camera in cameras:
            for camera_name, attributes in camera.items():
                camera_data = [camera_name]
                camera_data.extend(int(attributes[0][key]) for key in ['x', 'y', 'orientation', 'angle', 'reach'])  # Convert to int
                cameras_list.append(camera_data)
        room_list.append(cameras_list)
        
        result.append(room_list)

    return result
'''
# Example usage
json_file_path = 'files\lab.json'
converted_data = convert_json_to_list_of_lists(json_file_path)
print(json.dumps(converted_data, indent=4))
'''