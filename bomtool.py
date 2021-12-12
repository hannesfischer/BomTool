import sys, csv, pandas as pd

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

if __arg_ok == True:
    #Read CSV File:
    csv_file = open(bom_file_pth, encoding="UTF8")
    bom_data = csv.reader(csv_file)
    csv_file.close()
    #xlsx_file = pd.read_excel(database_pth)
    #data = pd.DataFrame(xlsx_file, columns=[xlsx_label])
    #data_length = len(data)
    print(bom_data)