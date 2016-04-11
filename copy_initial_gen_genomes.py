import random
import json_load_file
import os
from Organism import *
import shutil
import random
import tempfile
from Decoder import *

#import AlternateOrganism

def compare(devo_file, outpath, altmode):
    original_org = json_load_file.json_load_file (devo_file)
    genome = original_org.genome
    # This is done to get the potential_locaions list
    new_org = Organism(original_org.generation, original_org.generational_index, original_org.genome_size,
                       2, True, original_org.thread_length, original_org.mutation_rate, parent1=None, parent2=None,genome=genome,alt_mode=altmode)
    xover_locations = new_org.instruction_set.potential_locations
    # set the xover points to 0
    for i in genome:
        i.crossover_point = 0

    counter = 0
    while counter != 2:
        try:
            rand_index = random.choice(xover_locations)
            print(rand_index)
            genome[rand_index].crossover_point = 1
            xover_locations.remove(rand_index)
            counter +=1
        except IndexError:
            pass
    print([i.crossover_point for i in genome])
    restricted_org = Organism(original_org.generation, original_org.generational_index, original_org.genome_size,
                              2, False, original_org.thread_length, original_org.mutation_rate, parent1=None, parent2=None,genome=genome,alt_mode=altmode)

    restricted_org.save_to_file(outpath)
path = '/home/jake/org/Thesis_Stuff/Robot_Data/Development/Gen1'
outpath =  '/home/jake/org/Thesis_Stuff/Simulation_Data/Random_Selection_Fixed_Xover_Devo_OLD_GENOMES/Gen1'

for root, dirs, files in os.walk(path):
    for f in files:
        if f.endswith('.txt'):
            compare(root+'/'+f, outpath, False )
#compare('/home/jake/org/Thesis_Stuff/Robot_Data/Development')
#compare("/Users/Aaron/Projects/ShakingJakeyBakey/Braitenbot_Data/Simulation_Data/Random_Selection_Collisions/Gen10/10_1_9_6_9_3/10_1_9_6_9_3.txt")
