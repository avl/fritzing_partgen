def hole(x,y,pinnr,ringwidth,diameter,plating=0.035):
    radius=diameter/2.0
    radius+=plating
    
    halfwidth=ringwidth/2.0
    radius+=halfwidth
        
    return """<circle stroke-width="%(ringwidth)f" stroke="rgb(255, 191, 0)" fill="none" id="connector%(nr)dpin" cx="%(x)f" cy="%(y)f" r="%(radius)f"/>"""%dict(
                x=x,y=y,nr=pinnr,ringwidth=ringwidth,radius=radius
                    )

