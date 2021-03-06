#a utility that unpickles all pickled organisms in a directory, and prints each threads' connections.
#The genome is then 
#and compares the output to the current code

import json_load_file
import os
from Organism import *
import shutil
import random
import tempfile
from Decoder import *

def compare(directory):
    for root, dir, files in os.walk(directory):
        for f in files:
            print root +'/' + f 
            if f.endswith('.txt'):
			    try:
			        devo_org = json_load_file.json_load_file (root+'/'+f)
			        genome = devo_org.genome
			        new_devo_org = Organism(devo_org.generation, devo_org.generational_index, devo_org.genome_size,
			            800, True, devo_org.thread_length, devo_org.mutation_rate, parent1=None, parent2=None,genome=genome,alt_mode=False)

			        print "++++++++++++++++++++comparing pickled threads to threads produced from current code+++++++++++++++++++++++++++++++++++++"
			        print "++++++++++++++++++++pickled organism+++++++++++++++++++++++++++++++++++++"
			        print "no. of threads: " + str(len(devo_org.threads))
			        print "length of genome: ", len(devo_org.genome)
			        print "no. collisions: ", devo_org.collisions
			        print "connected_pins: ", [str(pin.number)+pin.group_id for pin in devo_org.connections]
			        print "collision events: ", devo_org.collision_events
			        #assert(len(devo_org.genome) == len(devo_org.instruction_set.genome))
			        for thread in devo_org.threads:
			            if len(thread.decoded_instructions) == 0: 
			                print 'empty thread'
			            else:
			                print "decoded:",thread.decoded_instructions
			                for connection in thread.connected_pins:
			                    print connection.group_id, connection.number
			            print "-------------------------------------//"
	
			        print "++++++++++++++++++++newly generated organism+++++++++++++++++++++++++++++++++++++\n"
			        genome = devo_org.genome
			        new_devo_org = Organism(devo_org.generation, devo_org.generational_index, devo_org.genome_size,
			            800, True, devo_org.thread_length, devo_org.mutation_rate, parent1=None, parent2=None,genome=genome,alt_mode=False)

			        print "no. of threads: " + str(len(new_devo_org.threads))
			        print "length of genome: ", len(new_devo_org.genome)
			        print "no. collisions: ", new_devo_org.collisions
			        print "connected_pins: ", [str(pin.number)+pin.group_id for pin in new_devo_org.connections]
			        assert(len(new_devo_org.genome) == len(new_devo_org.instruction_set.genome))

			        #for thread in new_devo_org.threads:
			        for x in range(len(new_devo_org.threads)):
			            thread = new_devo_org.threads[x]
			            devo_thread = devo_org.threads[x]
			            assert (thread.decoded_instructions == devo_thread.decoded_instructions)
			            if len(thread.decoded_instructions) == 0: 
			                print 'empty thread'
			                assert len(new_devo_org.connections) > 0
			                assert len(devo_org.connections) > 0
			            else:
			                print "decoded:",thread.decoded_instructions
			                for connection in thread.connected_pins:
			                    print connection.group_id, connection.number
			            print "-------------------------------------//"
			    except IOError:
			        print 'IO error'

compare("/Users/Aaron/Projects/Braitenbot_Data/Robot_Data/Development/Gen1/")