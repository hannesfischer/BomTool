import sys

__ver = "1.0.0"

arg_len = len(sys.argv)

if(arg_len != 3):
    _f = open("helptext.txt", "r")
    print("Python BoM-Tool V" + __ver)
    print(_f.read())

elif (arg_len == 2):
    arg = sys.argv[1]
    if arg == "-h":
        _f = open("helptext.txt", "r")
        print("Python BoM-Tool V" + __ver)
        print(_f.read())
else:  
    bom_file = sys.argv[1]
    database = sys.argv[2]

    print(bom_file)
    print(database)

