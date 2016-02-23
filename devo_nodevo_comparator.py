import json_load_file
import os
from Organism import *
import shutil
import random
import tempfile
from Decoder import *

import AlternateOrganism

def compare(devo_file, non_devo_file):
 #   for root, dir, files in os.walk(directory):
 #       for f in files:
 #           print root +'/' + f 
 #           if f.endswith('.txt'):
    try:
        devo_org = json_load_file.json_load_file (devo_file)
        
        org.decoder = Decoder()
        
        print "++++++++++++++++++++devo / no devo comparason+++++++++++++++++++++++++++++++++++++"
        print "++++++++++++++++++++development organism+++++++++++++++++++++++++++++++++++++"
        print "no. of threads: " + str(len(org.threads))
        print "length of genome: ", len(org.genome)
        print "no. collisions: ", org.collisions
        print "connected_pins: ", [str(pin.number)+pin.group_id for pin in org.connections]
        assert(len(org.genome) == len(org.instruction_set.genome))
        for thread in org.threads:
            if len(thread.decoded_instructions) == 0: 
                print 'empty thread'
            else:
                print "decoded:",thread.decoded_instructions
                for connection in thread.connected_pins:
                    print connection.group_id, connection.number
            print "-------------------------------------//"
            #print "Org: %s" % org.filename
            #print "connections: "
            #for thread in org.threads:
            #    print [i.group_id for i in thread.connected_pins]
            #    print "new thread connections:"
            #    for connection in thread.connected_pins:
            #        print connection.group_id, connection.number
            #    print "-------------------------------------//"
            #break
        print "++++++++++++++++++++non_development organism+++++++++++++++++++++++++++++++++++++"
        genome = devo_org.genome
        non_devo_org = AlternateOrganism.Organism(non_devo_org.generation, non_devo_org.generational_index, non_devo_org.genome_size,
            800, True, non_devo_org.thread_length, non_devo_org.mutation_rate, parent1=None, parent2=None,genome=genome)

        print "no. of threads: " + str(len(org.threads))
        print "length of genome: ", len(org.genome)
        print "no. collisions: ", org.collisions
        print "connected_pins: ", [str(pin.number)+pin.group_id for pin in org.connections]
        assert(len(org.genome) == len(org.instruction_set.genome))
        for thread in org.threads:
            if len(thread.decoded_instructions) == 0: 
                print 'empty thread'
            else:
                print "decoded:",thread.decoded_instructions
                for connection in thread.connected_pins:
                    print connection.group_id, connection.number
            print "-------------------------------------//"
    except IOError:
        print 'error'


compare('/home/jake/org/Thesis_Stuff/Simulation_Data/Random_Selection_Collisions/Gen10/10_9_9_5_9_4/10_9_9_5_9_4.txt')
