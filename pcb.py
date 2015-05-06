def hole(x,y,pinnr,ringwidth,diameter,plating=0.035):
    radius=diameter/2.0
    radius+=plating
    
    halfwidth=ringwidth/2.0
    radius+=halfwidth
        
    return """<circle stroke-width="%(ringwidth)f" stroke="rgb(255, 191, 0)" fill="none" id="connector%(nr)dpin" cx="%(x)f" cy="%(y)f" r="%(radius)f"/>"""%dict(
                x=x,y=y,nr=pinnr,ringwidth=ringwidth,radius=radius
                    )


def pad(x,y,pinnr,xsize,ysize):
    return """<rect  fill="rgb(255, 191, 0)" stroke="none" id="connector%(pin)dpin" x="%(x1)f" y="%(y1)f" width="%(width)f" height="%(height)f"/>"""%dict(
            pin=pinnr,
            x1=x,
            y1=y,
            width=xsize,
            height=ysize
        )
        
