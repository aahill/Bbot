import json_load_file
import os
from Organism import *
import shutil
import random
import tempfile
from Decoder import *

#import AlternateOrganism

def compare(devo_file):
 #   for root, dir, files in os.walk(directory):
 #       for f in files:
 #           print root +'/' + f 
 #           if f.endswith('.txt'):
    try:
        devo_org = json_load_file.json_load_file (devo_file)
<<<<<<< HEAD
        genome = devo_org.genome
        #devo_org = devo_file
        devo_org = Organism(devo_org.generation, devo_org.generational_index, devo_org.genome_size,
            800, True, devo_org.thread_length, devo_org.mutation_rate, parent1=None, parent2=None,genome=genome,alt_mode=False)
=======
>>>>>>> 88fa4129504ddc9e22e127ee715680c5803163b8

        print "++++++++++++++++++++devo / no devo comparason+++++++++++++++++++++++++++++++++++++"
        print "++++++++++++++++++++development organism+++++++++++++++++++++++++++++++++++++"
        print devo_org.filename
        print "PERFORMANCE", devo_org.performance_1
        print "no. of threads: " + str(len(devo_org.threads))
        print "length of genome: ", len(devo_org.genome)
        print "no. collisions: ", devo_org.collisions
        print "connected_pins: ", [str(pin.number)+pin.group_id for pin in devo_org.connections]
        print "collision events: ", devo_org.collision_events
        assert(len(devo_org.genome) == len(devo_org.instruction_set.genome))
        for thread in devo_org.threads:
            if len(thread.decoded_instructions) == 0: 
                print 'empty thread'
            else:
                print "decoded:",thread.decoded_instructions
                for connection in thread.connected_pins:
                    print connection.group_id, connection.number
            print "-------------------------------------//"
            #print "Org: %s" % org.filename
            print "connections: "
            #for thread in org.threads:
            #    print [i.group_id for i in thread.connected_pins]
            #    print "new thread connections:"
            #    for connection in thread.connected_pins:
            #        print connection.group_id, connection.number
            #    print "-------------------------------------//"
            #break
        print "++++++++++++++++++++non_development organism+++++++++++++++++++++++++++++++++++++\n"
        genome = devo_org.genome
        non_devo_org = Organism(devo_org.generation, devo_org.generational_index, devo_org.genome_size,
            800, True, devo_org.thread_length, devo_org.mutation_rate, parent1=None, parent2=None,genome=genome,alt_mode=True)

        print non_devo_org.filename
        print "no. of threads: " + str(len(non_devo_org.threads))
        print "length of genome: ", len(non_devo_org.genome)
        print "no. collisions: ", non_devo_org.collisions
        print "connected_pins: ", [str(pin.number)+pin.group_id for pin in non_devo_org.connections]
        assert(len(non_devo_org.genome) == len(non_devo_org.instruction_set.genome))

        #for thread in non_devo_org.threads:
        for x in range(len(non_devo_org.threads)):
            thread = non_devo_org.threads[x]
            devo_thread = devo_org.threads[x]
            assert (thread.decoded_instructions == devo_thread.decoded_instructions)
            if len(thread.decoded_instructions) == 0: 
                print 'empty thread'
                assert len(non_devo_org.connections) > 0
                assert len(devo_org.connections) > 0
            else:
                print "decoded:",thread.decoded_instructions
                for connection in thread.connected_pins:
                    print connection.group_id, connection.number
            print "-------------------------------------//"
    except IOError:
        print 'IO error'

    return non_devo_org
#for x in range(30000):
#    #g = generate_viable()
#    g = Organism(0, 0,560,2,True,80,2000)
#    compare(g)
#    print (str(x) +" completed")#, end="\r")
#g = Organism(0, 0,560,2,True,80,2000)
<<<<<<< HEAD
#g = generate_viable()
#compare(g)
#compare('/home/jake/org/Thesis_Stuff/Simulation_Data/Random_Selection_Collisions/Gen10/10_9_9_5_9_4/10_9_9_5_9_4.txt')
compare("/Users/Aaron/Projects/ShakingJakeyBakey/Braitenbot_Data/Robot_Data/Development/Gen1/1_9_ _ _ _ /1_9_ _ _ _ .txt")
=======
path = '/home/jake/org/Thesis_Stuff/Robot_Data/Development/Gen1'
for root, dirs, files in os.walk(path):
    for f in files:
        if f.endswith('.txt'):
            compare(root+'/'+f)
#compare('/home/jake/org/Thesis_Stuff/Robot_Data/Development')
#compare("/Users/Aaron/Projects/ShakingJakeyBakey/Braitenbot_Data/Simulation_Data/Random_Selection_Collisions/Gen10/10_1_9_6_9_3/10_1_9_6_9_3.txt")
>>>>>>> 88fa4129504ddc9e22e127ee715680c5803163b8
