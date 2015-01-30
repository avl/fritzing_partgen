name="GEN"
description="Generic 1-row component"

from pcb import hole

def gen_pcb(pin_names=[],pins=2,holediameter="0.7",ringwidth="0.4",pitch="2.54",nofrontring=None):

    pins=int(pins)
    for x in xrange(pins):
        pin_names.append("pin%d"%(x,))
    holediameter=float(holediameter)
    ringwidth=float(ringwidth)
    pitch=float(pitch)

    N=pins
    
       
    overall_w=N*pitch
    overall_h=holediameter+2.0*ringwidth
    xx=overall_w/2.0
    yy=overall_h/2.0
    
    x=overall_w/2.0
    y=overall_h/2.0
    
    x1=0.5*pitch
        
           
    header="""<?xml version='1.0' encoding='UTF-8'?>
<svg xmlns="http://www.w3.org/2000/svg" baseProfile="tiny" viewBox="0 0 %(w)f %(h)f" height="%(height_mm)fmm" width="%(width_mm)fmm" version="1.2">
    <desc>
        <referenceFile>unknown.svg</referenceFile>
    </desc>
    <desc >Fritzing footprint SVG</desc>    
    
    """%dict(h=overall_h,w=overall_w,height_mm=overall_h,width_mm=overall_w)
    
    silkscreen=("""
    <g  id="silkscreen">
    """)
 
    silkscreen+=("""
    </g>    
    """)
    
    
    print "Nofrontring:",nofrontring
    if nofrontring:
        print "Is true"
    if not nofrontring:
        print "Is false"
    copper_start="""
    <g  id="copper0">
    """
    if not nofrontring:
        copper_start+="""
            <g  id="copper1">
    """   
 
    copper_pads=[]
    
    
    for pin in xrange(N):

                        
        copper_pads.append(hole(
                pinnr=pin,
                x=x1+pitch*float(pin),
                y=yy,
                ringwidth=ringwidth,
                diameter=holediameter
                ))
 
    
    copper_end=""
    if not nofrontring:      
        copper_end="""
            </g>"""
    copper_end+="""
        </g>
"""
    if nofrontring:
        copper_end+="""<g  id="copper1">"""
        
        for pin in xrange(N):

                            
            copper_end+=hole(
                    pinnr=pin,
                    x=x1+pitch*float(pin),
                    y=yy,
                    ringwidth=0.0,
                    diameter=holediameter
                    )
     
            
        copper_end+="""</g>"""
        
    
    footer="""
</svg>
"""    
    out=header+silkscreen+copper_start+"\n".join(copper_pads)+copper_end+footer
    return out,False
    
    
def javascript():
   return """ 
function on_GEN()
{
    add_row('Pins:','  <input type="text" name="pins" onchange="onpreview()" />');        
    add_row('Hole diameter:',' <input type="text" name="holediameter" onchange="onpreview()" /> mm');        
    add_row('Ring width:','  <input type="text" name="ringwidth" onchange="onpreview()" /> mm');        
    add_row('Pitch:',' <input type="text" name="pitch" onchange="onpreview()" /> mm');        
    add_row('No front ring:',' <input type="checkbox" name="nofrontring" onchange="onpreview()" />');        

}
"""    
    
    
    
    
if __name__=='__main__':
    f=open("test_pcb.svg","w")
    f.write(gen_pcb(4))    
    f.close()
    
    
