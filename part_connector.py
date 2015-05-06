from pcb import hole
import pcb

name="Connector"
description="Generic Connector"

def javascript():
   #inch = size_mm/25.4
   #inch*1000 = size_mm*(1000.0/25.4) = size_mm*39.37007874015748
   return """ 
function Connector_delete_row()
{
    var table = document.getElementById('formtable')
    table.deleteRow(-1);
}   
Connector_rows=0;
function on_Connector()
{
    on_ConnectorUpdate(1);
}
function on_calc_mils()
{
    var e=document.getElementById('Connector_sparkgap_mils');
    e.innerHTML=(parseFloat(document.getElementById('sparkgap_width').value)*39.37007874015748).toFixed(2);
}
function on_ConnectorUpdate(initial)
{
    var pine=document.getElementById('Connector_pins');
    var pins=2;
    if (pine)
    {
        pins=parseInt(pine.value);
        if (pins>1000)
        {
            pins=10000;
            pine.value=10000;
        }
    }
    while(Connector_rows>0)
    {
        Connector_delete_row();
        Connector_rows-=1;
    }
    if (initial)
    {
        add_row('Pins','  <input type="text" id="Connector_pins" name="pins" onchange="on_ConnectorUpdate(0)" value="2" />');        
        add_row('Hole size:','  <input type="text" name="holesize" onchange="onpreview()" value="1.0" /> mm diameter');        
        add_row('Ring width:',' <input type="text" name="ringwidth" onchange="onpreview()" value="0.3" /> mm');        
        add_row('Pitch',' <input type="text" name="pitch" onchange="onpreview()" value="3.5" /> mm');        
        add_row('Overall Width',' <input type="text" name="width" onchange="onpreview()" value="" /> mm (blank for auto)');        
        add_row('Overall Height',' <input type="text" name="height" onchange="onpreview()" value="" /> mm (blank for auto)');        
        add_row('Height Offset',' <input type="text" name="height_offset" onchange="onpreview()"/> mm (blank for auto)');        
        add_row('Spark Gap',' <input type="checkbox" name="sparkgap" onchange="onpreview()"/> (blank for auto)');            
        add_row('Spark Gap Width',' <input type="text" name="sparkgap_width" id="sparkgap_width" onchange="onpreview();on_calc_mils()"/> mm (if sparkgap chosen) (<span id="Connector_sparkgap_mils"></span> mils)');            
        add_row('Spark Gap Lead',' <input type="text" name="sparkgap_lead" onchange="onpreview()"/> mm (if sparkgap chosen)');            
    }
    var num_pins=0;
    while (num_pins<pins)
    {
        Connector_add_table_row(num_pins);
        num_pins+=1;
    }
    Connector_rows=num_pins;
}


function Connector_save_name(pin,rowcol)
{
    var pine=document.getElementById('pin'+pin);
    oldnames[rowcol]=pine.value;
}

function Connector_add_table_row(pinnum)
{
    var table = document.getElementById('formtable')
    var row = table.insertRow(-1);

    var cell1 = row.insertCell(-1);
    var cell2 = row.insertCell(-1);
    cell1.innerHTML = "Pin "+pinnum;
    var pinname='';
    var rowcol=''+pinnum;
    if (rowcol in oldnames)
        pinname=oldnames[rowcol];
    cell2.innerHTML = '<input type="text" id="pin'+pinnum+'" name="pin'+pinnum+'" onchange="Connector_save_name('+pinnum+',\\''+rowcol+'\\');" />';
    document.getElementById('pin'+pinnum).value=pinname;

}
"""    

def gen_pcb(pin_names,**options):
    pins=int(options['pins'])
    holesize=float(options['holesize'])
    ring=float(options['ringwidth'])
    pitch=float(options['pitch'])
    width=float(options['width']) if 'width' in options and options['width'].strip() else 0.0
    height=float(options['height']) if 'height' in options and options['height'].strip() else 0.0
    offset=float(options['height_offset']) if 'height_offset' in options and options['height_offset'].strip() else 0.0
    sparkgap='sparkgap' in options
    sparkgap_width=float(options['sparkgap_width']) if 'sparkgap_width' and options['sparkgap_width'].strip() else 0.5
    sparkgap_lead=float(options['sparkgap_lead']) if 'sparkgap_lead' and options['sparkgap_lead'].strip() else 1.0
        
    if sparkgap_lead<0.5:
        sparkgap_lead=0.5

    for i in xrange(pins):
        pin_names.append(options['pin%d'%(i,)])
    if sparkgap:
        pin_names.append("SparkGND")        

    silk_t=0.5

    effective_ring=ring+2*pcb.defaultplating

    if width==0:
        width=pitch*(pins+1)+holesize+effective_ring*2
    if height==0:
        height=(3+holesize+effective_ring*2)
    
    minwidth=pitch*(pins-1)+holesize+effective_ring*2.0
    minheight=holesize+effective_ring*2.0

           
    overall_x=max(width,minwidth)
    overall_y=max(height,minheight)
    
    dx=(overall_x - (pins-1)*pitch)/2.0
    dy=overall_y/2.0+offset
    
    ringtop=dy-holesize/2.0-effective_ring
    gaph1=ringtop-sparkgap_width*2.0-sparkgap_lead
    gaph2=ringtop-sparkgap_width*2.0
    gaph3=ringtop-sparkgap_width
            
           
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
    
    
      

    for x in xrange(pins):
        copper_pads.append(hole(
                        x=dx+pitch*x,y=dy,pinnr=x,ringwidth=ring,diameter=holesize
            ))
            
    if sparkgap:
        copper_pads.append("""<path fill="rgb(255, 191, 0)" stroke="none" id="connector%(pin)dpin" d="M%(x)f %(y)f L%(x1)f %(y1)f L%(x2)f %(y2)f"""%(
            dict(pin=pins,x=dx-holesize/2.0,y=gaph1,x1=dx+pitch*(pins-1)+holesize/2.0,y1=gaph1,x2=dx+pitch*(pins-1)+holesize/2.0,y2=gaph2)))
        for x in reversed(xrange(pins)):
            a1=dx+pitch*x-holesize/2.0
            a2=dx+pitch*x
            a3=dx+pitch*x+holesize/2.0
            copper_pads.append(" L%f %f L%f %f L%f %f "%(a3,gaph2,a2,gaph3,a1,gaph2))
        
        copper_pads.append(" Z\" /> ")


        copper_pads.append(hole(
                        x=dx,y=(gaph1+gaph2)*0.5,pinnr=None,ringwidth=sparkgap_lead*0.4/2.0-pcb.defaultplating,diameter=sparkgap_lead*0.6))
        if pins>1:
            copper_pads.append(hole(
                        x=dx+pitch*(pins-1),y=(gaph1+gaph2)*0.5,pinnr=None,ringwidth=sparkgap_lead*0.4/2.0-pcb.defaultplating,diameter=sparkgap_lead*0.6))
            

      
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
    
    
