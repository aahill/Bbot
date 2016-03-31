import re
import csv

def compare_offspring_to_parent(filename, offspring_gen):
    with open(filename, 'rU') as f:
        parent1_name = ''
        parent2_name = ''
        for org in f:
            org_list = (org.split(','))
            name_list = org_list[0]
            try:
                name_split = name_list.split('_')
                if name_split[0] == str(offspring_gen) and name_split[1] == '1':
                    parent1 += name_split[2]+'_'+name_split[3] 
                    parent2 += name_split[4]+'_'+name_split[5] 
            except IndexError:
                pass
        for org in f:
            org.startswith(parent1) or org.startswith()
compare_offspring_to_parent('/home/jake/org/Thesis_Stuff/Robot_Data/Development/Robot_Development_Data_Num_Threads.csv', 2)
