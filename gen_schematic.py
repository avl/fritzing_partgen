

def gen_schematic(cnt):
    out="""<?xml version='1.0' encoding='utf-8'?>
<svg xmlns="http://www.w3.org/2000/svg" y="0in"  baseProfile="tiny" viewBox="0 0 14.4 %(yh)f" height="%(width)fin" id="svg2" width="0.2in" version="1.2" x="0in">
    <desc>
        <referenceFile>unknown.svg</referenceFile>
    </desc>
    <g  id="schematic">"""%dict(width=cnt/10.0,cnt=cnt,yh=7.2*cnt)


    for x in xrange(cnt):
        out+=("""
        <line  stroke="#000000" stroke-width="0.7" stroke-linejoin="round" fill="none" stroke-linecap="round" id="connector%(pinnr)dpin" y1="%(y1)g" y2="%(y1)g" x1="0.35" x2="7.346"/>
        <rect y="%(y1b)g"  fill="none" height="0.208" id="connector%(pinnr)dterminal" width="0.546" x="-0.252"/>
        <polyline  stroke="#000000" stroke-width="0.7" stroke-linejoin="round" points="14.1,%(y2)g 9.928,%(y1)g 14.1,%(y0)g" fill="none" stroke-linecap="round"/>
        <line  stroke="#000000" stroke-width="0.7" stroke-linejoin="round" fill="none" stroke-linecap="round" id="line" y1="%(y1)g" y2="%(y1)g" x1="10.11" x2="4.804"/>
        <text y="%(y0b)g" text-anchor="middle"  stroke="none" stroke-width="0" fill="#8c8c8c" font-size="2.5" font-family="'Droid Sans'" class="text" x="5.05">%(pinnr2)d</text>
        """
        %dict(y0=1.643+7.2*x,y1=3.6+7.2*x,y2=5.557+7.2*x,y1b=3.504+7.2*x,y0b=2.58+7.2*x,pinnr=x,pinnr2=x+1))
        

        
    out+="""</g>
</svg>"""
    return out
    
    
if __name__=='__main__':
    f=open("test_schem.xml","w")

    f.write(gen_schematic(4))
    f.close()
    
    
