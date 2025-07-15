import json

def process_room_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Find the first key in the data dictionary (assuming only one key for the room)
    room_key = next(iter(data))
    room_data = data[room_key]
    
    length = int(room_data['length'])  # Convert length to int
    width = int(room_data['width'])    # Convert width to int
    walls = room_data['walls']
    zones = room_data.get("zones of interest", {})  # Get zones of interest

    # Create the desired output format
    output = [
        room_key,                       # Use the dynamic room key
        [length, width],
        [],
        []
    ]

    # Process walls
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
    
    # Process zones of interest
    for zone_key, coordinates in zones.items():
        output[3].append([
            zone_key,
            int(coordinates['x1']),         # Convert x1 to int
            int(coordinates['y1']),         # Convert y1 to int
            int(coordinates['x2']),         # Convert x2 to int
            int(coordinates['y2'])          # Convert y2 to int
        ])

    return output
'''
# Example usage
json_file_path = "roomexp.json"  # Replace with your JSON file path
result = process_room_file(json_file_path)
print(result)
'''