name="EMIFIL"
description="EMI filter 1206 package"
def gen_pcb(pin_names):

    overall_x=5.4
    overall_y=3.2
    
    silk_x=3.4
    silk_y=1.45
    
    mid_pad_x=1.1
    mid_pad_y=3.2
    
    outer_pad_x=1.3
    outer_pad_y=2.0 
    
    
    pad1_x1=-overall_x/2.0+0.1
    pad1_x2=-overall_x/2.0+0.1+outer_pad_x
    pad1_y1=-outer_pad_y/2.0
    pad1_y2=outer_pad_y/2.0

    
    pad2_x1=-mid_pad_x/2.0
    pad2_x2=mid_pad_x/2.0
    pad2_y1=-mid_pad_y/2.0+0.1
    pad2_y2=mid_pad_y/2.0-0.1
    
    pad3_x1=overall_x/2.0-0.1-outer_pad_x
    pad3_x2=overall_x/2.0-0.1
    pad3_y1=-outer_pad_y/2.0
    pad3_y2=outer_pad_y/2.0

    xx=overall_x/2.0
    yy=overall_y/2.0
    
    silk_t=0.2
            
           
    header="""<?xml version='1.0' encoding='UTF-8'?>
<svg xmlns="http://www.w3.org/2000/svg" baseProfile="tiny" viewBox="0 0 %(w)f %(h)f" height="%(height_mm)fmm" width="%(width_mm)fmm" version="1.2">
    <desc>
        <referenceFile>unknown.svg</referenceFile>
    </desc>
    <desc >Fritzing footprint SVG</desc>    
    
    """%dict(w=overall_x,h=overall_y,height_mm=overall_y,width_mm=overall_x)

    
    silk_seqs=[[    
            (0,0),
            (overall_x,0),
            (overall_x,overall_y),
            (0,overall_y),
            (0,0)
    ],[
        (mid_pad_x/2.0+xx,-mid_pad_y/2.0+yy),
        (mid_pad_x/2.0+xx,mid_pad_y/2.0+yy)
    ],[
        (-mid_pad_x/2.0+xx,-mid_pad_y/2.0+yy),
        (-mid_pad_x/2.0+xx,mid_pad_y/2.0+yy)
    ]
    ]
    
    silkscreen=("""
    <g  id="silkscreen">
    """)
    
    for silk_points in silk_seqs:
        for a,b in zip(silk_points,silk_points[1:]):
            silkscreen+="""<line fill="none" stroke="black" stroke-width="%f" x1="%f" y1="%f" x2="%f" y2="%f"/>"""%(
                silk_t,a[0],a[1],b[0],b[1])
            silkscreen+="\n"
               
    silkscreen+=("""
    </g>    
    """)
    
    
    
    copper_start="""
        <g  id="copper1">
"""   
    copper_pads=[]

    
        
    copper_pads.append("""<rect  fill="rgb(255, 191, 0)" stroke="none" id="connector%(pin)dpin" x="%(x1)f" y="%(y1)f" width="%(width)f" height="%(height)f"/>"""%dict(
            pin=0,
            x1=pad1_x1+xx,
            y1=pad1_y1+yy,
            width=pad1_x2-pad1_x1,
            height=pad1_y2-pad1_y1,                               
        ))

    copper_pads.append("""<rect  fill="rgb(255, 191, 0)" stroke="none" id="connector%(pin)dpin" x="%(x1)f" y="%(y1)f" width="%(width)f" height="%(height)f"/>"""%dict(
            pin=1,
            x1=pad2_x1+xx,
            y1=pad2_y1+yy,
            width=pad2_x2-pad2_x1,
            height=pad2_y2-pad2_y1,                               
        ))

    copper_pads.append("""<rect  fill="rgb(255, 191, 0)" stroke="none" id="connector%(pin)dpin" x="%(x1)f" y="%(y1)f" width="%(width)f" height="%(height)f"/>"""%dict(
            pin=2,
            x1=pad3_x1+xx,
            y1=pad3_y1+yy,
            width=pad3_x2-pad3_x1,
            height=pad3_y2-pad3_y1,                               
        ))


    pin_names.extend(["IN",'GND','OUT'])

    copper_end="""
    </g>
"""
    
    footer="""
</svg>
"""    
    out=header+silkscreen+copper_start+"\n".join(copper_pads)+copper_end+footer
    return out,True
    
    
    
    
    
    
    
    
if __name__=='__main__':
    f=open("test_pcb_emifil.svg","w")
    names=[]
    f.write(gen_pcb(names))
    print "Names:",names
    f.close()
    
    
