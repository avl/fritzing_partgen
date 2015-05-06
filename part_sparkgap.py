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

 
"""

def gen_pcb(pin_names,**options):
    width=float(options['width'])
    height=float(options['height'])
    gap=float(options['gap'])

    pin_names.append("sig");
    pin_names.append("GND");
       
    border=min(0.75+min(width,height)*0.1,min(width,height)*0.25)
    overall_x=width+border*2
    overall_y=height+border*2
            
           
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
    
    silk_t=0.5
    silkscreen=("""
    <g id="silkscreen">
    """)               
    for a,b in zip(silk_points,silk_points[1:]):
        silkscreen+="""<line fill="none" stroke="white" stroke-width="%f" x1="%f" y1="%f" x2="%f" y2="%f"/>"""%(
            silk_t,a[0],a[1],b[0],b[1])
        silkscreen+="\n"
    
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
        d="M%(x1)f %(y1)f L%(w)f %(y1)f L%(w)f %(h)f L%(a3)f %(h)f L%(a2)f %(hgap)f L%(a1)f %(h)f L%(x1)f %(h)f Z" />
   
"""%dict(
        x1=border,
        y1=border,
        w=width+border,
        h=height/2.0-gap+border,
        pin=0,
        a3=width/2.0+gap+border,
        a2=width/2.0+border,
        a1=width/2.0-gap+border,
        hgap=height/2.0-gap/2.0+border
    ))

    copper_pads.append("""
   
      <path fill="rgb(255, 191, 0)" stroke="none" id="connector%(pin)dpin" 
        d="M%(x1)f %(y2)f L%(x2)f %(y2)f L%(x2)f %(y1)f L%(a3)f %(y1)f L%(a2)f %(hgap)f L%(a1)f %(y1)f L%(x1)f %(y1)f Z" />
   
"""%dict(
        x1=0+border,
        y1=height/2.0+gap+border,
        x2=width+border,
        y2=height+border,
        a3=width/2.0+gap+border,
        a2=width/2.0+border,
        a1=width/2.0-gap+border,
        hgap=height/2.0+gap/2.0+border,
        pin=1,
    ))

      
    copper_end="""
    </g>
"""
    
    footer="""
</svg>
"""    
    out=header+silkscreen+copper_start+"\n".join(copper_pads)+copper_end+footer
    return out,True
    
    
    
    
    
    
    
    
if __name__=='__main__':
    f=open("test_pcb_sparkgap.svg","w")
    names=[]
    f.write(gen_pcb(names,width=2.0,height=2.0,gap=0.2)[0])
    print "Names:",names
    f.close()
    
    
