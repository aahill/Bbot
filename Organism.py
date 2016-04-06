# -*- coding: utf-8 -*-
from BaseAndInstructionSet import *
from Decoder import Decoder
import random
import os
import jsonpickle
#*Input:* thread_decoder, a Decoder object\\
#*Output:* a Thread, stores a section of an Organism’s InstructionSet and builds connections from it, whcih are also stored.\\

class Thread(object):
    def __init__(self, thread_decoder):
        #stores the binary of the thread
        self.binary = []
        #list of tuples containing the directional movement instructions encoded in the thread
        #(once the thread has been decodex)
        self.decoded_instructions = []
        #the connected pins as a result of the decoded instructions
        self.connected_pins = []
        #the decoder object to be used by the Thread
        self.decoder = thread_decoder

    # simply calls the decoder to decode the thread's instructions
    def decode(self):
        self.decoded_instructions = self.decoder.generate_coords(self.binary)
"""*Input:* generation, int,  the generation the org belongs to.
 generational index, int, tracks the order in which the orgs in a gen were created
 parent1=None, Organism, One of the orgs parents, defaults to None
 parent2=None, Organism, The other parent, also defaults to none
 genome=None: An InstructionSet, defaults to None.
*Output:* An Organism object. It keeps track of an individual’s genome, lineage,
and experimental performance, as well as builds its phenotype from the genome."""
class Organism(object):
      def __init__(self, generation, generational_index,genome_size, num_crossover_points, unrestricted_crossover_point_distribution, thread_length,mutation_rate, parent1=None, parent2=None, genome=None, alt_mode=False):
          #conditionally import the correct pin groups
          self.alt_mode = alt_mode 
          if self.alt_mode:
                from AlternatePinAndPinGroup import *
          else:
                from PinAndPinGroup import *
          # store perfromance on behavioral task: raw performance and normalized performance
          self.performance_1 = None
          self.performance_2 = None
          #lists where collisions occur
          self.collision_events = []
          self.reproduction_possibilities = None
          self.generation = generation
          #variables to track lineage info and generate file name
          self.generational_index = generational_index
          self.thread_length = thread_length
          self.genome_size = genome_size
          #store the number of collisions between threads
          self.collisions = 0
          self.mutation_rate = mutation_rate
          # store organizational and naming information
          #NOTE: no longer saves a reference to parent org object
          #as that resulted in gigundus file sizes
          #try-except block necessary because parents may be None
          try:
              self.parent1_generation = parent1.generation
              self.parent1_generational_index = parent1.generational_index
              self.parent2_generation = parent2.generation
              self.parent2_generational_index = parent2.generational_index
          except AttributeError:
              pass
          self.filename = self.set_file_name()
          thread_length = thread_length
          self.instruction_set = InstructionSet(genome_size, num_crossover_points,unrestricted_crossover_point_distribution, thread_length, mutation_rate)
          #This conditional is recquired for threads to build with
          # recombinated genome
          if genome is None: self.genome = self.instruction_set.genome
          else: self.genome = genome
          self.decoder = Decoder()
          # initialize pin groups
          self.group1 = Group1()
          self.group2 = Group2()
          self.group3 = Group3()
          self.group4 = Group4()
          self.group5 = Group5()
          self.group6 = Group6()
          self.groupPl = GroupPl()
          self.groupRl = GroupRl()
          self.groupRr = GroupRr()
          self.groupPr = GroupPr()
          self.groupBl = GroupBl()
          self.groupBr = GroupBr()
          self.groupFl = GroupFl()
          self.groupFr = GroupFr()
          # organize pin groups into a single list
          self.pinGroups = [ self.groupBl, self.group1, self.group2, self.group3, self.groupFl, self.group4, self.group5, 
              self.group6, self.groupBr, self.groupPl, self.groupRl, self.groupRr, self.groupFr, self.groupPr, ]
          # threads will eventually be created and appended to the thread list
          self.threads = []
          # store the pins currently connected in the organism (in no specific order)
          self.connections = []

          self.create_threads(thread_length)
          self.generate_thread_instructions()
          self.build_thread_coordinates()

      """
      creates the string for the organism's filename
      """
      def set_file_name(self):
          # create the filename based on the generational and lineage data
          try:
              filename = (str(self.generation) + "_" +
                          str(self.generational_index) + "_" +
                          str(self.parent1_generation) + "_" +
                          str(self.parent1_generational_index) + "_" +
                          str(self.parent2_generation) + "_" +
                          str(self.parent2_generational_index))
          except AttributeError:
              filename = (str(self.generation) + "_" +
                          str(self.generational_index) + "_" +
                          str(" ") + "_" +
                          str(" ") + "_" +
                          str(" ") + "_" +
                          str(" "))
          return filename
      
      # save the Organism file using jsonpickle and a prespecified path
      def save_to_file(self, path):
          if not os.path.exists(path+"/"+self.filename):
              dir = os.mkdir(path+"/"+self.filename)
          with open(path+"/"+self.filename+"/"+self.filename+".txt", 'wb') as output:
              data = jsonpickle.encode(self)
              output.write(data)
      # divides an organism's genome into threads of 'thread_length'
      def create_threads(self, thread_length):
          for genome_index in range(0, len(self.genome), thread_length):
              # iteratively create lists of base chars of size 'thread_length'
              # these lists will become the binary for the threads
              new_thread = Thread(self.decoder)
              try:
                  # get the chars from each base in the segment of the instruction code being examined
                  thread_binary = ([self.genome[i].char for i in range(genome_index,  genome_index+thread_length)])
                  new_thread.binary = thread_binary
                  self.threads.append(new_thread)
              # in the event of not having enough bases to create an entire thread
              # let the thread be truncated, and stop copying over bases, and append it to the list of threads
              except IndexError:
                  thread_binary = ([self.genome[i].char for i in range(genome_index, len(self.genome))])
                  new_thread.binary = thread_binary
                  self.threads.append(new_thread)
      #*Input:* Nothing\\
      #*Output:* Nothing\\
      #*Side Effect:* The binary instructions for each Thread in self.threads (see above) is decoded into corresponding coordinate instructions (see Decoder).\\
      def generate_thread_instructions(self):
          for thread in self.threads:
              # instructions are xy coordinate points to plug into the pinGroups
              thread.decode()
              #print thread.decoded_instructions
      
      #*Input:* Nothing   
      #*Output:* Nothing    
      #*Side Effect:* Determines the pins connected as dictated by the coordinates of each thread.    
      #*Process:* Each Thread is built (i.e.  their decoded_instructions are used to accesses PinGroups and Pins (see below))   
      # using a round-robin approach. This done by simultaneously building each thread, one index at a    
      # time. Threads that are actively being built are stored in the list active_threads. Threads are    
      # removed from active_threads if they collided with with a previously built Thread, for trying    
      #to accesses out of bounds Pins, for having only one valid pin, etc. Pins are accessed using the    
      # xyz coordinates stored in Thread.decoded_instructions, where x corresponds to the PinGroup, y   
      # corresponds to a specific Pin in the PinGroup, and z corresponding to another Pin within that   
      # same PinGroup-- the origin of the next wire. After each Thread is built, and therefore    
      #active_threads is empty, threads are checked to make sure there are no connections without a   
      # terminal pin.
      def build_thread_coordinates(self):
          # threads will be temporarily copied into a separate list of running threads, to determine when the process of
          # making their connections is completed
          running_threads = []
          for thread in self.threads:
          # we only want to use the the threads that connect at least two pins.
              # this is represented by the number of instructions in said thread
              if len(thread.decoded_instructions) >= 2:
                  running_threads.append(thread)
      
      # using a round-robin approach attempt to pair a thread's coordinate to a pin. when the thread fails for
      # some reason (i.e. collision between threads, or coordinates not corresponding to an available pin)
      # the thread will not be runnable and be taken from the running_threads list
          index = 0
          # A deepcopy of running_threads that we are free to modify
          # threads are removed from active_thread when they are no longer able to make connections
          active_threads = [i for i in running_threads]
          while len(active_threads) > 0:
              # This builds each thread at the current index value
              for running in running_threads:
      
                  error_encountered = False
                  # declare variables for finding and storing a selected pin
                  accessed_output_pin = None
                  new_connection_origin = None
                  if running in active_threads:
                      try:
                          # get the specific pin coordinates from the instruction and translate it to make it a valid pin
                          pin_coordinates = running.decoded_instructions[index]
                          accessed_pin_group = self.pinGroups[pin_coordinates[0]]
                          accessed_output_pin = accessed_pin_group.get_input(
                              pin_coordinates[1])
                          #if the pin coordinates specifiy one, get a connection origin
                      except IndexError:
                          error_encountered = True
                          active_threads.remove(running)
      
                      if not error_encountered and len(pin_coordinates) == 3:
                          try:
                              new_connection_origin = accessed_pin_group.get_output(
                                  pin_coordinates[2])
                          except IndexError:
                              active_threads.remove(running)
                      # even if an index error is not encounter, it is possible that the pin exists but has been taken
                      try:
                          # ensure the pin hasn't been 'taken' by another thread already (if not generating an alternate organism)
                          # using the 'in' keyword works, but consider iterating through the list manually and comparing the pin's id and number
                          if accessed_output_pin != None:
                              if accessed_output_pin in self.connections:
                                  self.collisions += 1
                                  self.collision_events.append(
                                      "collision getting pin at: " + str(
                                          pin_coordinates[0]) + "," + str(
                                              pin_coordinates[1]))
                                  if not self.alt_mode:
                                      raise LookupError(
                                          "Connection failed: pin already connected")
                              self.connections.append(accessed_output_pin)
                              running.connected_pins.append(accessed_output_pin)
                      except LookupError:
                          if running in active_threads:
                              active_threads.remove(running)
      
                      try:
                          if new_connection_origin != None:
                              #track the collision regardless of mode, but only handle it (via raise lookupError ) if not in alt mode
                              if new_connection_origin in self.connections:
                                  self.collisions += 1
                                  self.collision_events.append(
                                      "collision getting pin at: " + str(
                                          pin_coordinates[0]) + "," + str(
                                              pin_coordinates[2]))
                                  #set the new_connection_origin back to available
                                  if not self.alt_mode:
                                      raise LookupError(
                                          "Connection failed: pin already connected!")
      
                              self.connections.append(new_connection_origin)
                              running.connected_pins.append(new_connection_origin)
                      except LookupError:
                          if self.alt_mode:
                              assert False
                          # if a thread only has two pins, then it cannot create a connection to pins outside of the initial
                          # group, and each pin must be made available
                          # if len(running.connected_pins) == 2:
                          #     error_encountered = True
                          #     for x in range(len(running.connected_pins)):
                          #         # set the pin's availability to 'true'
                          #         running.connected_pins[x].available = True
                          #         # remove the pin from the thread's & organism's group of connected pins
                          #         #self.connections.remove(running.connected_pins[x])
                          #         for n in range(len(self.connections)):
                          #             if (self.connections[n].group_id == running.connected_pins[x].group_id and
                          #                 self.connections[n].number == running.connected_pins[x].number):
                          #                 del self.connections[n]
                          #                 break
                          #
                          #     # wipe the running thread's connected pins since it only contains two pins,
                          #     # which is not a complete connection
                          #     running.connected_pins = []
                          if running in active_threads:
                              active_threads.remove(running)
      
              index += 1  # Starts loop again at next index for all threads
      
          for running in self.threads:
              if len(running.connected_pins) % 2 != 0:  # and len(running.connected_pins) >= 1:
                  to_remove = running.connected_pins[-1]
                  to_remove.available = True
                  running.connected_pins.remove(to_remove)
                  self.connections.remove(to_remove)
      
      def is_viable(self):
          connected_pins = []
      
          def check1():
              for connected_pin_group in connected_pins:
                  if (#("bl" in connected_pin_group and "fr" in connected_pin_group) or
                         # ("fl" in connected_pin_group and "br" in connected_pin_group) or
                          ("bl" in connected_pin_group and "br" in connected_pin_group ) or
                          ("fl" in connected_pin_group and "fr" in connected_pin_group)):
                      return True
              return False
      
          def check3():
              for connected_pin_group in connected_pins:
                  if ((#"rr" in connected_pin_group or
                               #"rl" in connected_pin_group or
                               "pl" in connected_pin_group or
                               "pr" in connected_pin_group) and
                          ("fl" in connected_pin_group or
                                   "bl" in connected_pin_group or
                                   "fr" in connected_pin_group or
                                   "br" in connected_pin_group)):
      
                      return True
                  return False
      
          def check4():
              try:
                   if connected_pins[0] ==connected_pins[1] and connected_pins\
                      [len(connected_pins) - 1]\
                            ==  connected_pins[len(connected_pins) - 2]: 
                          False
                   else:
                          True
              except(IndexError):
                  pass
      
          for t in self.threads:
              if len(t.connected_pins) > 0:
                  # make a set out of the connected pins of the thread
                  t_set = set([pin.group_id for pin in t.connected_pins])
                  connected_pins.append(t_set)
                  # loop through the list, and for every group of connected pins, check the \
                      #intersection of it &
                  # and its neighbor.
                  # If there is an intersection, place the union of the two sets in the connected_pin
                  # group and remove the two original sets. This will determine if the correct pins are wired
                  # to create a viable phenotype
                  for x in range(len(connected_pins)-1):
                      if len(set(connected_pins[x]).intersection(set(connected_pins[x+1]))) > 0:
                          merged_set = set(connected_pins[x]).union(connected_pins[x+1])
                          connected_pins.remove(connected_pins[x+1])
                          connected_pins.remove(connected_pins[x])
                          connected_pins.append(merged_set)
                          # check to see if the length of the connected_pin set has changed due\
                              #to appends and removes
                          if x < len(connected_pins)-1:
                              break
      
      
          if check1() and check3( ):  # and check2():
              #print "connected pins: ", connected_pins
              return True
          else:
              return False
      
      
      
      

