name="COBLED"
description="Generic COB LED"

def gen_pcb(pad_dist_x,pad_dist_y,silk_size_x,silk_size_y,hole_diam,pin_names):
    print "Silk x:",silk_size_x
    pin_names.extend(["plus","minus"])
    silk_size_x=float(silk_size_x)
    silk_size_y=float(silk_size_y)
    pad_dist_x=float(pad_dist_x)
    pad_dist_y=float(pad_dist_y)
    hole_diam=float(hole_diam)

    overall_x=silk_size_x
    overall_y=silk_size_y
    
    xx=overall_x/2.0
    yy=overall_y/2.0
    
    silk_t=0.25
            
           
    header="""<?xml version='1.0' encoding='UTF-8'?>
<svg xmlns="http://www.w3.org/2000/svg" baseProfile="tiny" viewBox="0 0 %(w)f %(h)f" height="%(height_mm)fmm" width="%(width_mm)fmm" version="1.2">
    <desc>
        <referenceFile>unknown.svg</referenceFile>
    </desc>
    <desc >Fritzing footprint SVG</desc>    
    
    """%dict(h=overall_y,w=overall_x,height_mm=overall_y,width_mm=overall_x)

    
    silk_points=[    
            (0,0),
            (overall_x,0),
            (overall_x,overall_y),
            (0,overall_y),
            (0,0)
    ]
    
    silkscreen=("""
    <g  id="silkscreen">
    """)
    
    for a,b in zip(silk_points,silk_points[1:]):
        silkscreen+="""<line fill="none" stroke="white" stroke-width="%f" x1="%f" y1="%f" x2="%f" y2="%f"/>"""%(
            silk_t,a[0],a[1],b[0],b[1])
        silkscreen+="\n"


    px=-pad_dist_x/2.0+xx+3.5
    py=-pad_dist_y/2.0+yy-0.5
    s=0.75
    
    silkscreen+="""<line fill="none" stroke="white" stroke-width="%f" x1="%f" y1="%f" x2="%f" y2="%f"/>"""%(
        silk_t*0.7,px-s,py,px+s,py)
    silkscreen+="""<line fill="none" stroke="white" stroke-width="%f" x1="%f" y1="%f" x2="%f" y2="%f"/>"""%(
        silk_t*0.7,px,py-s,px,py+s)

    silkscreen+=("""<circle stroke="white" fill="none" stroke-width="0.25" id="noconn" cx="%(x)f" cy="%(y)f" r="%(r)f"/>"""%dict(
        x=xx,y=yy,r=hole_diam/2.0+0.125
            ))
             
    silkscreen+=("""
    </g>    
    """)
    
    
    
    copper_start="""
    <g  id="copper0">
        <g  id="copper1">
"""   
    copper_pads=[]
    
    copper_pads.append("""<circle stroke="rgb(255, 191, 0)" fill="none" stroke-width="0" id="noconn" cx="%(x)f" cy="%(y)f" r="%(r)f"/>"""%dict(
        x=xx,y=yy,r=hole_diam/2.0
            ))
    
        
    copper_pads.append("""<circle stroke="rgb(255, 191, 0)" fill="none" id="connector0pin" cx="%(x)f" cy="%(y)f" r="1.5"/>"""%dict(
        x=-pad_dist_x/2.0+xx,y=-pad_dist_y/2.0+yy
            ))
    copper_pads.append("""<circle stroke="rgb(255, 191, 0)" fill="none" id="connector1pin" cx="%(x)f" cy="%(y)f" r="1.5"/>"""%dict(
        x=+pad_dist_x/2.0+xx,y=+pad_dist_y/2.0+yy
            ))
                   
      
    copper_end="""
        </g>
    </g>
"""
    
    footer="""
</svg>
"""    
    out=header+silkscreen+copper_start+"\n".join(copper_pads)+copper_end+footer
    return out,False
    
    
    
def javascript():
    return """
function on_COBLED()
{
    add_row('Width:','  <input type="text" name="silk_size_x" onchange="onpreview()" value="18"/> mm');        
    add_row('Height:',' <input type="text" name="silk_size_y" onchange="onpreview()" value="18"/> mm');        
    add_row('Pad spacing X:','  <input type="text" name="pad_dist_x" onchange="onpreview()" value="14.6"/> mm');        
    add_row('Pad spacing Y:',' <input type="text" name="pad_dist_y" onchange="onpreview()" value="14.6" /> mm');        
    add_row('Hole diam:',' <input type="text" name="hole_diam" onchange="onpreview()" value="15.25"/> mm');        

    onpreview();
}
"""

    
    
    
    
if __name__=='__main__':
    f=open("test_pcb_cobled.svg","w")
    f.write(gen_pcb(14.6,14.6,18.5,18.5,15.25))
    f.close()
    
    
