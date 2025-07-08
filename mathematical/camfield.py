def outlineView(viewlist):
    newlist=[]
    for p in viewlist:
        if not( (p[0],p[1]-1) in viewlist and (p[0],p[1]) in viewlist):
            newlist.append(p)
    return(newlist)