def reproduce(org1, org2, path):
    dom = random.choice([org1, org2])  # Parent whose crossover points are being used
    rec = filter(lambda y: y != dom, [org1, org2])
    rec = rec[0]# Other parent
    child1_genome = []
    gen_count = 0
    index = 0
    # This is how the offsprings genome is made
    #allows for crossing over at nonhotspots at 1/100000 chance.
    dom_genome_copy = True
    dom_stuff =[]
    rec_stuff=[]
    while index <= len(dom.genome) - 1:
        if dom_genome_copy:
            child1_genome.append(dom.genome[index])
            dom_stuff.append(dom.genome[index].char)
            rec_stuff.append(rec.genome[index].char)
            if dom.genome[index].crossover_point == 1:
                dom_stuff.append('HERE')
                rec_stuff.append('HERE')
                dom_genome_copy = False
            index += 1
        else:
            child1_genome.append(rec.genome[index])
            dom_stuff.append(rec.genome[index].char)
            rec_stuff.append(rec.genome[index].char)
            if rec.genome[index].crossover_point == 1:
                dom_stuff.append('HERE')
                rec_stuff.append('HERE')
                dom_genome_copy = True
            index +=1

    # This takes care of  of saving the Org.
    # if the path specified does not exist a new directory
    # will be created

    count = 0
    if os.path.isdir(path):
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                count += 1
        child_instruction_set = InstructionSet(dom.genome_size, 2,True,dom.thread_length, dom.mutation_rate)
        child_instruction_set.setGenome(child1_genome)
        child_instruction_set.mutate()
        if dom.alt_mode:
            child1 = Organism(dom.generation + 1, count,dom.genome_size,2,True,dom.thread_length,dom.mutation_rate, dom, rec, child_instruction_set.genome,alt_mode=True)
        else:
            child1 = Organism(dom.generation + 1, count,dom.genome_size,2,True,dom.thread_length,dom.mutation_rate, dom, rec, child_instruction_set.genome,alt_mode=False)
    else:
        os.makedirs(path)
        child_instruction_set = InstructionSet(dom.genome_size, 2,True,dom.thread_length, dom.mutation_rate)
        child_instruction_set.setGenome(child1_genome)
        child_instruction_set.mutate()
        if dom.alt_mode:
            child1 = Organism(dom.generation + 1, count,dom.genome_size,2,True,dom.thread_length,dom.mutation_rate, dom, rec, child_instruction_set.genome,alt_mode=True)
        else:
            child1 = Organism(dom.generation + 1, count,dom.genome_size,2,True,dom.thread_length,dom.mutation_rate, dom, rec, child_instruction_set.genome,alt_mode=False)
    child1.save_to_file(path)
    return child1
#Generates a viable organism based on the is_viable check
def generate_viable():
    # writes a 'progress bar' to the console
    def progress(x):
        out = '\r %s organisms tested' % x  # The output
        print out,

    genomes_tested = 0
    finished = False
    while not finished:
        test = Organism(0, 0,560,2,True,80,2000)
        if test.is_viable():
            print "-------------------------------------//"
            print "connections: "
            for thread in test.threads:
                print "new thread connections:"
                for connection in thread.connected_pins:
                    print connection.group_id, connection.number
            print "-------------------------------------//"
            finished = True
        else:
            del test
            genomes_tested += 1
            progress(genomes_tested)
