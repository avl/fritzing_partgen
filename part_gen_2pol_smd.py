name="SMD2P"
description="Generic 2 pole SMD component"

import pcb

def javascript():
   return """ 
function on_SMD2P()
{
    add_row('Width:','  <input type="text" name="width" onchange="onpreview()" value="12" /> mm');        
    add_row('Height:',' <input type="text" name="height" onchange="onpreview()" value="6" /> mm');        
    add_row('Pin 1 name:',' <input type="text" name="pin1" onchange="onpreview()" value="pin1" /> mm');        
    add_row('Pin 2 name:',' <input type="text" name="pin2" onchange="onpreview()" value="pin2" /> mm');        
    add_row('Pad width:','  <input type="text" name="padwidth" onchange="onpreview()" value="6"/> mm');        
    add_row('Pad height:',' <input type="text" name="padheight" onchange="onpreview()" value="6"/> mm');        

}
"""    
    

def gen_pcb(pin_names=[],**options):

    pin_names.append(options['pin1'])
    pin_names.append(options['pin2'])
    width=float(options['width'])
    height=float(options['height'])
    padwidth=float(options['padwidth'])
    padheight=float(options['padheight'])

    
           
    overall_w=width
    overall_h=max(height,padheight)
        
                
           
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
     
     
    silkscreen+=("""<rect stroke-width="1.0" fill="none" stroke="white" x="0" y="0" width="%(width)f" height="%(height)f"/>"""%dict(
            width=overall_w,
            height=overall_h                               
        ))
     
    silkscreen+=("""
    </g>    
    """)
    
    
    
    copper_start="""
        <g  id="copper1">
"""   
    copper_pads=[]
    
    

    if padheight>height:
        pad_y=0
    else:
        pad_y=(height-padheight)/2.0
    for pinnr in xrange(2):                    
        copper_pads.append(pcb.pad(
                pinnr=pinnr,
                x=0+(width-padwidth)*pinnr,
                y=pad_y,
                xsize=padwidth,
                ysize=padheight
                ))
    
        
      
    copper_end="""
        </g>
"""
    
    footer="""
</svg>
"""    
    out=header+silkscreen+copper_start+"\n".join(copper_pads)+copper_end+footer
    
    #unicode(out,'ascii')
    print "Type of buf:",type(out)
    return out,True
    
    
    
    
    
    
    
    
if __name__=='__main__':
    f=open("test_pcb.svg","w")
    f.write(gen_pcb(4))    
    f.close()
    
    
