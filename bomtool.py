import sys, csv, pandas as pd, os, json

__ver = "1.0.0"


arg_len = len(sys.argv)
__arg_ok = 0

if(arg_len != 5):
    _f = open("helptext.txt", "r")
    print("Python BoM-Tool V" + __ver)
    print(_f.read())

elif (arg_len == 2):
    arg = sys.argv[1]
    if arg == "-h":
        _f = open("helptext.txt", "r")
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
            print("JSON Daten nichtmehr vorhanden")
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



if __arg_ok == True:
    #Read CSV File:
    xlsx_file = pd.read_excel(database_pth)
    data = pd.DataFrame(xlsx_file)
    parse_bom_data_to_json()
    json_file = open(".bom.json", "r")
    buffer = ""
    for line in json_file:
            buffer += line.strip()
    bom_dict = json.loads(buffer)
    #print(data["LCSC"][3])
    for x in range(len(bom_dict) -1 ):
        for y in range(len(data)):
            if bom_dict[str(x)][csv_coloum] == data[xlsx_label][y]:
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                print("Match at x=" + str(x) + ", y=" + str(y))
                print(data.iloc[y])
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    

