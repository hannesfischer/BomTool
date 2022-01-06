import sys, csv, pandas as pd, os, json, webbrowser
from colorama import Fore, Style, init
init()

__ver = "1.1.4"

html_table = ""
queried_parts = []

arg_len = len(sys.argv) 
__arg_ok = 0

if(arg_len != 5):
    _f = open("./req/helptext.txt", "r")
    print("Python BoM-Tool V" + __ver)
    print(_f.read())
elif (arg_len == 2): 
    arg = sys.argv[1]
    if arg == "-h":
        _f = open("./req/helptext.txt", "r")
        print("Python BoM-Tool V" + __ver)
        print(_f.read())
        _f.close()
else:  
    bom_file_pth = sys.argv[1]
    database_pth = sys.argv[2]
    csv_coloum = sys.argv[3]
    xlsx_label = sys.argv[4]
    __arg_ok = True



def parse_bom_data_to_json():
    global csv_headings
    with open(bom_file_pth, 'r') as file:
        try:
            os.remove(".bom.json")
        except:
            print(f"{Fore.YELLOW}JSON data missing. Creating new one ...{Style.RESET_ALL}")
        _json = open(".bom.json", "w")
        _json.write("{")
        csv_file = csv.DictReader(file)
        i = 0
        for row in csv_file:
            _json.write("\""+str(i)+"\":"+str(dict(row))+",")
            i += 1
    _json.write("\"end\":\"end\"")
    _json.write("}")
    _json.close()
    _replace = open(".bom.json", "r")
    _replaced_data = ""
    for _line in _replace:
        _data = _line.strip()
        _new_data = _data.replace("'", "\"")
        _new_data = _new_data.replace("None", "\"None\"")
        _replaced_data += _new_data+"\n"
    _replace.close()
    _new_json = open(".bom.json", "w")
    _new_json.write(_replaced_data)


def create_html_table(desc, parameters, partnr, component, place):
    html = "<tr><td>" + desc + "</td><td>" + parameters + "</td><td>" + partnr + "</td><td>" + component + "</td><td>" + place + "</td></tr>\n"

    return html



if __arg_ok == True:
    #Read CSV File:
    try:
        xlsx_file = pd.read_excel(database_pth)
        data = pd.DataFrame(xlsx_file)
    except:
        print(f"{Fore.RED}Couldn't load excel File!{Style.RESET_ALL}")

    #parse KiCad BOM data to json format

    parse_bom_data_to_json()
    json_file = open(".bom.json", "r")
    buffer = ""
    for line in json_file:
            buffer += line.strip()
    bom_dict = json.loads(buffer)
    json_file.close()
    os.remove(".bom.json")
    try:
        os.remove("./output.html")
    except:
        print(f"Error removing \"output.html\". Has it been removed already?")

    #create output file and start filling it with html

    output = open("./output.html", "w")
    output.write(open("./req/html_head.html", "r").read())
    
    #check each line of the bom with each line of the xlsx file, write the used parts to the html file and skip the ones allready written to it.

    for x in range(len(bom_dict) -1 ):
        for y in range(len(data)):
            if bom_dict[str(x)][csv_coloum] == data[xlsx_label][y]:
                if not str(data.iloc[y][xlsx_label]) in queried_parts:
                    output.write(create_html_table(str(data.iloc[y][0]), str(data.iloc[y][1]), str(data.iloc[y][xlsx_label]), str(bom_dict[str(x)]["Designator"]), str(data.iloc[y]["Lagerort"])))
                    queried_parts.append(str(data.iloc[y][xlsx_label]))
                else:
                    print(f"{Fore.YELLOW}Part exists. Skipped it.{Style.RESET_ALL}")
    #finish up the html and close the file
    
    output.write(open("./req/html_foot.html", "r").read())
    output.close()

    #check the current path and open the html file in the webbrowser
    
    file_path = os.path.dirname(os.path.abspath(__file__)) + "\output.html"
    print(f"{Fore.GREEN}open Browser ... {Style.RESET_ALL}")
    webbrowser.open(file_path)
