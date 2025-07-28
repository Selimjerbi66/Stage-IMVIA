import sys
from ast import literal_eval
from main_interface import *
from main_exec import *

scene = "roomexp1.json"  # Default scene for case 3
cams = "surveillance1.json"  # Default cams for case 3

if len(sys.argv) == 1:
    interface(sys)
    sys.exit(0)

if len(sys.argv) == 5 and sys.argv[1] == '--compare' and sys.argv[4].isnumeric():
    scene_path = sys.argv[2]
    cams_path = sys.argv[3]

    # Check if the scene_path is a valid sceneset file
    if not is_sceneset(scene_path):
        print(f"Error: {scene_path} is not a valid sceneset file.")
        sys.exit(1)

    # Check if the cams_path is a .uri file
    if not cams_path.endswith('.uri'):
        print(f"Error: {cams_path} is not a .uri file.")
        sys.exit(1)

    # Read camera set files
    with open(cams_path, 'r') as file:
        lines = [line.strip() for line in file.readlines()]

    for line in lines:
        if not line.endswith('.json'):
            print(f"Error: {line} does not end with .json.")
            sys.exit(1)
        if not is_cameraset(line):
            print(f"Error: {line} is not a valid camera set file.")
            sys.exit(1)

    # Call compare1 with the scene_path and the list of camera sets
    index = sys.argv[4]
    compare1(scene_path, lines, index)
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