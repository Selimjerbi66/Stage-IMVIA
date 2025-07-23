def visual_coverage(total_points, points):#total_points is self.room.points and points is list(self.viewable.keys())
    """Calculate the visual coverage ratio."""
    return (float(len(points)) / len(total_points))*100 if total_points else 0

def redundancy(values):#self.viewable.values
    """Calculate the redundancy percentage of camera coverage."""
    if not values:  # Check if values is empty
        return 0

    total_cameras = len(values)
    redundant_cameras = float(sum(1 for camera_dict in values if len(camera_dict['cameras']) > 1))
    
    return (redundant_cameras / total_cameras) * 100

def zonepercent(values):#self.data.values()
    """Calculate the average percentage of visibility in zones."""
    if not values:  # Check if values is empty
        return 0
    return (sum(values) / len(values))*100

def networks_number(networks):#self.networks is a list
    """Return the total number of networks."""
    return len(networks)