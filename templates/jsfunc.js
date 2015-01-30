
var num_pins=0;
var oldnames={};

function add_row(label,html)
{
    var table = document.getElementById('formtable')
    var row = table.insertRow(-1);
   
    var cell1 = row.insertCell(-1);
    var cell2 = row.insertCell(-1);
    cell1.colSpan=1;
    cell1.innerHTML=label;
    cell2.colSpan=3;
    cell2.innerHTML=html;

}

function delete_table_rows()
{
    
    var table = document.getElementById('formtable')
    while(table.rows.length>2)
    {
        table.deleteRow(-1);
    }
}
function clearpreview()
{
    var div=document.getElementById('imagediv');    
    div.innerHTML='';    
}
function onpreview()
{
    var div=document.getElementById('imagediv');
    
    var urlparm=$("#mainpartform").serialize();
    url='/preview.svg?'+urlparm;
    div.innerHTML='<img src="'+url+'" style="background:#E0E0E0;transform: scale(4);transform-origin: 0 0;" />';    
    
}


function on_part_name_change()
{
    var eform=document.getElementById('mainpartform');
    var e=document.getElementById('partname');
    eform.action=e.value+".fzpz";
    onpreview();
}
function on_ic_change()
{
    clearpreview();
    var e=document.getElementById('ictype');    

    var seltype=e.options[e.selectedIndex].value;
    delete_table_rows();
    
    {% for typ in parts.get_parts() %}
    if (seltype=="{{typ}}")
        on_{{typ}}();    
    else
    {% endfor %}
        alert('internal error');
                
}
window.onload=on_ic_change;

{{parts.get_javascripts()}}


