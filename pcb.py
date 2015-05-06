defaultplating=0.035
def hole(x,y,pinnr,ringwidth,diameter,plating=defaultplating):
    radius=diameter/2.0
    radius+=plating
    
    halfwidth=ringwidth/2.0
    radius+=halfwidth
    if pinnr==None:
        idpart=""
    else:
        idpart="id=\"connector%dpin\""%(pinnr,)
        
    return """<circle stroke-width="%(ringwidth)f" stroke="rgb(255, 191, 0)" fill="none" %(idpart)s cx="%(x)f" cy="%(y)f" r="%(radius)f"/>"""%dict(
                x=x,y=y,idpart=idpart,ringwidth=ringwidth,radius=radius
                    )


def pad(x,y,pinnr,xsize,ysize):
    if pinnr==None:
        idpart=""
    else:
        idpart="id=\"connector%dpin\""%(pinnr,)
    return """<rect  fill="rgb(255, 191, 0)" stroke="none" %(idpart)s x="%(x1)f" y="%(y1)f" width="%(width)f" height="%(height)f"/>"""%dict(
            idpart=idpart,
            x1=x,
            y1=y,
            width=xsize,
            height=ysize
        )
        
