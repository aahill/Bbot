__author__ = 'JakeBrawer'
#from json_load_file import json_load_file
import json
import jsonpickle
import random
from  Organism import *
import HoboAnalysis
import os
import math
import datetime
import csv
import gc
global_quartiles = {}
def json_load_file(filename):
    f = open(filename)
    json_str = f.read()
    obj = jsonpickle.decode(json_str)
    return obj

def calculateStdError(list_of_vals, average):
    stddev = 0.0
    diffsquared = 0.0
    sum_diffsquared = 0.0
    print '\n--------------------------------------------------\nCalculating the Std Error of the mean: '
    for val in list_of_vals:
        diffsquared = (val- average)**2.0
        sum_diffsquared += diffsquared 
        print 'Org mean perf: %s Pop mean: %s Diffsqrd: %s SumDiffsqrd: %s ' % (val, average, diffsquared, sum_diffsquared)
    stddev = math.sqrt((sum_diffsquared)/len(list_of_vals))
    stderror = stddev / math.sqrt(len(list_of_vals))
    print 'Stddv: %s  StdErr: %s\n------------------------------------------------------------\n ' % (stddev, stderror)
    #print(numpy.sqrt(numpy.var(list_of_vals)))
    return stderror
def thresholdedCrossGeneration(experiment_directory, gen_directory,path_to_new_gen,*new_gen_size):
    unpickled_orgs = []# temporarily holds unpickled orgs
    try:
        new_gen_size = int( new_gen_size[0]) #turns the input (a tuple) into an int
    except IndexError:
        new_gen_size = None #No size input given
    def evaluateGenerationPerformance(gen_directory):
        global global_quartiles
        mean_performance_per_org = [] 
        mean_performance_per_pop = 0
        list_of_vals = []
        collisions_per_org = []
        num_wires_per_org = []
        y = []
        baseline_performance = 0
        #get the performance of the baseline organism
        for root, dir, files in os.walk(gen_directory):
            org = None
            performance = 0
            for f in files:
                if "baseline" in f:
                    baseline_performance = HoboAnalysis.energyAcquired(root + '/' + f, 2)
    
        #walks through files belonging to an organism, one org at a time
        print "All the org files in this directory:"
        for root, dir, files in os.walk(gen_directory):
            org = None
            #will store the amount of light collected on both trials
            performance_1 = 0
            performance_2 = 0
            y.append(root)
            for f in files:
                try:
                    y.append(f)
                    if f.endswith('.txt'):
                        org = json_load_file(root + '/' + f)
                        #print  rooty + '/'+ f
                        #print [i.crossover_point for i in org.genome]
                    elif f.endswith('.csv'):
                        if f == 'quartile_data.csv':
                            pass
                        else:
                            if performance_1 == 0:
                                #rooty denotes the path to subdir, f a file in root. Concatenating
                                # the two results in the full path to file
                                #divide performance by the baseline for normalization
                                performance_1 = HoboAnalysis.energyAcquired(root +'/' + f, 2)
                                # This stores the normalized fitness
                                performance_2 = HoboAnalysis.energyAcquired(root + '/' + f, 2)/baseline_performance
                except AttributeError:
                    pass
            try:
                org.performance_1 = performance_1
                org.performance_2 = performance_2
                #Connections attributes stores all pins connected
                #Dividing by 2 will give us the number of wires
                num_wires_per_org.append(len(org.connections)/2)
                #append the average of two performances to list
                #for use later in calculating stddev
                mean_performance_per_org.append(org.performance_2)
                collisions_per_org.append(org.collisions)
                unpickled_orgs.append(org)
                org.save_to_file(gen_directory)
                # org.save_to_file(f)
            except AttributeError:
                pass
    #for org in unpickled_orgs:
        #   mean_performance_per_org.append((org.performance_1 + org.performance_1) / 2.0 )"""
        print'\n mean performances for each org in population:', mean_performance_per_org
        #Calculates quartiles: Q1 = mean * .5, Q2 = mean, Q3 = mean * 1.5
        mean_performance_per_pop = sum(mean_performance_per_org)/float(len(mean_performance_per_org))
        mean_collisions = sum(collisions_per_org)/float(len(collisions_per_org))
        mean_wires =sum(num_wires_per_org)/float(len(num_wires_per_org))
        #Saves quartile information and stdev of pop mean to a dict
        quartiles = {'Generation': unpickled_orgs[0].generation, \
                     'mean': mean_performance_per_pop, \
                     'stderr': calculateStdError(mean_performance_per_org, mean_performance_per_pop), \
                     'mean collisions':mean_collisions, \
                     'collision stderr': calculateStdError(collisions_per_org, mean_collisions), \
                     'collisions min': min(collisions_per_org), \
                     'collisions max': max(collisions_per_org), \
                     'mean wires': mean_wires, \
                     'mean wires stderr': calculateStdError(num_wires_per_org, mean_wires)}
        print '\nquartiles: %s\n' % quartiles  
        global_quartiles = quartiles
        return quartiles
    def calculateRankings(gen_directory):
        evaluateGenerationPerformance(gen_directory)
        sorted_orgs = sorted(unpickled_orgs, key=lambda x: (x.performance_1 + x.performance_1)/2.0,\
                             reverse=True)
        ranking = []
        while len(sorted_orgs) >0:
            ranking.append([sorted_orgs.pop(0), sorted_orgs.pop(0)])
    
        print 'ranking:', ranking
    
        return ranking
       
    def crossAndSaveGeneration(path_to_new_gen,new_gen_size):
        #These lines calculate the quartiles, and then save each area 
        #above a quartile to its own list
        rankings = calculateRankings(gen_directory)
        fours = rankings.pop(0)
        threes = rankings.pop(0)
        twos = rankings.pop(0)
        ones = rankings.pop(0)
        def chooseTwoToCross(path_to_new_gen):
            org1 = None
            org2 = None
            #This horribly ugly blcok of code handles the selection of the orgs
            #To be crossed. The algorithm always looks two cross orgs in the higher
            #lists first (i.e. threes then twos then ones). Once an organism has been
            #crossed, they are put into a lower list (Threes-->twos, etc), or are
            #removed altogether from the lists (ones --> n/a)
            try:
                print 'fours %s' % [i.filename for i in fours]
                print 'threes %s' % [i.filename for i in threes]
                print 'twos %s' % [i.filename for i in twos]
                print 'ones %s' % [i.filename for i in ones]
            except IndexError:
                pass
            if len(fours) > 0:
                org1 = random.choice(fours)
                fours.remove(org1)
                threes.append(org1)
            elif len(threes) > 0:
                org1 = random.choice(threes)
                threes.remove(org1)
                twos.append(org1)
            elif len(twos) > 0:
                org1 = random.choice(twos)
                ones.append(org1)
                twos.remove(org1)
            elif len(ones) > 0:
                org1 = random.choice(ones)
                ones.remove(org1)
            if len(fours) > 0:
                fours_sans_org1 = filter(lambda y:y != org1, fours)
                org2 = random.choice(fours_sans_org1)
                fours.remove(org2)
                threes.append(org2)
            elif len(threes) > 0:
                try:
                    threes_sans_org1 = filter(lambda y:y != org1, threes)
                    org2 = random.choice(threes_sans_org1)
                    threes.remove(org2)
                    twos.append(org2)
                except IndexError:
                    pass
            elif len(filter(lambda y:y != org1, twos)) > 0:
                try:
                    twos_sans_org1 = filter(lambda y:y != org1, twos)
                    org2 = random.choice(twos_sans_org1)
                    ones.append(org2)
                    twos.remove(org2)
                except IndexError:
                    pass
            elif len(filter(lambda y:y != org1, ones)) > 0:
                try:
                    ones_sans_org1 = filter(lambda y:y != org1, ones)
                    org2 = random.choice(ones_sans_org1)
                    ones.remove(org2)
                except IndexError:
                    pass
                    #print 'one filtered list %s' % ones_sans_org1
            print 'org1 %s, org2 %s' % (org1.filename, org2.filename)
            if org1 is not None and  org2 is not None:
                print 'crossing org1:%s with org2:%s\n' % (org1.filename, org2.filename, 
                                                                   )
                reproduce(org1, org2, path_to_new_gen)
                return True
            else:
                return False
        #This block handles how much crossing is actually done. If an upper limit
        # is specified via a non None new_gen_size val, crossing will stop after
        #those many offspring have been created. Otherwise orgs will be crossed as
        #long as there are orgs in any of the lists.
        print '------------------------------------------------------------\nCrossing Generation:\n'
        if new_gen_size is not None:
            while(new_gen_size > 0):
                reproduction = chooseTwoToCross(path_to_new_gen)
                if reproduction is True:
                    new_gen_size -= 1
                else:
                    break
        else:
            count = 0
            while ( len(threes) + len(twos) +len(ones)) >= 2:
                chooseTwoToCross(path_to_new_gen)
                count += 1
            print '\nNumber of Orgs in new gen: %s' % count
    def writeQuartilesToCsv(data_dict, dir):
    #os.mkdir(dir)
        data_file =  dir + '/' + 'experiment_data.csv' 
        if os.path.isfile(data_file):
            with open(dir + '/' + 'experiment_data.csv' , 'a') as f:
                fieldnames = ['Generation', 'mean', 'stderr', 'mean collisions', 'collision stderr', 'collisions min', \
                              'collisions max', 'mean wires', 'mean wires stderr' ]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writerow(data_dict)
        else:
            with open(dir + '/' + 'experiment_data.csv' , 'wb') as f:
                fieldnames = ['Generation', 'mean', 'stderr', 'mean collisions', 'collision stderr', 'collisions min', \
                              'collisions max', 'mean wires', 'mean wires stderr']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
    
                writer.writeheader()
                writer.writerow(data_dict)

    crossAndSaveGeneration(path_to_new_gen, new_gen_size)
    #calculateRankings(gen_directory)
    writeQuartilesToCsv(global_quartiles, experiment_directory)


path = '/home/jake/org/Thesis_Stuff/Robot_Data/Development'
thresholdedCrossGeneration(path, path+'/Gen3', path+'/Gen4')
