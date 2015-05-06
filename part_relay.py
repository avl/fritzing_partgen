from pcb import hole

name="Relay"
description="Generic Relay"

def javascript():
   return """ 
function on_Relay()
{
    add_row('Inputs:','  <input type="text" name="inputs" onchange="onpreview()" value="3" /> (2 or 3)');        
    add_row('Outputs:','  <input type="text" name="outputs" onchange="onpreview()" value="3" /> (2 or 3)');        
    add_row('Separation:',' <input type="text" name="separation" onchange="onpreview()" value="15" /> mm');        
    add_row('Vertical Spacing:',' <input type="text" name="vspace" onchange="onpreview()" value="7.5" /> mm');        
    add_row('Horizontal Spacing:',' <input type="text" name="hspace" onchange="onpreview()" value="5" /> mm');        
    add_row('Hole Size:',' <input type="text" name="hole" onchange="onpreview()" value="1.3" /> mm');        
    add_row('Omron-type:',' <input type="checkbox" name="omron" onchange="onpreview()"/>');        

}
"""    

def gen_pcb(pin_names,**options):
    inputs=int(options['inputs'])
    outputs=int(options['outputs'])
    omron='omron' in options
    separation=float(options['separation'])
    vspace=float(options['vspace'])
    hspace=float(options['hspace'])
    holesize=float(options['hole'])

    silk_t=0.5

    if not omron:
        pin=1
        if outputs==3:
            pin_names.append("%d (nSet)"%(pin,));pin+=1
        else:
            pin_names.append("%d (Set)"%(pin,));pin+=1
        
        if outputs==3:
            pin_names.append("%d (OutputA)"%(pin,));pin+=1


        pin_names.append("%d (Input)"%(pin,));pin+=1
        if outputs==3:
            pin_names.append("%d (OutputB)"%(pin,));pin+=1
        else:
            pin_names.append("%d (Output)"%(pin,));pin+=1

        if outputs==3:
            pin_names.append("%d (OutputB)"%(pin,));pin+=1
        else:
            pin_names.append("%d (Output)"%(pin,));pin+=1

        pin_names.append("%d (Input)"%(pin,));pin+=1
        if outputs==3:
            pin_names.append("%d (OutputA)"%(pin,));pin+=1

        if outputs==3:
            pin_names.append("%d (nRelease)"%(pin,));pin+=1
        else:
            pin_names.append("%d (Release)"%(pin,));pin+=1

        if inputs==3:
            pin_names.append("%d (+CtrlVdd)"%(pin,));pin+=1
    else:
        pin=1
        pin_names.append("%d (coil1)"%(pin,));pin+=1
        pin_names.append("%d (output)"%(pin,));pin+=1
        if outputs==3:
            pin_names.append("%d (inputA)"%(pin,));pin+=1
            pin_names.append("%d (inputB)"%(pin,));pin+=1
        else:
            pin_names.append("%d (input)"%(pin,));pin+=1
        pin_names.append("%d (coil2)"%(pin,));pin+=1
        
   
    edist=2.3+(holesize/2.0-1.3/2.0)
    overall_x=edist*2 + separation + (outputs-1)*hspace
    overall_y=edist*2 + vspace
            
           
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
    
    

       

    pin=[0]
    def emit(x,y):        
        copper_pads.append(hole(
                        x=x+edist,y=y+edist,pinnr=pin[0],ringwidth=0.5*holesize,diameter=holesize
            ))
        pin[0]+=1
        
    if not omron:
        emit(0,0)
        emit(separation,0)
        emit(separation+hspace,0)
        if outputs==3:
            emit(separation+hspace*2,0)

        if outputs==3:
            emit(separation+hspace*2,vspace)
        emit(separation+hspace,vspace)
        emit(separation,vspace)
        emit(0,vspace)
        if inputs==3:
            emit(0,vspace/2.0)
    else:
        emit(0,vspace)    
        if outputs==3:
            emit(separation+hspace/2.0,vspace)    
            emit(separation+hspace,0)    
            emit(separation,0)    
        else:
            emit(separation,vspace)    
            emit(separation+hspace,0)    
        
        emit(0,0)    
      
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
    
    
