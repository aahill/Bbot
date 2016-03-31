import re
import csv

def compare_offspring_to_parent(filename, offspring_gen):
    with open(filename, 'rU') as f:
        #the rows of the csv
        mean_dic = find_avgs(filename)
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

                child_fitness = child_list[2]
                child_xovers = child_list[5]
                #the row to write to the csv
                org_row = []
                #try: 
                child_name_split = child_name.split('_')
                #print child_name_split
                #check the first character of the first entry to see if it matches the 
                #desired gen
                if child_name_split[0][0] == str(offspring_gen):
                    #print child_name_split
                    #if child_name_split[0] == str(offspring_gen) and child_name_split[1] == '1':
                    parent1_name = child_name_split[2]+'_'+child_name_split[3] 
                    parent2_name = child_name_split[4]+'_'+child_name_split[5] 

                #except IndexError:
                #    pass
                #get the data for the two partents of the org
                    for org_parent in file_rows:
                        #print org_parent
                        org_list_parent = org_parent.split(',')
                        #print org_list_parent
                        if org_list_parent[0].startswith(parent1_name) or org_list_parent[0].startswith(parent2_name):
                            #print ">>>",org_list_parent[0]
                           #check if current org list is the parent in question
                            if org_list_parent[0].startswith(parent1_name):
                                parent1_name = org_list_parent[0]
                                #parent1_row = org_list_parent.split(',')
                                parent1_fitness = org_list_parent[2]
                                parent1_xovers = org_list_parent[5]
                            elif org_list_parent[0].startswith(parent2_name):
                                parent2_name = org_list_parent[0]
                                #parent2_row = org_parent.split(',')
                                parent2_fitness = org_list_parent[2]
                                parent2_xovers = org_list_parent[5]
                                mean_parent_co_points = (float(parent2_xovers) +float(parent1_xovers))/2.0
                                mean_parent_fitness = (float(parent1_fitness) + float(parent2_fitness)) /2.0
                                if offspring_gen > 1:
                                    mean_parent_gen_co = float(mean_dic[str(offspring_gen - 1)][1]) 
                                    mean_parent_gen_fitness = float(mean_dic[str(offspring_gen - 1)][0]) 
                                    selection_differential_co = mean_parent_gen_co -  mean_parent_co_points
                                    selection_differential_fitness = mean_parent_gen_fitness -  mean_parent_fitness
                                else:
                                    pass
                    org_row = [child_name,child_fitness,child_xovers, parent1_name, parent1_fitness, parent1_xovers, 
                               parent2_name, parent2_fitness, parent2_xovers,mean_parent_co_points,selection_differential_co,
                               mean_parent_fitness,selection_differential_fitness]
                    csv_rows.append(org_row)
        results_file = open('no_devo_highest_rank_child_offspring_comparison.csv', 'a')
        wr = csv.writer(results_file, dialect='excel')
        #wr.writerow(['child','child_fitness','child_xover''parent1', 'parent_1_fitness','parent1_co_points','parent2','parent2_fitness', 'parent2_co_points',
        #'mean_parent_co_points','selection_differential_co_points','mean_parents_fitness','selection_differential_fitness'])
        for x in csv_rows:
            if x[0][2] == '0':
                wr.writerow(x)
#Calculates average fitness and co points for given gen
def find_avgs(filename):
    with open(filename, 'rU') as f:
        output_dic = {}
        org_counter = 0.0
        for org in f:
            if not org.startswith('Filename'):
                split = org.split(',')
                curr_gen = split[0].split('_')[0]
                try:
                    performance = float(split[2])
                    co_points = float(split[5])
                except ValueError:
                    pass
                try:
                    output_dic[curr_gen][0] += performance/10.0
                    output_dic[curr_gen][1] += co_points/10.0
                except KeyError:
                    output_dic[curr_gen] = [(performance/10.0),(co_points/10.0)]

    return output_dic
#compare_offspring_to_parent('/home/jake/org/Thesis_Stuff/Robot_Data/Development/Robot_Development_Data_Num_Threads.csv', 2)
f = '/home/jake/org/Thesis_Stuff/Robot_Data/Non_Development/Robot_Non_Development_Data_Num_Threads.csv'
results_file = open('no_devo_highest_rank_child_offspring_comparison.csv', 'a')
wr = csv.writer(results_file, dialect='excel')
wr.writerow(['child','child_fitness','child_xover''parent1', 'parent_1_fitness','parent1_co_points','parent2','parent2_fitness', 'parent2_co_points' , 'mean_parent_co_points','selection_differential_co_points','mean_parents_fitness','selection_differential_fitness'])
for i in range(2,10):
    compare_offspring_to_parent(f, i)
