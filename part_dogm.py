from pcb import hole

name="EADOG"
description="Electronic Assembly DOG LCD"

def gen_pcb(pin_names):

    overall_x=55.0 + 2.0
    overall_y=31.0 + 1.0
     
    xx=overall_x/2.0
    yy=overall_y/2.0
    
    pin_row_dist=27.94
    pin_pitch=2.54
    
    silk_t=0.5
            
           
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
    
    for a,b in zip(silk_points,silk_points[1:]):
        silkscreen+="""<line fill="none" stroke="white" stroke-width="%f" x1="%f" y1="%f" x2="%f" y2="%f"/>"""%(
            silk_t,a[0],a[1],b[0],b[1])
        silkscreen+="\n"
               
    silkscreen+=("""
    </g>    
    """)
    
    
    
    copper_start="""
    <g  id="copper0">
        <g  id="copper1">
"""   
    copper_pads=[]
    
    
    row_width=19.0*pin_pitch
    
    startx=-row_width/2.0
    starty=-pin_row_dist/2.0
    
    pinnr=0 #partgen/fritzing pinnr
    for col in xrange(20):
        for row in xrange(2):
            if row==1 and not col in (0,1,18,19):
                continue
            y=float(row)*pin_row_dist + starty
            x=startx+2.54*col
            
            if row==0:
                dogpin=40-col #pin nr from schematic
            else:
                dogpin=1+col
            name=None
            if row==1:
                if dogpin==1: name="A1"
                elif dogpin==2: name="C1"
                elif dogpin==19: name="C2"
                elif dogpin==20: name="A2"
                else: raise Exception()
            else:
                name={ 
                        21:'CAP1N',
                        22:'CAP1P',
                        23:'PSB',
                        24:'VOUT',
                        25:'VIN',
                        26:'VDD',
                        27:'VSS',
                        28:'D7',
                        29:'D6',
                        30:'D5',
                        31:'D4',
                        32:'D3',
                        33:'D2',
                        34:'D1',
                        35:'D0',
                        36:'E',
                        37:'R/W',
                        38:'CSB',
                        39:'RS',
                        40:'RESET'
                    }[dogpin]
                                    
        
            copper_pads.append(hole(
                                x=x+xx,y=y+yy,pinnr=pinnr,ringwidth=0.5,diameter=0.825
                    ))
                    
            assert name
            pin_names.append(name)
            pinnr+=1
      
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
    f=open("test_pcb_dogm.svg","w")
    names=[]
    f.write(gen_pcb(names))
    print "Names:",names
    f.close()
    
    
