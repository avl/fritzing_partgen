name="CAP"
description="Generic capacitor"

from pcb import hole

def javascript():
   return """ 
function on_CAP()
{
    add_row('Pitch:','  <input type="text" name="pitch" onchange="onpreview()" /> mm');        
    add_row('Offset:',' <input type="text" name="offset" onchange="onpreview()" /> mm');        
    add_row('Case Diameter:','  <input type="text" name="diameter" onchange="onpreview()" /> mm');        
    add_row('Hole ring width:',' <input type="text" name="ringwidth" onchange="onpreview()" /> mm');        
    add_row('Hole diameter:',' <input type="text" name="holediameter" onchange="onpreview()" /> mm');        

}
"""    
    

def gen_pcb(pin_names=[],**options):

    pin_names.append("minus")
    pin_names.append("plus")
    pitch=float(options['pitch'])
    offset=float(options['offset'])
    diameter=float(options['diameter'])
    ringwidth=float(options['ringwidth'])
    holediameter=float(options['holediameter'])

    
    
       
    overall_w=diameter+0.125
    
    y1a=-pitch/2.0-holediameter/2.0-ringwidth
    y2a=+pitch/2.0+holediameter/2.0+ringwidth
    y1b=-diameter/2.0 + offset - 0.125
    y2b=+diameter/2.0 + offset + 0.125
    
    y1=min(y1a,y1b)
    y2=max(y2a,y2b)
        
    overall_h=y2-y1
    
    xx=overall_w/2.0
    yy=-y1
            
           
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
     
    silkscreen+=("""<circle stroke="white" fill="none" cx="%(x)f" cy="%(y)f" r="%(radius)f" stroke-width="0.25"/>"""%dict(
        x=xx,y=offset+yy,radius=diameter/2.0
            ))
    silkscreen+=("""
    </g>    
    """)
    
    
    
    copper_start="""
    <g  id="copper0">
        <g  id="copper1">
"""   
    copper_pads=[]
    
    

                    
    copper_pads.append(hole(
            pinnr=0,
            x=xx,
            y=pitch/2.0+yy,
            ringwidth=ringwidth,
            diameter=holediameter
            ))
    
                    
    copper_pads.append(hole(
            pinnr=1,
            x=xx,
            y=-pitch/2.0+yy,
            ringwidth=ringwidth,
            diameter=holediameter
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
    
    
    
    
    
    
    
    
if __name__=='__main__':
    f=open("test_pcb.svg","w")
    f.write(gen_pcb(4))    
    f.close()
    
    
