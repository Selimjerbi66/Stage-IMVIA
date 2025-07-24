from main_interface import *
from main_exec import *
import sys
from ast import literal_eval

scene = "roomexp1.json"  # Default scene for case 3
cams = "surveillance1.json"  # Default cams for case 3

if len(sys.argv) == 1:
    interface(sys)
    sys.exit(0)
if len(sys.argv) >= 5 and sys.argv[1] == '--compare':
    # The first argument is --compare, and we need at least 4 more (scene and 2+ cameras)
    scene_path = sys.argv[2]  # The scene file
    cams_list = sys.argv[3:]  # The list of camera files

    # Check if scene file is a JSON file
    if not scene_path.endswith('.json'):
        print("Error: The scene file must be a JSON file.")
        sys.exit(1)

    # Check if there are at least 2 camera files
    if len(cams_list) < 2:
        print("Error: You must provide at least two camera files for comparison.")
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