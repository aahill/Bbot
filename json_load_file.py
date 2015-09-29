import jsonpickle
import json

def json_load_file(filename):
    f = open(filename)
    json_str = f.read()
    obj = jsonpickle.decode(json_str)
    return obj
