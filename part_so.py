name="SOIC"
description="Generic SOIC component"


def gen_pcb(pin_names,**options):
        
    pincount=int(options.get('pins',0))
    pin_names.extend(['pin%d'%(x+1,) for x in xrange(pincount)])

    for idx in xrange(pincount):
        varname='pin%d'%(idx+1,)
        if varname in options:
            pin_names[idx]=options.get(varname).encode('utf8')
    
    pins=len(pin_names)
    assert pins%2==0
    assert pins>0
    N=pins
    Nh=N/2
    
    e=1.27
    C=5.56
    X1=0.61
    Y1=1.91
    
    silk_h=C-Y1
    
    silk_overhang=0.25
    silk_x1=0.0
    silk_x2=(Nh-1)*e+X1+2.0*silk_overhang
    silk_y1=-silk_h/2.0
    silk_y2=+silk_h/2.0
    
    
    silk_t=0.2
    overall_h=C+Y1
    ww=silk_overhang
    overall_w=silk_x2+silk_t
    ww+=silk_t/2.0
    sht=silk_t/2.0
    hh=overall_h/2.0
    
           
    header="""<?xml version='1.0' encoding='UTF-8'?>
<svg xmlns="http://www.w3.org/2000/svg" baseProfile="tiny" viewBox="0 0 %(w)f %(h)f" height="%(height_mm)fmm" width="%(width_mm)fmm" version="1.2">
    <desc>
        <referenceFile>unknown.svg</referenceFile>
    </desc>
    <desc >Fritzing footprint SVG</desc>    
    
    """%dict(h=overall_h,w=overall_w,height_mm=overall_h,width_mm=overall_w)

    gap=0.5
    igap=silk_y2-gap
    
    silk_points=[    
            (silk_x1+sht,silk_y1+igap+sht),
            (silk_x1+sht,silk_y1+sht),
            (silk_x2-sht,silk_y1+sht),
            (silk_x2-sht,silk_y2-sht),
            (silk_x1+sht,silk_y2-sht),
            (silk_x1+sht,silk_y2-igap-sht),
    ]
    
    silkscreen=("""
    <g  id="silkscreen">
    """)
    
    for a,b in zip(silk_points,silk_points[1:]):
        silkscreen+="""<line  stroke="white" stroke-width="%f" x1="%f" y1="%f" x2="%f" y2="%f"/>"""%(
            silk_t,a[0],a[1]+hh,b[0],b[1]+hh)
        silkscreen+="\n"
    
    
    

    silkscreen+="""<circle  fill="white" stroke-width="0" stroke="none" r="0.25" cx="%(x)f" cy="%(y)f" />"""%dict(
                x=X1/2.0+ww,
                y=silk_y2-0.6+hh
            )           
    
    silkscreen+=""" <path d="M0,%f A0.25,0.25,30,0,1,0,%f" stroke-width="%f" stroke="white" fill="none" />"""%(
            -gap+hh,gap+hh,0.25)

    silkscreen+=("""
    </g>    
    """)
    
    
    
    copper_start="""
    <g  id="copper1">
"""   
    copper_pads=[]
    
    
    for row in xrange(Nh):
        for col in xrange(2):
            if col==0:
                pin=row
                y=C/2.0
            else:
                pin=2*Nh-1-row
                y=-C/2.0
                
            copper_pads.append("""<rect fill="rgb(255, 191, 0)" stroke="none" id="connector%(pin)dpin" x="%(x1)f" y="%(y1)f" width="%(width)f" height="%(height)f"/>"""%dict(
                    pin=pin,
                    x1=row*e+ww,
                    y1=y+hh-Y1/2.0,
                    width=X1,
                    height=Y1
                ))
    
    if 'thermal_pad' in options:
        numrows=Nh
 
        pin_names.append("thermal")
        
        x1=ww
        x2=row*(Nh-1)+ww+X1
        tx=0.5*(x1+x2)
        tx1=1.6
        tx2=overall_w-1.6
        
        txw=tx2-tx1
        if txw<2.29:
            deff=2.29-txw
            tx1-=deff/2.0
            tx2+=deff/2.0
        
        ty1=-2.29/2
        ty2=+2.29/2
        
        copper_pads.append("""<rect  fill="rgb(255, 191, 0)" stroke="none" id="connector%(pin)dpin" x="%(x1)f" y="%(y1)f" width="%(width)f" height="%(height)f"/>"""%dict(
                pin=pins,
                x1=tx1,
                y1=ty1+hh,
                width=tx2-tx1,
                height=ty2-ty1,                               
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
function on_SOIC()
{   
    var pine=document.getElementById('pins');
    var pins=2;
    if (pine)
        pins=parseInt(pine.value);
    delete_table_rows();
    SOIC_add_pins();
    pine=document.getElementById('pins');
    pine.value=''+pins;
    if (pins>4000)
    {
        document.getElementById('pins').value=4000;
        pins=4000;
    }    
    rows=parseInt(pins/2);
    pins=2*rows;
    if (pins==0)
    {
        pins=2;
    }
    num_pins=0;
    while (num_pins<pins)
    {
        SOIC_add_table_row(pins);
        num_pins+=2;
    }
    
    SOIC_add_thermal_pad_option();
    onpreview();
}


function SOIC_add_pins()
{
    add_row('Pin count:','<input type="text" value="2" id="pins" name="pins" onchange="on_SOIC()"/>');
}
function SOIC_add_thermal_pad_option()
{
    add_row('Thermal Pad:','<input type="checkbox" name="thermal_pad" onchange="onpreview()" >');        
}


function SOIC_save_name(pin,rowcol)
{
    var pine=document.getElementById('pin'+pin);
    oldnames[rowcol]=pine.value;
}
function SOIC_add_table_row(pins)
{
    var table = document.getElementById('formtable')
    var row = table.insertRow(-1);

    var rownum=num_pins/2;
    for(var col=0;col<2;++col)
    {
        var pinnum=rownum+1;
        if (col==1)
            pinnum=pins-rownum;
        var cell1 = row.insertCell(-1);
        var cell2 = row.insertCell(-1);
        cell1.innerHTML = "Pin "+pinnum;
        var pinname='';
        var rowcol=''+rownum+'_'+col;
        if (rowcol in oldnames)
            pinname=oldnames[rowcol];
        cell2.innerHTML = '<input type="text" id="pin'+pinnum+'" name="pin'+pinnum+'" onchange="SOIC_save_name('+pinnum+',\\''+rowcol+'\\');" />';
        document.getElementById('pin'+pinnum).value=pinname;
    }
}
 

"""    
    
    
    
    
if __name__=='__main__':
    f=open("test_pcb.xml","w")
    f.write(gen_pcb(4))    
    f.close()
    
    
