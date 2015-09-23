__author__ = 'JakeBrawer'
from json_load_file import json_load_file
import random
from  Organism import *
import HoboAnalysis
import os
import math
import datetime
import csv
import gc
global_quartiles = {}
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
