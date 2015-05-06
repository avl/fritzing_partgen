from pcb import hole

name="Spark"
description="Spark Gap"

def javascript():
   return """ 
function on_Spark()
{
    add_row('Width:','  <input type="text" name="width" onchange="onpreview()" value="1" /> mm');        
    add_row('Height:','  <input type="text" name="height" onchange="onpreview()" value="1" /> mm');        
    add_row('Gap:',' <input type="text" name="gap" onchange="onpreview()" value="0.2" /> mm');
}
"""    

def gen_pcb(pin_names,**options):
    width=float(options['width'])
    height=float(options['height'])
    gap=float(options['gap'])

    pin_names.append("sig");
    pin_names.append("GND");
       
    overall_x=width
    overall_y=height
            
           
    header="""<?xml version='1.0' encoding='UTF-8'?>
<svg xmlns="http://www.w3.org/2000/svg" baseProfile="tiny" viewBox="0 0 %(w)f %(h)f" height="%(height_mm)fmm" width="%(width_mm)fmm" version="1.2">
    <desc>
        <referenceFile>unknown.svg</referenceFile>
    </desc>
    <desc >Fritzing footprint SVG</desc>    
    
    """%dict(w=overall_x,h=overall_y,height_mm=overall_y,width_mm=overall_x)

    
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
    silkscreen+=("""
    </g>    
    """)
    
    
    
    copper_start="""
        <g  id="copper1">
"""   
    copper_pads=[]
    
    

   
#       <rect  fill="rgb(255, 191, 0)" stroke="none" id="connector%(pin)dpin" x="%(x1)f" y="%(y1)f" width="%(w)f" height="%(h)f"/>   
    copper_pads.append("""
      <path fill="rgb(255, 191, 0)" stroke="none" id="connector%(pin)dpin" 
        d="M%(x1)f %(y1)f L%(w)f %(y1)f L%(w)f %(h)f L%(a3)f %(h)f L%(a2)f %(hgap)f L%(a1)f %(h)f L0 %(h)f Z" />
   
"""%dict(
        x1=0,
        y1=0,
        w=width,
        h=height/2.0-gap,
        pin=0,
        a3=width/2.0+gap,
        a2=width/2.0,
        a1=width/2.0-gap,
        hgap=height/2.0-gap/2.0
    ))

    copper_pads.append("""
   
      <path fill="rgb(255, 191, 0)" stroke="none" id="connector%(pin)dpin" 
        d="M%(x1)f %(y2)f L%(x2)f %(y2)f L%(x2)f %(y1)f L%(a3)f %(y1)f L%(a2)f %(hgap)f L%(a1)f %(y1)f L0 %(y1)f Z" />
   
"""%dict(
        x1=0,
        y1=height/2.0+gap,
        x2=width,
        y2=height,
        a3=width/2.0+gap,
        a2=width/2.0,
        a1=width/2.0-gap,
        hgap=height/2.0+gap/2.0,
        pin=1,
    ))

      
    copper_end="""
    </g>
"""
    
    footer="""
</svg>
"""    
    out=header+silkscreen+copper_start+"\n".join(copper_pads)+copper_end+footer
    return out,False
    
    
    
    
    
    
    
    
if __name__=='__main__':
    f=open("test_pcb_sparkgap.svg","w")
    names=[]
    f.write(gen_pcb(names,width=2.0,height=2.0,gap=0.2)[0])
    print "Names:",names
    f.close()
    
    
