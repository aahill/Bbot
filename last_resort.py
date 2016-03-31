import re
import csv

def compare_offspring_to_parent(filename, offspring_gen):
    with open(filename, 'rU') as f:
        parent1_name = ''
        parent2_name = ''
        for org in f:
            org_list = (org.split(','))
            name_list = org_list[0]
            if not org.startswith('Filename'):
                name_split = name_list.split('_')
                if name_split[0] == str(offspring_gen) and name_split[1] == '1':
                    parent1_name += name_split[2]+'_'+name_split[3] 
                    parent2_name += name_split[4]+'_'+name_split[5] 
    with open(filename, 'rU') as f:
        for org in f:
            if org.startswith(parent1_name) or org.startswith(parent2_name):
                print(org)

compare_offspring_to_parent('/home/jake/org/Thesis_Stuff/Robot_Data/Development/Robot_Development_Data_Num_Threads.csv', 2)
