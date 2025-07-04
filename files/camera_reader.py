import json

def process_cameras_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    cameras = data['cameras']
    output = []

    for camera in cameras:
        for camera_key, attributes in camera.items():
            output.append([
                camera_key,
                attributes['x'],
                attributes['y'],
                attributes['orientation'],
                attributes['angle'],
                attributes['reach']
            ])

    return output
'''
# Example usage
json_file_path = "cameraexp.json"  # Replace with your JSON file path
result = process_cameras_file(json_file_path)
print(result)
'''