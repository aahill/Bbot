from RankAndCrossGeneration import calculateStdError
import csv
import os
from collections import OrderedDict
avgs_averages = []
avgs_std_error = []
list_of_lists =[[] for i in range(0,10)]
dict_list = []

for root, dirs, files in os.walk('/home/jake/org/Thesis_Stuff/Simulation_Data/Random_Selection_Collisions_csvs', topdown=False):
    entry_counter = 0
    curr_avg_sum = 0
    curr_std_error_sum = 0
    
    for name in files:
        file_name = os.path.join(root, name)
        with open(file_name) as f:
            reader = csv.reader(f)
            index = 0
            for row in reader:
                if  row[3] == 'mean collisions':
                    pass
                else:
                    #print row
                    list_of_lists[index].append(row[3])
                    index += 1
            print list_of_lists

counter = 1
for listy in list_of_lists:
    list_ints = [float(f) for f in listy]
    average = sum(list_ints)/float(len(listy))
    dict_list.append(OrderedDict({'Gen': counter, 'Mean collisions': average, 'StdErr': calculateStdError(list_ints, average) }))
    counter += 1
for dic in dict_list:
    print dic
                #line = row.strip().split(',')
