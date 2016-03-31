import re
import csv

def compare_offspring_to_parent(filename, offspring_gen):
    with open(filename, 'rU') as f:
        #the rows of the csv
        file_rows = [row for row in f]
        #rows to create teh eresultant csv with
        csv_rows = []
        #iterate through each entry in the csv
        for org in file_rows:
            if not org.lower().startswith("filename"):
                parent1_name = ''
                parent1_fitness = 0
                parent1_xovers = 0

                parent2_name = ''
                parent2_fitness = 0
                parent2_xovers = 0

                child_list = (org.split(','))
                child_name = child_list[0]

                child_fitness = 0
                child_xovers = 0
                #the row to write to the csv
                org_row = []
                #try: 
                child_name_split = child_name.split('_')
                print child_name_split
                #check the first character of the first entry to see if it matches the 
                #desired gen
                if child_name_split[0][0] == str(offspring_gen):
                    print child_name_split
                    #if child_name_split[0] == str(offspring_gen) and child_name_split[1] == '1':
                    parent1_name = child_name_split[2]+'_'+child_name_split[3] 
                    parent2_name = child_name_split[4]+'_'+child_name_split[5] 

                #except IndexError:
                #    pass
                #get the data for the two partents of the org
                    for org_parent in file_rows:
                        print org_parent
                        org_list_parent = org_parent.split(',')
                        #print org_list_parent
                        if org_list_parent[0].startswith(parent1_name) or org_list_parent[0].startswith(parent2_name):
                            #print ">>>",org_list_parent[0]
                           #check if current org list is the parent in question
                            if org_list_parent[0].startswith(parent1_name):
                                parent1_name = org_list_parent[0]
                                #parent1_row = org_list_parent.split(',')
                                parent1_fitness = org_list_parent[1]
                                parent1_xovers = org_list_parent[5]
                            elif org_list_parent[0].startswith(parent2_name):
                                parent2_name = org_list_parent[0]
                                #parent2_row = org_parent.split(',')
                                parent2_fitness = org_list_parent[1]
                                parent2_xovers = org_list_parent[5]
                    org_row = [child_name, parent1_name, parent1_fitness, parent1_xovers, 
                        parent2_name, parent2_fitness, parent2_xovers]
                    csv_rows.append(org_row)
        for x in csv_rows:
            print x


#compare_offspring_to_parent('/home/jake/org/Thesis_Stuff/Robot_Data/Development/Robot_Development_Data_Num_Threads.csv', 2)
f = '/Users/Aaron/Downloads/Robot_Non_Development_Data_Num_Threads.csv'
compare_offspring_to_parent(f, 2)
