import json

def process_cameras_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    cameras = data['cameras']
    output = []

    for camera in cameras:
        for camera_key, attributes in camera.items():
            try:
                output.append([
                    camera_key,
                    int(attributes['x']),
                    int(attributes['y']),
                    int(attributes['orientation']),  # Convert orientation to int
                    int(attributes['angle']),
                    int(attributes['range'])
                ])
            except (ValueError, KeyError) as e:
                print(f"Error processing camera {camera_key}: {e}")

    return output
'''
# Example usage
json_file_path = "cameraexp.json"  # Replace with your JSON file path
result = process_cameras_file(json_file_path)
print(result)
'''