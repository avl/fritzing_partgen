#encoding=utf8
from gen_schematic import gen_schematic
from gen_breadboard import gen_breadboard
from datetime import datetime
from gen_icon import gen_icon
import zipfile
import md5
import os
import glob

"""
pins=8
partfilename="part.fzpz"
partname="test4"
version=1
pin_names=["pin%d"%(x+1,) for x in xrange(pins)]
package="so"
"""


def gen_part_xml(name,pins,modname,pin_names,smd):
    copper0=''
    if not smd:
        copper0='<layer layerId="copper0"/>'
        
    for pname in pin_names:
        print "Pin name:",type(pname),pname

    header="""<?xml version='1.0' encoding='UTF-8'?>
    <module fritzingVersion="0.2.2.b.03.04.2550" referenceFile="generic_female_pin_header_4_100mil.fzp" moduleId="%(name)s">
     <version>4</version>
     <author>AMTAB script</author>
     <title>%(name)s</title>
     <label>C</label>
     <date>%(date)s</date>
     <tags/>
     <properties>
      <property name="family">Custom</property>
      <property name="Pins">%(pins)d</property>
      <property name="Position"></property>
      <property name="layer"></property>
      <property name="part number"></property>
      <property name="variant">variant 9</property>
     </properties>
     <description>%(name)s</description>
     <views>
      <iconView>
       <layers image="icon/%(modname)s_icon.svg">
        <layer layerId="icon"/>
       </layers>
      </iconView>
      <breadboardView>
       <layers image="breadboard/%(modname)s_breadboard.svg">
        <layer layerId="breadboard"/>
       </layers>
      </breadboardView>
      <schematicView fliphorizontal="true">
       <layers image="schematic/%(modname)s_schematic.svg">
        <layer layerId="schematic"/>
       </layers>
      </schematicView>
      <pcbView>
       <layers image="pcb/%(modname)s_pcb.svg">
        %(copper0)s
        <layer layerId="copper1"/>
        <layer layerId="silkscreen"/>
       </layers>
      </pcbView>
     </views>
     <connectors>          
     """%dict(name=name.encode('utf8'),date=datetime.now().strftime("%a %b %d %Y"),modname=modname,pins=pins,copper0=copper0)
     

    connectors=[]
    assert len(pin_names)==pins
    for pin,pinname in enumerate(pin_names):
        pinname=pinname.encode('utf8')
        if smd:
            extra=''
        else:
            extra='<p svgId="connector%(nr)dpin" layer="copper0"/>'%dict(nr=pin)
        connectors.append("""
      <connector type="male" id="connector%(nr)d" name="%(pinname)s">
       <description>%(pinname)s</description>
       <views>
        <breadboardView>
         <p svgId="connector%(nr)dpin" layer="breadboard" terminalId="connector%(nr)dterminal"/>
        </breadboardView>
        <schematicView>
         <p svgId="connector%(nr)dpin" layer="schematic" terminalId="connector%(nr)dterminal"/>
        </schematicView>
        <pcbView>
         %(extra)s
         <p svgId="connector%(nr)dpin" layer="copper1"/>
        </pcbView>
       </views>
      </connector>
      """%dict(nr=pin,pinname=pinname,extra=extra))
              
    footer="""
     </connectors>
    </module>
    """
    return header+"\n".join(connectors)+footer
    

#import importlib

parts=dict()
def init():

    globlist=os.path.dirname(__file__)+"/*.py"
    for pyfile in glob.glob(globlist):
        if os.path.basename(pyfile).startswith("part_"):        
            mod=__import__(os.path.basename(pyfile)[:-3])
            parts[mod.name]=mod
init()

def get_parts():
    return parts.keys()
def get_parts_with_description():
    return [(part.name,part.description) for part in parts.values()]
    

import traceback
missing_svg=open('missing.svg').read()
def make_part_preview(package,options):
    try:
        mod=parts[package]
        pcb,smd=mod.gen_pcb(pin_names=[],**options)
    except Exception,cause:
        print cause
        print traceback.format_exc()
        return missing_svg
    return pcb

def get_javascript(package):
    mod=parts[package]
    if hasattr(mod,'javascript'):
        return mod.javascript()
    return """
    function on_%s()
    {
        onpreview();
    }
"""%(package,)

def get_javascripts():
    out=[]
    for package in get_parts():
        print "Package:",package
        out.append(get_javascript(package))
    return "\n".join(out)
   
def make_part(
    partfilename,
    partname,
    version,
    package="SOIC",
    options=dict()):
 
    pin_names=[]    
    
    mod=parts[package]
    print "Calling mod:",mod
    pcb,smd=mod.gen_pcb(pin_names=pin_names,**options)
    
    
    
    pins=len(pin_names)
    print "Package:",package,"pins:",pins
    assert type(pins)==int
    if pin_names==None:
        pin_names=["pin%d"%(x+1,) for x in xrange(pins)]
            
    dig=md5.md5("f1_v%d_%d_%s"%(version,pins,partname.encode('utf8'))).hexdigest()

    modname="%s_%s_%d"%(partname.encode('utf8'),dig,version)

    schem=gen_schematic(pins)
    bread=gen_breadboard(pins)

    icon=gen_icon(pins)
    print "Pins:",pins  
    partxml=gen_part_xml(partname,pins,modname,pin_names,smd)

    f=open("test_part.xml","w")
    f.write(partxml)
    f.close()


    #os.unlink(partfilename)
    partfile=zipfile.ZipFile(partfilename,"w")
    
    print "types",type(bread),type(pcb),type(schem),type(icon),type(partxml)

    partfile.writestr("svg.breadboard.%s_breadboard.svg"%(modname,),bread)
    partfile.writestr("svg.pcb.%s_pcb.svg"%(modname,),pcb)
    partfile.writestr("svg.schematic.%s_schematic.svg"%(modname,),schem)
    partfile.writestr("svg.icon.%s_icon.svg"%(modname,),icon)
    partfile.writestr("part.%s.fzp"%(modname,),partxml)


