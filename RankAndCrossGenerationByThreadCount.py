__author__ = 'JakeBrawer'
from json_load_file import json_load_file
import random
import Organism
import HoboAnalysis
import os
import math
import datetime
import csv
import gc
global_quartiles = {}

#INPUT: list_of_vals-- list cont
def calculateStdError(list_of_vals, average):
    stddev = 0.0
    diffsquared = 0.0
    sum_diffsquared = 0.0
    print '\n--------------------------------------------------\nCalculating the Std Error of the mean: '
    for val in list_of_vals:
        diffsquared = (val- average)**2.0
        sum_diffsquared += diffsquared 
        print 'Org mean perf: %s Pop mean: %s Diffsqrd: %s SumDiffsqrd: %s ' % (val, average, diffsquared, sum_diffsquared)
    stddev = ((sum_diffsquared)/len(list_of_vals))**(1.0/2.0)
    stderror = stddev / (len(list_of_vals)**(1.0/2.0))
    print 'Stddv: %s  StdErr: %s\n------------------------------------------------------------\n ' % (stddev, stderror)
    #print(numpy.sqrt(numpy.var(list_of_vals)))
    return stderror

#INPUT: experiment_directory -- direcotry containing all the gens for the given experiment
     #gen_directory -- directory containing subdirectories of agents in a given generation
     #  path_to_new_generation -- where you want the direcotry containing new dir
     #  *new_gen_size --(OPTIONAL) upperlimit on number of individuals in new generation
#OUTPUT: A direcory containing individuals from the next generation
def thresholdedCrossGeneration(experiment_directory, gen_directory,path_to_new_gen,*new_gen_size):
    unpickled_orgs = []# temporarily holds unpickled orgs
    try:
        new_gen_size = int( new_gen_size[0]) #turns the input (a tuple) into an int
    except IndexError:
        new_gen_size = None #No size input given

    #INPUT: Directory containing gen to be crossed
    #OUTPUT: Calculates performance thresholds based on the mean pop. performance
            #orgs < Q1 dont reproduce, Q1<= org < Q2 can reproduce once, Q2 <= org <Q3
            # twice, etc.
    def evaluateGenerationPerformance(gen_directory):
        global global_quartiles
        num_threads_per_org = [] 
        mean_threads_per_pop = 0
        list_of_vals = []
        y = []
        #walks through files belonging to an organism, one org at a time
        print 'Active Threads per org:\n'
        for root, dir, files in os.walk(gen_directory):
            for f in files:
                print 'File',
                try:
                    y.append(f)
                    if f.endswith('.pkl') or f.endswith('.txt'):
                        org = json_load_file(root + '/' + f)
                        #print  root + '/'+ f
                        print org.filename
                        print "genome length", len(org.genome) 
                        # This stores the number of active threads per org in org.performance_1,
                        # which is used to rank the organism later on.
                        thread_count = 0
                        for thread in org.threads:
                            print 'thread len.:',len(thread.connected_pins)
                            print "thread binary len:", len(thread.binary)
                            if len(thread.connected_pins) > 0:
                                thread_count += 1
                        org.performance_1 = thread_count
                        print '\nthread count', thread_count
                        print
                        num_threads_per_org.append(org.performance_1)
                except AttributeError:
                    print 'Error'
                    pass
                try:
                    unpickled_orgs.append(org)
                except AttributeError:
                    print 'append error'
                    pass
        print'\n mean performances for each org in population:', num_threads_per_org
        try:
            mean_threads_per_pop = sum(num_threads_per_org)/float(len(num_threads_per_org)) #cast as a float to get float quotient
        except ZeroDivisionError:
            mean_threads_per_pop = 0 
        #Saves quartile information and stdev of pop mean to a dict
        quartiles = {'Generation': unpickled_orgs[0].generation, 'mean_threads': mean_threads_per_pop, \
                     'stderr': calculateStdError(num_threads_per_org, mean_threads_per_pop),\
                     'gen_size': len(unpickled_orgs), 'mode': max(set(num_threads_per_org), key=num_threads_per_org.count),\
                     'min': min(num_threads_per_org), 'max': max(num_threads_per_org)}
        print '\nquartiles: %s\n' % quartiles  
        global_quartiles = quartiles
        return quartiles

    #INPUT: dir containing gen of interest
    #OUTPUT: Sorts organisms into lists that denote how many offspring they
            # can potentially create
    def calculateRankings(gen_directory):
        evaluateGenerationPerformance(gen_directory)
        #Sorts orgs from Orgs with most threads to Orgs with least threads
        sorted_orgs = sorted(unpickled_orgs, key=lambda x: x.performance_1,\
                             reverse=True)
        ranking = []
        while len(sorted_orgs) >0:
            ranking.append([sorted_orgs.pop(0), sorted_orgs.pop(0)])

        for i in ranking:
            for r in i:
                print r.performance_1
        
        return ranking
   
    #INPUT: path_to_new_gen: where to save the new gen data
        #   new_gen_size: the upperlimit (if any) to the new gen
    #OUTPUT: New generation of orgs saved to path_to_new_gen 
    def crossAndSaveGeneration(path_to_new_gen,new_gen_size):
        #These lines calculate the quartiles, and then save each area 
        #above a quartile to its own list
        rankings = calculateRankings(gen_directory)
        fours = rankings.pop(0)
        threes = rankings.pop(0)
        twos = rankings.pop(0)
        ones = rankings.pop(0)
        #INPUT: path_to_new_gen -- see above
        #OUTPUT: Crosses to orgs (if any are present in the above lists) 
        # and sve their offspring to a direcotry located in path_to_new_gen
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
                Organism.reproduce(org1, org2, path_to_new_gen)
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
   #INPUT: quartile_dict: the dict containing quartile info
         # dir: path_to_new_gen
   #OUTPUT: a CSV file saved to dir containing quartile data 
    def writeQuartilesToCsv(data_dict, dir):
        #os.mkdir(dir)
        data_file =  dir + '/' + 'experiment_data.csv' 
        if os.path.isfile(data_file):
            with open(dir + '/' + 'experiment_data.csv' , 'a') as f:
                fieldnames = ['Generation', 'mean_threads', 'stderr','gen_size', 'mode', 'min', 'max' ]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writerow(data_dict)
        else:
            with open(dir + '/' + 'experiment_data.csv' , 'wb') as f:
                fieldnames = ['Generation', 'mean_threads', 'stderr','gen_size', 'mode', 'min', 'max' ]
                writer = csv.DictWriter(f, fieldnames=fieldnames)

                writer.writeheader()
                writer.writerow(data_dict)

            #w = csv.DictWriter(f, quartile_dict.keys())
            #w.writeheader()
            #w.writerow(quartile_dict)

    crossAndSaveGeneration(path_to_new_gen, new_gen_size)
    ##calculateRankings(gen_directory)
    writeQuartilesToCsv(global_quartiles, experiment_directory)
    gc.collect()


#thresholdedCrossGeneration('/home/jake/Dropbox/BraitenbotCode/Summer2015/2015-07-22- EvolvingThreadNumber/Selection_High_Mutation_Rate/Population_1', '/home/jake/Dropbox/BraitenbotCode/Summer2015/2015-07-22- EvolvingThreadNumber/Selection_High_Mutation_Rate/Population_1/Gen11' ,'/home/jake/Dropbox/BraitenbotCode/Summer2015/2015-07-22- EvolvingThreadNumber/Selection_High_Mutation_Rate/Population_1/Gen12' )
