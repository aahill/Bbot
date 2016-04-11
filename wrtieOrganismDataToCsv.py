import Organism
import csv
import os
import re
from json_load_file import json_load_file
import HoboAnalysis

def writeOrganismDataToCsv(pop_dir, outfile):
    for root, dir, files in os.walk(pop_dir, topdown = True):
        for f in files:
            if f.endswith('.txt'):
                print root+'/'+f
                try:
                    org = json_load_file(root+'/'+f)
                    filename = org.filename
                    normalzied_performance = org.performance_2
                    raw_performance = org.performance_1
                    collisions = org.collisions
                    num_wires = len(org.connections)/2
                    num_co_points = len([i.crossover_point for i in org.genome if i.crossover_point ==1])
                    num_active_threads = len([i for i in org.threads if len(i.connected_pins) > 0])
                    print filename
                    print  raw_performance, collisions, num_wires, num_co_points
                except AttributeError:
                    print 'error'

                performance_dict = {'Filename': filename, \
                                    'Raw Performance': raw_performance, \
                                    'Normalzied Performance': normalzied_performance, \
                                    'Number of Collisions': collisions, \
                                    'Number of Wires': num_wires, \
                                    'Number of Crossover Points': num_co_points, \
                                    'Number of Active Threads': num_active_threads
                }
                print performance_dict
                if os.path.isfile(pop_dir +'/'+outfile+'.csv'):
                    with open(pop_dir + '/' + outfile+'.csv' , 'a') as f:
                        fieldnames = ['Filename', 'Raw Performance', 'Normalzied Performance', 'Number of Collisions', \
                                        'Number of Wires', 'Number of Crossover Points', 'Number of Active Threads']
                        writer = csv.DictWriter(f, fieldnames=fieldnames)
                        writer.writerow(performance_dict)
                else:
                    with open(pop_dir + '/' + outfile+'.csv' , 'wb') as f:
                        fieldnames = ['Filename', 'Raw Performance', 'Normalzied Performance', 'Number of Collisions', \
                                        'Number of Wires', 'Number of Crossover Points', 'Number of Active Threads']
                        writer = csv.DictWriter(f, fieldnames=fieldnames)

                        writer.writeheader()
                        writer.writerow(performance_dict)
writeOrganismDataToCsv('/home/jake/org/Thesis_Stuff/Simulation_Data/Random_Selection_Fixed_Xover_No_Devo', 'Fixed_Xover_Simulation_No_Selection_No_Devo')


def baselineCsv(infile, outfile):
    for root, dir, files in os.walk(infile, topdown = True):
        for f in files:
            if "baseline" in f:
                baseline_performance = HoboAnalysis.energyAcquired(root + '/' + f, 2)
                pattern = re.compile('\d')
                gen_num =pattern.search(f).group(0)
                dic={'Gen':gen_num, 'Fitness': baseline_performance}
                if os.path.isfile(infile +'/'+outfile+'.csv'):
                    with open(infile + '/' + outfile+'.csv' , 'a') as f:
                        fieldnames = ['Gen', 'Fitness']
                        writer = csv.DictWriter(f, fieldnames=fieldnames)
                        writer.writerow(dic)
                else:
                    with open(infile + '/' + outfile+'.csv' , 'wb') as f:
                        fieldnames = ['Gen', 'Fitness']
                        writer = csv.DictWriter(f, fieldnames=fieldnames)

                        writer.writeheader()
                        writer.writerow(dic)

