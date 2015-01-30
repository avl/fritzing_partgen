
def gen_breadboard(pins):
    cnt=pins
    out="""<?xml version='1.0' encoding='utf-8'?>
<svg xmlns="http://www.w3.org/2000/svg" y="0in"  baseProfile="tiny" viewBox="0 0 %(cnt)d000 1000" height="0.1in" width="%(width)fin" version="1.2" x="0in">
    <desc>
        <referenceFile>unknown.svg</referenceFile>
    </desc>
    <g  id="breadboard">
        <rect  fill="#404040" height="1000" width="%(cnt)d000"/>"""%dict(cnt=pins,width=cnt/10.0)
    
    for pin in xrange(cnt):

        pintext=("%d"%(pin,)) if pin else ''
        out+="""
        <rect y="306.727"  fill="none" height="386.544" id="connector%(pin)dpin" width="386.544" x="%(x)s306.727"/>
        <rect y="343.131"  fill="none" height="313.414" id="connector%(pin)dterminal" width="299.763" x="%(x)s349.77"/>
        <rect y="306.727"  height="386.544" width="386.544" x="%(x)s306.727"/>
        <polygon  points="%(x)s164.507,164.507 %(x)s306.727,306.727 %(x)s693.272,306.727 %(x)s835.631,164.507 &#x9;" fill="#2A2A29"/>
        <polygon  points="%(x)s835.631,164.507 %(x)s693.272,306.727 %(x)s693.272,693.272 %(x)s835.631,835.631 &#x9;" fill="#474747"/>
        <polygon  points="%(x)s835.631,835.631 %(x)s693.272,693.272 %(x)s306.727,693.272 %(x)s164.507,835.631 &#x9;" fill="#595959"/>
        <polygon  points="%(x)s164.507,835.631 %(x)s306.727,693.272 %(x)s306.727,306.727 %(x)s164.507,164.507 &#x9;" fill="#373737"/>
        """%dict(x=pintext,pin=pin)
        

    out+="""
    </g>
</svg>"""
    return out
    

    
if __name__=='__main__':
    f=open("test_bread.xml","w")

    f.write(gen_breadboard(4))
    f.close()
    
    
