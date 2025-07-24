from mathematical.mathAlg import *
from lab_builder import *
from connectivity import *
from briefing import *

def executor3 (room, cameras):
    viewable = room.point_matrix(cameras)
    zones = room.zones
    data = zoneViewer(zones, viewable)
    networks, _, _ = ConnectedCams(room, cameras, 250, 10)
    print('''
''')
    print_brief_results(room, viewable, data, networks)


def executor1(scene_path, cams_path):
    print(scene_path," and", cams_path)

    room = setUpLab(process_room_file(scene_path))
    cameras = setUpCameras(process_cameras_file(cams_path), room)
    executor3(room, cameras)


def executor2(scene, tuples):
    print(scene," and ", tuples)
    room = setUpLab(process_room_file(scene))
    cameras = setUpCameras(normalized_cams(tuples), room)
    executor3(room, cameras)


def default_cam(camera_tuple):
    camera_name, x, y, orientation = camera_tuple
    default_angle = 60
    default_range = 250
    return (camera_name, x, y, orientation, default_angle, default_range)

def is_valid_format(tn):
    return isinstance(tn[0], str) and all(isinstance(i, int) for i in tn[1:])

def normalized_cams(cams_list):
    output = []
    
    for tn in cams_list:
        try:
            if len(tn) == 4:
                if is_valid_format(tn):
                    ln = list(default_cam(tn))
                else:
                    raise ValueError(f"Invalid format for tuple: {tn}")

            elif len(tn) == 6:
                if is_valid_format(tn):
                    ln = list(tn)
                else:
                    raise ValueError(f"Invalid format for tuple: {tn}")

            else:
                raise ValueError(f"Invalid tuple length: {tn}")

            output.append(ln)

        except (ValueError, TypeError) as e:
            print(f"Error processing tuple {tn}: {e}")

    return output

def print_brief_results(room, viewable, data, networks):
    """Calculate and display the results using the imported functions."""
    try:
        total_points = room.points  # Accessing room's points attribute
    except Exception as e:
        print(f"Error in total points: {e}")
    else:
        try:
            points = list(viewable.keys())  # Accessing keys from viewable dict
            coverage = visual_coverage(total_points, points)
            print(f"Visual Coverage: {coverage:.2f}%")
        except Exception as e:
            print(f"Error calculating coverage: {e}")

    try:
        redundancy_values = list(viewable.values())  # Accessing values from viewable dict
        red = redundancy(redundancy_values)
        print(f"Redundancy: {red:.2f}%")
    except Exception as e:
        print(f"Error calculating redundancy: {e}")

    try:
        zone_avg = zonepercent(data.values())  # Accessing values from data
        print(f"Zone Average: {zone_avg:.2f}%")
    except Exception as e:
        print(f"Error calculating zone average: {e}")

    try:
        network_count = networks_number(networks)  # Accessing networks list
        print(f"Number of Networks: {network_count}")
    except Exception as e:
        print(f"Error counting networks: {e}")