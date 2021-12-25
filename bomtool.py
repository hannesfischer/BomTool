import sys, csv, pandas as pd, os, json, webbrowser


__ver = "1.1.3"

html_table = ""
queried_parts = []

arg_len = len(sys.argv)
__arg_ok = 0


if(arg_len != 5):
    _f = open("req/helptext.txt", "r")
    print("Python BoM-Tool V" + __ver)
    print(_f.read())
elif (arg_len == 2):
    arg = sys.argv[1]
    if arg == "-h":
        _f = open("req/helptext.txt", "r")
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
    with open("bom.csv", 'r') as file:
        try:
            os.remove(".bom.json")
        except:
            print("JSON data missing. Creating new one ...")
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


def create_html_table(desc, parameters, partnr, required):
    html = "<tr><td>" + desc + "</td><td>" + parameters + "</td><td>" + partnr + "</td><td>" + required + "</tr>\n"

    return html



if __arg_ok == True:
    #Read CSV File:
    try:
        xlsx_file = pd.read_excel(database_pth)
        data = pd.DataFrame(xlsx_file)
    except:
        print("Couldn't load excel File!")
    parse_bom_data_to_json()
    json_file = open(".bom.json", "r")
    buffer = ""
    for line in json_file:
            buffer += line.strip()
    bom_dict = json.loads(buffer)
    json_file.close()
    os.remove(".bom.json")
    #print(data["LCSC"][3])
    try:
        os.remove("./output.html")
    except:
        print("Error removing \"output.html\". Has it been removed already?")
    output = open("./output.html", "w")
    output.write(open("./req/html_head.html", "r").read())
    for x in range(len(bom_dict) -1 ):
        for y in range(len(data)):
            if bom_dict[str(x)][csv_coloum] == data[xlsx_label][y]:
                #print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                #output.write(str(data.iloc[y][0]) + "\n" + str(data.iloc[y][xlsx_label]))
                #output.write("\n\nPro Platine benoetigt:         " + bom_dict[str(x)]["Quantity Per PCB"])
                #output.write("\n~~~~~~~~~~~~~~~~~~~~\n")
                if not str(data.iloc[y][xlsx_label]) in queried_parts:
                    output.write(create_html_table(str(data.iloc[y][0]), str(data.iloc[y][1]), str(data.iloc[y][xlsx_label]), bom_dict[str(x)]["Quantity Per PCB"]))
                    queried_parts.append(str(data.iloc[y][xlsx_label]))
                else:
                    print("Part exists. Skipped it.")
                #print(data.iloc[y][1])
                #print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                #print("")
                #dump_string = str(bom_dict[str(x)][0][0]) + " at " + str(data.iloc[y])
                #print(dump_string)
    output.write(open("./req/html_foot.html", "r").read())
    output.close()
    file_path = os.path.dirname(os.path.abspath(__file__)) + "\output.html"
    webbrowser.open(file_path)
