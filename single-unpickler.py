import json_load_file
import os
from Organism import *
import shutil
import random
import tempfile
from Decoder import *

verified_genome = "010010100001011101001011100100011111100010011001"+\
    "010000011011101000111100111111110011101101011011101100011110001010110"+\
    "111001001111110001010000101100001110111011011110010100011101100000101"+\
    "011011101010011001100010100011001001011010000100011101011000011010100"+\
    "011110111000001110111110111011011111011110001001001100001100101001100"+\
    "110100111111110100010001111011011110011010111010110000000101011101011"+\
    "000001010010011101100100010001110000111000101000100101001011101000010"+\
    "101100011000111000010100101100011110001001011110111111001010111101100"+\
    "10110101110111101010000111100"
Verified_genome = list(verified_genome)

#genome with the first thread repeated 7 times; used to force collision with motor/sensor groups
#replicated_genome='01100001101010001111011100000111011111011101101111101111000100100110000110010100011000011010100011110111000001110111110111011011111011110001001001100001100101000110000110101000111101110000011101111101110110111110111100010010011000011001010001100001101010001111011100000111011111011101101111101111000100100110000110010100011000011010100011110111000001110111110111011011111011110001001001100001100101000110000110101000111101110000011101111101110110111110111100010010011000011001010001100001101010001111011100000111011111011101101111101111000100100110000110010100'
#another genome with a thread (which?) repeaded 7 times; used to force collision with non motor/sensor groups
replicated_genome='01000010001110100001111101001111110100111011110000010100011110010000011010010101010000100011101000011111010011111101001110111100000101000111100100000110100101010100001000111010000111110100111111010011101111000001010001111001000001101001010101000010001110100001111101001111110100111011110000010100011110010000011010010101010000100011101000011111010011111101001110111100000101000111100100000110100101010100001000111010000111110100111111010011101111000001010001111001000001101001010101000010001110100001111101001111110100111011110000010100011110010000011010010101'
def unpickle_and_print(f):
 #   for root, dir, files in os.walk(directory):
 #       for f in files:
 #           print root +'/' + f 
 #           if f.endswith('.txt'):
    try:
        org = json_load_file.json_load_file (f)
        org.decoder = Decoder()
        genome = org.genome
        #for x in range(len(genome)):
        #    genome[x].char = replicated_genome[x]

        #org.__init__(org.generation, org.generational_index, org.genome_size,
        #    800, True, org.thread_length, org.mutation_rate, parent1=None, parent2=None,genome=genome)
        #print [i.crossover_point for i in org.genome]
        co_points =0
        for i in org.genome:
            co_points += i.crossover_point
        print org.filename
        print "no. of threads: " + str(len(org.threads))
        print "length of genome: ", len(org.genome)
        print "no. collisions: ", org.collisions
        print "connected_pins: ", [str(pin.number)+pin.group_id for pin in org.connections]
        print "co points:", co_points
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
            #    for connection in thread.connected_pins::
            #        print connection.group_id, connection.number
            #    print "-------------------------------------//"
            #break
    except IOError:
        print 'error'


#unpickle_and_print('/home/jake/org/Thesis_Stuff/Simulation_Data/Random_Selection_Collisions/Gen10/10_9_9_5_9_4/10_9_9_5_9_4.txt')
unpickle_and_print('/home/jake/org/Thesis_Stuff/Robot_Data/Non_Development/Gen1/1_0_ _ _ _ /1_0_ _ _ _ .txt')
unpickle_and_print('/home/jake/org/Thesis_Stuff/Simulation_Data/Random_Selection_Non_Development/Gen1/1_0_ _ _ _ /1_0_ _ _ _ .txt')
#quickly load and print a single organism
def run(f):
    try:
        org = json_load_file.json_load_file(f)
        #org.decoder = Decoder()
        #gen = org.genome
        #org.__init__(org.generation, org.generational_index, org.genome_size,
        #    800, True, org.thread_length, org.mutation_rate, parent1=None, parent2=None,genome=gen)
    except IOError:
        print 'IOError encountered'
    print "thread collisions: ", org.collisions
#run('/Users/Aaron/Projects/Bbot/Random_Selection/Random_1/Gen10/last_one_testing.txt')
#g = generate_viable()
