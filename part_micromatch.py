name="AMPMM"
description="AMP Micro-Match SMD Female"
def gen_pcb(pin_names,pins):
    
    pins=int(pins)
    
    centers=[]
    
    padlength=3.5
    padwidth=1.5
    
    cx=padwidth/2.0
    for x in xrange(pins):
        cy=padlength/2.0
        if x%2==1:
            cy+=padlength+1.5
        centers.append((cx,cy))
        cx+=1.27
        pin_names.append("pin%d"%(x,))    
    
        
    
    overall_x=max([x for x,y in centers])+padwidth/2.0
    overall_y=max([y for x,y in centers])+padlength/2.0

    silk_t=0.2
            
           
    header="""<?xml version='1.0' encoding='UTF-8'?>
<svg xmlns="http://www.w3.org/2000/svg" baseProfile="tiny" viewBox="0 0 %(w)f %(h)f" height="%(height_mm)fmm" width="%(width_mm)fmm" version="1.2">
    <desc>
        <referenceFile>unknown.svg</referenceFile>
    </desc>
    <desc >Fritzing footprint SVG</desc>    
    
    """%dict(w=overall_x,h=overall_y,height_mm=overall_y,width_mm=overall_x)

    
   
    silkscreen=("""
    <g  id="silkscreen">
    """)
                   
    silkscreen+=("""
    </g>    
    """)
    
    
    
    copper_start="""
        <g  id="copper1">
"""   
    copper_pads=[]

    
    for idx,(x,y) in enumerate(centers):    
        copper_pads.append("""<rect  fill="rgb(255, 191, 0)" stroke="none" id="connector%(pin)dpin" x="%(x1)f" y="%(y1)f" width="%(width)f" height="%(height)f"/>"""%dict(
                pin=idx,
                x1=x-padwidth/2.0,
                y1=y-padlength/2.0,
                width=padwidth,
                height=padlength
            ))




    copper_end="""
    </g>
"""
    
    footer="""
</svg>
"""    
    out=header+silkscreen+copper_start+"\n".join(copper_pads)+copper_end+footer
    return out,True
    
    
def javascript():
   return """ 
function on_AMPMM()
{
    add_row('Pins:','  <input type="text" name="pins" onchange="onpreview()" />');        

}
"""    
    

    
    
    
    
    
if __name__=='__main__':
    f=open("test_pcb_emifil.svg","w")
    names=[]
    f.write(gen_pcb(names))
    print "Names:",names
    f.close()
    
    
