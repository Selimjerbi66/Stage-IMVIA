import json

def process_room_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    room_data = data['room']
    length = int(room_data['length'])  # Convert length to int
    width = int(room_data['width'])    # Convert width to int
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
                int(coordinates['x1']),         # Convert x1 to int
                int(coordinates['y1']),         # Convert y1 to int
                int(coordinates['x2']),         # Convert x2 to int
                int(coordinates['y2']),         # Convert y2 to int
                int(coordinates['thickness'])    # Convert thickness to int
            ])
    
    return output

'''
# Example usage
json_file_path = "roomexp.json"  # Replace with your JSON file path
result = process_room_file(json_file_path)
print(result)
'''