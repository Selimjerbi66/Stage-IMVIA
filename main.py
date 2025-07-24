import sys
from ast import literal_eval
from main_interface import *
from main_exec import *

def is_cameraset(file_path):
    """Check if the file is a cameraset.json type of file."""
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return False

    if "cameras" in data:
        if isinstance(data["cameras"], list):
            for camera in data["cameras"]:
                if not isinstance(camera, dict) or len(camera) != 1:
                    return False
                for cam_props in camera.values():
                    if not all(key in cam_props for key in ["x", "y", "orientation", "angle", "range"]):
                        return False
            return True
    return False


def is_sceneset(file_path):
    """Check if the file is a sceneset.json type of file."""
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return False

    if "room" in data:
        room = data["room"]
        if all(key in room for key in ["length", "width", "walls"]):
            if isinstance(room["walls"], list):
                for wall in room["walls"]:
                    if not isinstance(wall, dict) or len(wall) != 1:
                        return False
                    for wall_props in wall.values():
                        if not all(key in wall_props for key in ["x1", "y1", "x2", "y2", "thickness"]):
                            return False
            # Check for optional "zones of interest"
            if "zones of interest" in room:
                zones = room["zones of interest"]
                if not isinstance(zones, dict):
                    return False
                for zone in zones.values():
                    if not all(key in zone for key in ["x1", "y1", "x2", "y2"]):
                        return False

            return True
    return False


scene = "roomexp1.json"  # Default scene for case 3
cams = "surveillance1.json"  # Default cams for case 3

if len(sys.argv) == 1:
    interface(sys)
    sys.exit(0)

if len(sys.argv) >= 5 and sys.argv[1] == '--compare':
    scene_path = sys.argv[2]  # The scene file
    cams_list = sys.argv[3:]  # The list of camera files

    # Check if scene file is a JSON file
    if not scene_path.endswith('.json'):
        print("Error: The scene file must be a JSON file.")
        sys.exit(1)

    # Check if the scene file is valid
    if not is_sceneset(scene_path):
        print(f"Error: {scene_path} is not a valid sceneset file.")
        sys.exit(1)

    # Check if there are at least 2 camera files
    if len(cams_list) < 2:
        print("Error: You must provide at least two camera files for comparison.")
        sys.exit(1)

    # Validate each camera file
    for cam_path in cams_list:
        if not cam_path.endswith('.json'):
            print(f"Error: {cam_path} must be a JSON file.")
            sys.exit(1)
        if not is_cameraset(cam_path):
            print(f"Error: {cam_path} is not a valid cameraset file.")
            sys.exit(1)

    # Call the compare function
    compare(scene_path, cams_list)
    sys.exit(0)

if len(sys.argv) == 2 and sys.argv[1] == '--default':
    executor1(scene, cams)
    sys.exit(0)

if len(sys.argv) > 1:
    first_arg = sys.argv[1]

    # Check if the first argument is a JSON file
    if first_arg.endswith('.json'):
        # Now check if there is a second argument
        if len(sys.argv) == 3:
            cams_path = sys.argv[2]
            if cams_path.endswith('.json'):
                # Case 1: Valid scene and cams file
                if not is_sceneset(first_arg):
                    print(f"Error: {first_arg} is not a valid sceneset file.")
                    sys.exit(1)
                if not is_cameraset(cams_path):
                    print(f"Error: {cams_path} is not a valid cameraset file.")
                    sys.exit(1)
                executor1(first_arg, cams_path)
                sys.exit(0)
            else:
                # Case 2: Scene file followed by tuples
                tuples = []
                for arg in sys.argv[2:]:
                    try:
                        parsed_tuple = literal_eval(arg)
                        if isinstance(parsed_tuple, tuple):
                            tuples.append(parsed_tuple)
                        else:
                            raise ValueError(f"{arg} is not a valid tuple.")
                    except (ValueError, SyntaxError):
                        print(f"Error: {arg} is not a valid tuple format.")
                        sys.exit(1)
                # Execute with scene file and list of tuples
                executor2(first_arg, tuples)
                sys.exit(0)

        # If there are more than two arguments, check for tuples
        elif len(sys.argv) > 3:
            tuples = []
            for arg in sys.argv[2:]:
                try:
                    parsed_tuple = literal_eval(arg)
                    if isinstance(parsed_tuple, tuple):
                        tuples.append(parsed_tuple)
                    else:
                        raise ValueError(f"{arg} is not a valid tuple.")
                except (ValueError, SyntaxError):
                    print(f"Error: {arg} is not a valid tuple format.")
                    sys.exit(1)
            # Execute with scene file and list of tuples
            executor2(first_arg, tuples)
            sys.exit(0)

    else:
        # Check if all arguments are tuples for case 3
        tuples = []
        for arg in sys.argv[1:]:
            try:
                parsed_tuple = literal_eval(arg)
                if isinstance(parsed_tuple, tuple):
                    tuples.append(parsed_tuple)
                else:
                    raise ValueError(f"{arg} is not a valid tuple.")
            except (ValueError, SyntaxError):
                print(f"Error: {arg} is not a valid tuple format.")
                sys.exit(1)

        # Execute with default scene and tuples
        executor2(scene, tuples)
        sys.exit(0)

print("No valid command-line arguments provided.")
sys.exit(1)