import json

def process_room_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    room_data = data['room']
    length = room_data['length']
    width = room_data['width']
    walls = room_data['walls']

    # Create the desired output format
    output = [
        "room",
        [length, width],
        []
    ]

    for wall in walls:
        for wall_key, coordinates in wall.items():
            output[2].append([
                wall_key,
                coordinates['x1'],
                coordinates['y1'],
                coordinates['x2'],
                coordinates['y2'],
                coordinates['thickness']
            ])
    
    return output
'''
# Example usage
json_file_path = "roomexp.json"  # Replace with your JSON file path
result = process_room_file(json_file_path)
print(result)
'''