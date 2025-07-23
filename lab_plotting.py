from lab_builder import *  # Ensure this module contains necessary functions and classes

def plotLab(room, cameras, viewable, ax):
    ax.clear()  # Nettoyage pour éviter des superpositions

    # Dessin des zones
    for zone in room.zones:
        zone_rectangle = patches.Rectangle(
            (zone.blc[0], zone.blc[1]),
            zone.length,
            zone.width,
            linewidth=1,
            edgecolor=hex_codes[4],
            facecolor=hex_codes[4]
        )
        ax.add_patch(zone_rectangle)
        ax.text(zone.blc[0], zone.blc[1], zone.name, ha='left', va='bottom', color='#20B2AA')

    # Dessin des murs
    for wall in room.walls:
        wall_rectangle = patches.Rectangle(
            (wall.xbl, wall.ybl),
            wall.length,
            wall.width,
            linewidth=1,
            edgecolor='000000',
            facecolor='000000'
        )
        ax.add_patch(wall_rectangle)

    # Points visibles
    points = []
    colors = []
    sizes = []

    for point, _ in viewable.items():
        x, y = point
        n = closeCam(point, viewable, cameras)
        color = hex_codes_new[n % len(hex_codes_new)] if zoned(room.zones, point) else hex_codes[n % len(hex_codes)]
        points.append((x, y))
        colors.append(color)
        sizes.append(1)

    points = np.array(points)
    if len(points) > 0:
        ax.scatter(points[:, 0], points[:, 1], color=colors, s=sizes)

    # Caméras
    camera_positions = [(cam.x, cam.y) for cam in cameras]
    camera_names = [cam.name for cam in cameras]

    if camera_positions:
        ax.scatter(*zip(*camera_positions), color='red', s=10)
        for (x, y), name in zip(camera_positions, camera_names):
            ax.text(x, y, name, fontsize=10, ha='center', va='bottom')

    # Configuration finale
    ax.set_xlim(-1, room.length + 1)
    ax.set_ylim(-1, room.width + 1)
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_title(room.name)

def plotConnectivity(room, camera_points, camera_proxi, ax):
    ax.clear()  # Nettoyer l'axe

    # Murs
    for wall in room.walls:
        wall_rectangle = patches.Rectangle(
            (wall.xbl, wall.ybl),
            wall.length,
            wall.width,
            linewidth=1,
            edgecolor='black',
            facecolor='black'
        )
        ax.add_patch(wall_rectangle)

    # Positions des caméras
    camera_positions = [(pt[0], pt[1]) for pt in camera_points.values()]
    ax.scatter(*zip(*camera_positions), color='red', s=50)

    # Liens de connectivité
    for camera_name, links in camera_proxi.items():
        for linked_camera, dist, eff_dist, obstacles in links:
            if dist <= eff_dist:
                pos1 = camera_points[camera_name]
                pos2 = camera_points[linked_camera]

                ax.plot([pos1[0], pos2[0]], [pos1[1], pos2[1]], color='blue', linestyle='--', alpha=0.5)

                mid_x = (pos1[0] + pos2[0]) / 2
                mid_y = (pos1[1] + pos2[1]) / 2
                annotation = f'Dist: {dist:.2f}, Eff: {eff_dist:.2f}, Obst: {obstacles}'
                ax.text(mid_x, mid_y, annotation, fontsize=8, ha='center', va='center', color='#FF00FF')

    ax.set_xlim(-1, room.length + 1)
    ax.set_ylim(-1, room.width + 1)
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_title(f'Connectivity Network Inside {room.name}')
