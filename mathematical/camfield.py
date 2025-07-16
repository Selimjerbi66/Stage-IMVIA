def outlineView(viewlist):
    newlist=[]
    for p in viewlist:
        if not( (p[0],p[1]-1) in viewlist and (p[0],p[1]) in viewlist):
            newlist.append(p)
    return(newlist)
def camViewer(room, cameras):
    s=[]
    for i in cameras:
        to_view = room.visible_points_by_camera(i)
        s.append((i.name,to_view))
        '''print(s)'''
    return (s)
def zoneViewer(zones, matrix):
    data=dict()
    for zone in zones:
        data[zone.name]=zone.visibility_rate(matrix)
    return data