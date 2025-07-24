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

def compare(scene_path, cams_paths_list):
    """Compare camera sets based on various metrics."""
    results = {}  # Initialize an empty dictionary to store results

    for cam_path in cams_paths_list:
        room = setUpLab(process_room_file(scene_path))
        cameras = setUpCameras(process_cameras_file(cam_path), room)
        viewable = room.point_matrix(cameras)
        zones = room.zones
        data = zoneViewer(zones, viewable)
        networks, _, _ = ConnectedCams(room, cameras, 250, 10)

        print('')  # Print a blank line for separation
        results[cam_path] = brief_results(room, viewable, data, networks)

    # Initialize variables to track the best results
    best_coverage = -1
    best_redundancy = -1
    best_zone_avg = -1
    best_network_count = float('inf')  # Start with infinity for smallest comparison
    best_coverage_cams = []
    best_redundancy_cams = []
    best_zone_avg_cams = []
    best_network_count_cams = []

    # Compare results after the loop
    for cam_path, metrics in results.items():
        coverage, redundancy, zone_avg, network_count = metrics

        # Compare coverage
        if coverage is not None:
            if coverage > best_coverage:
                best_coverage = coverage
                best_coverage_cams = [cam_path]
            elif coverage == best_coverage:
                best_coverage_cams.append(cam_path)

        # Compare redundancy
        if redundancy is not None:
            if redundancy > best_redundancy:
                best_redundancy = redundancy
                best_redundancy_cams = [cam_path]
            elif redundancy == best_redundancy:
                best_redundancy_cams.append(cam_path)

        # Compare zone average
        if zone_avg is not None:
            if zone_avg > best_zone_avg:
                best_zone_avg = zone_avg
                best_zone_avg_cams = [cam_path]
            elif zone_avg == best_zone_avg:
                best_zone_avg_cams.append(cam_path)

        # Compare network count
        if network_count is not None:
            if network_count < best_network_count:  # Looking for the smallest
                best_network_count = network_count
                best_network_count_cams = [cam_path]
            elif network_count == best_network_count:
                best_network_count_cams.append(cam_path)

    # Print best results
    coverage_cams_str = ', '.join(best_coverage_cams)
    redundancy_cams_str = ', '.join(best_redundancy_cams)
    zone_avg_cams_str = ', '.join(best_zone_avg_cams)
    network_count_cams_str = ', '.join(best_network_count_cams)

    print(f'The best camera set in terms of coverage is {coverage_cams_str} with a coverage of {best_coverage:.2f}%')
    print(f'The best camera set in terms of redundancy is {redundancy_cams_str} with a redundancy of {best_redundancy:.2f}%')
    print(f'The best camera set in terms of zone average is {zone_avg_cams_str} with an average of {best_zone_avg:.2f}%')
    
    network_word = 'network' if best_network_count == 1 else 'networks'
    print(f'The best camera set in terms of network count is {network_count_cams_str} with only {best_network_count} {network_word}')

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

def brief_results(room, viewable, data, networks):
    """Assess the information and return a tuple of results."""
    try:
        total_points = room.points  # Accessing room's points attribute
    except Exception as e:
        print(f"Error in total points: {e}")
        return None  # Return None if there's an error

    try:
        points = list(viewable.keys())  # Accessing keys from viewable dict
        coverage = visual_coverage(total_points, points)
    except Exception as e:
        print(f"Error calculating coverage: {e}")
        coverage = None  # Default to None if there's an error

    try:
        redundancy_values = list(viewable.values())  # Accessing values from viewable dict
        red = redundancy(redundancy_values)
    except Exception as e:
        print(f"Error calculating redundancy: {e}")
        red = None  # Default to None if there's an error

    try:
        zone_avg = zonepercent(data.values())  # Accessing values from data
    except Exception as e:
        print(f"Error calculating zone average: {e}")
        zone_avg = None  # Default to None if there's an error

    try:
        network_count = networks_number(networks)  # Accessing networks list
    except Exception as e:
        print(f"Error counting networks: {e}")
        network_count = None  # Default to None if there's an error

    return (coverage, red, zone_avg, network_count)  # Return results as a tuple


def print_brief_results(room, viewable, data, networks):
    """Call brief_results and print the results."""
    results = brief_results(room, viewable, data, networks)

    if results is not None:
        coverage, red, zone_avg, network_count = results
        
        if coverage is not None:
            print(f"Visual Coverage: {coverage:.2f}%")
        if red is not None:
            print(f"Redundancy: {red:.2f}%")
        if zone_avg is not None:
            print(f"Zone Average: {zone_avg:.2f}%")
        if network_count is not None:
            print(f"Number of Networks: {network_count}")