__author__ = 'JakeBrawer'
#from json_load_file import json_load_file
import json
import jsonpickle
import random
from  AlternateOrganism import *
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
    stddev = ((sum_diffsquared)/len(list_of_vals))**(1.0/2.0)
    stderror = stddev / (len(list_of_vals)**(1.0/2.0))
    print 'Stddv: %s  StdErr: %s\n------------------------------------------------------------\n ' % (stddev, stderror)
    #print(numpy.sqrt(numpy.var(list_of_vals)))
    return stderror
def thresholdedCrossGeneration(experiment_directory, gen_directory,path_to_new_gen,*new_gen_size):
    unpickled_orgs = []# temporarily holds unpickled orgs
    try:
        new_gen_size = int( new_gen_size[0]) #turns the input (a tuple) into an int
    except IndexError:
        new_gen_size = None #No size input given
    
    def calculateRankings(gen_directory):
        evaluateGenerationPerformance(gen_directory)
        sorted_orgs = sorted(unpickled_orgs, key=lambda x: (x.performance_3 + x.performance_3)/2.0,\
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
    

    crossAndSaveGeneration(path_to_new_gen, new_gen_size)
    #calculateRankings(gen_directory)
    writeQuartilesToCsv(global_quartiles, experiment_directory)