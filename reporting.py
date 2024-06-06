import json
from json2html import *
from pathlib import Path


def convert2html(json_file, folder_path, outputfilename = ""):
    if (outputfilename==""):
        outputfilename = folder_path + Path(json_file).stem+".html"
        html_fp = open(outputfilename,'w')
        
    with open(json_file, 'r') as json_fp:
        data = json.load(json_fp)
        json_fp.close
    
    
    data=json.dumps(data)
    build_direction = "LEFT_TO_RIGHT"
    table_attributes = {"style" : "width:50%","class" : "table ","border" :1}
    
    html_txt  = json2html.convert(json=data)
    html_fp.write(html_txt)
    html_fp.close
    
    return html_fp.name

