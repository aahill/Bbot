import Organism
from json_load_file import json_load_file
import os


def compareGenomes(path1, path2):
    org1 = json_load_file(path1)
    org2 = json_load_file(path2)
    for i in range(len (org1.genome)):
        print"%s %s\n" % (org1.genome[i].char, org2.genome[i].char)
        assert org1.genome[i].char == org2.genome[i].char

path1 = '/home/jake/org/Thesis_Stuff/Robot_Data/Non_Development/Gen4/4_5_3_7_3_5/4_5_3_7_3_5.txt'
path2 = '/home/jake/org/Thesis_Stuff/Robot_Data/Non_Development/Gen5/5_1_4_5_4_2/5_1_4_5_4_2.txt'
compareGenomes(path1, path2)
