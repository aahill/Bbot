# -*- coding: utf-8 -*-
from BaseAndInstructionSet import *
from Decoder import Decoder
from PinAndPinGroup import *
import random
import os
import jsonpickle
class Thread(object):
    def __init__(self, thread_decoder):
        self.binary = []
        self.decoded_instructions = []
        self.connected_pins = []
        self.decoder = thread_decoder

    # simply calls the decoder to decode the thread's instructions
    def decode(self):
        self.decoded_instructions = self.decoder.generate_coords(self.binary)
class Organism(object):
      def __init__(self, generation, generational_index,genome_size, num_crossover_points, unrestricted_crossover_point_distribution, thread_length,mutation_rate, parent1=None, parent2=None, genome=None):
          # store perfromance on behavioral task
          self.performance_1 = None
          self.performance_2 = None
          self.reproduction_possibilities = None
          self.generation = generation
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
          self.pinGroups = [self.group1, self.group2, self.group3, self.group4, self.group5, self.group6, self.groupPl,
                            self.groupRl, self.groupRr, self.groupPr, self.groupBl, self.groupBr, self.groupFl, self.groupFr]
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
          #if self.parent1 is not None and self.parent2 is not None:
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
      
      def save_to_file(self, path):
          dir = os.mkdir(path+"/"+self.filename)
          with open(path+"/"+self.filename+"/"+self.filename+".txt", 'wb') as output:
              data = jsonpickle.encode(self)
              output.write(data)
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
      def generate_thread_instructions(self):
          for thread in self.threads:
              # instructions are xy coordinate points to plug into the pinGroups
              thread.decode()
              #print thread.decoded_instructions
      
      
      """
      *Input:* Nothing
      *Output:* Nothing
      *Side Effect:* Determines the pins connected as dictated by the coordinates of each thread.
      *Process:* Each Thread is built (i.e.  their decoded_instructions are used to accesses PinGroups and Pins (see below))
       using a round-robin approach. This done by simultaneously building each thread, one index at a
       time. Threads that are actively being built are stored in the list active_threads. Threads are
       removed from active_threads if they collided with with a previously built Thread, for trying 
      to accesses out of bounds Pins, for having only one valid pin, etc. Pins are accessed using the
       xyz coordinates stored in Thread.decoded_instructions, where x corresponds to the PinGroup, y
       corresponds to a specific Pin in the PinGroup, and z corresponding to another Pin within that
       same PinGroup-- the origin of the next wire. After each Thread is built, and therefore 
      active_threads is empty, threads are checked to make sure there are no connections without a
       terminal pin. """
      
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
          #tracks the number of threads that have been run, and in turn, when the index should be incremented
          #thread_counter = 0
          # A deepcopy of running_threads that we are free to modify
          # threads are removed from active_thread when they are no longer able to make connections
          active_threads = [i for i in running_threads] 
          while len(active_threads) > 0: 
          # This builds each thread at the current index value
              for running in running_threads:
      
      
                  # if 
                  #if thread_counter % len(running_threads):
                  # if thread_counter == len(active_threads):
                      #index += 1
                      #print "---------------------------------------------\nNew Index:  %s" % index
                      #thread_counter = 0
      
      
                  error_encountered = False
                  # declare variables for finding and storing a selected pin
                  if running in active_threads:
                      #print '\nActive Thread Coords:', running.decoded_instructions
                      try:
                          # get the specific pin coordinates from the instruction and translate it to make it a valid pin
                          pin_coordinates = running.decoded_instructions[index]
                          accessed_pin_group = self.pinGroups[pin_coordinates[0]]
                          accessed_output_pin = accessed_pin_group.get_input(pin_coordinates[1])
                          #print "Coords: %s  Group : %s  Pin: %s" % (pin_coordinates, accessed_output_pin.group_id,accessed_output_pin.number)
                          # Jake addition 2015-06-09 this hopefully chooses another pin to be the origin 
                          # ofrthe next connection (same pin group as terminus of previous connection)
                      # print pin_coordinates,
      
                      # an index error means that the thread's coordinates could not connect to an actual pin
                      except IndexError:
                          try:
                              #print "Out of Bounds coordinate: %s. Thread deactivated" %  str(running.decoded_instructions[index])
                              pass
                          except IndexError:
                              pass
                          #print 'Bad index: %s' % index
                          error_encountered = True
                          # if a thread only has one pin, then it cannot create a connection, and the pin must be made available
                          if len(running.connected_pins) == 1:
                              to_remove = running.connected_pins[0]
                              # set the pin's availability to 'true'
                              to_remove.available = True
                              # remove the pin from the thread's & organism's group of connected pins
                              for x in range(len(self.connections)):
                                  if (self.connections[x].group_id == to_remove.group_id and
                                              self.connections[x].number == to_remove.number):
                                      del self.connections[x]
                                      break
                              # wipe the running thread's connected pins since it only contains one pin, which cannot connect
                              running.connected_pins = []
                          active_threads.remove(running)
      
                  # it is possible that the pin exists but has been taken
                      if not error_encountered:
                          try:
                              # ensure the pin hasn't been 'taken' by another thread already
                              # if accessed_output_pin in self.connections:
                              for pin in self.connections:
                                  if accessed_output_pin.group_id == pin.group_id and accessed_output_pin.number == pin.number: 
                                      #print "pin already taken: %s" % accessed_output_pin.group_id
                                      raise LookupError("Connection failed: pin already connected")
                              ###WARNING: OUTDATED CODE
                              # its possible the accessed pin is unavailable, signifying it was already taken by another thread
                              #if not accessed_pin.available:
                              #    raise LookupError("Connection failed: pin already connected")
                              else:
                                  self.connections.append(accessed_output_pin)
                                  running.connected_pins.append(accessed_output_pin)
      
                              #print 'connected pins:',[i.group_id for i in running.connected_pins]
                              if len(pin_coordinates) == 3: #and (len(running.decoded_instructions) % 2) != 0:
                                  new_connection_origin = accessed_pin_group.get_output(pin_coordinates[2])
                              else:
                                  new_connection_origin = None
                                  # ensure the pin hasn't been 'taken' by another thread already
                                  # connect to a random input pin in the same group
                                  # input pins are used since the previous pin was an output
                                  #output_pin = accessed_pin_group.get_random_input()
                                  #self.connections.append(output_pin)
                                  #running.connected_pins.append(output_pin)
                              if new_connection_origin is not None:
                                  if new_connection_origin in self.connections:
                                      raise LookupError("Connection failed: pin already connected!")
                                  else:
                                      self.connections.append(new_connection_origin)
                                      running.connected_pins.append(new_connection_origin)
      
                          except LookupError:
                              #the pin raised a lookup error due to a collisions; update variable accordingly
                              self.collisions += 1
                              # if a thread only has two pins, then it cannot create a connection to pins outside of the initial
                              # group, and each pin must be made available
                              if len(running.connected_pins) == 2:
                                  error_encountered = True
                                  for x in range(len(running.connected_pins)):
                                      # set the pin's availability to 'true'
                                      running.connected_pins[x].available = True
                                      # remove the pin from the thread's & organism's group of connected pins
                                      #self.connections.remove(running.connected_pins[x])
                                      for n in range(len(self.connections)):
                                          if (self.connections[n].group_id == running.connected_pins[x].group_id and
                                              self.connections[n].number == running.connected_pins[x].number):
                                              del self.connections[n]
                                              break
      
                                  # wipe the running thread's connected pins since it only contains two pins,
                                  # which is not a complete connection
                                  running.connected_pins = []
                              active_threads.remove(running)
                              if len(running.connected_pins) >  2:
                                      pass
              #thread_counter += 1
              index+=1 # Starts loop again at next index for all threads
          for running in self.threads:             
              if len(running.connected_pins) % 2 != 0:# and \
                      #len(running.connected_pins) >= 1:
                  x =len(running.connected_pins)- 1
                  to_remove =  running.connected_pins[-1]
                  to_remove.available = True
                  running.connected_pins.remove(to_remove)
                  #running.connected_pins[len(running.connected_pins) - 1].available = True
                  connections_copy = [n for n in self.connections] #deepcopy that we can manipulate
                                                                  #with impunity
                  for n in self.connections:
                      if (n.group_id == to_remove.group_id and\
                          n.number == to_remove.number):
                          connections_copy.remove(n)
                  self.connections = connections_copy
                  #running.connected_pins = [running.connected_pins[i] for i in range(x - 1)]
                  #print 'thread stuff \n' +  [i.group_id for i in running.connected_pins]
              else:
                  #for running in running_threads:
                  pass
      
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
    """"while index < len(dom.genome):
        child1_genome.append(dom.genome[index])
        if dom.genome[index].crossover_point == 1:
            while dom.genome[index + 1].crossover_point != 1 and \
                    index + 1 < len(dom.genome) - 1:
                        child1_genome.append(rec.genome[index + 1])
                        index += 1
        index += 1"""

    dom_genome_copy = True
    dom_stuff =[]
    rec_stuff=[]
    while index <= len(dom.genome) - 1:
        """if index  % 4 == 0:
            dom_stuff.append('')
            #rec_stuff.append('|')"""
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
    #for i in range (0, len(dom_stuff)- 1):
        #print '%s  %s' %  (dom_stuff[i], rec_stuff[i])
    #print dom_stuff


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
        child1 = Organism(dom.generation + 1, count,dom.genome_size,2,True,dom.thread_length,dom.mutation_rate, dom, rec, child_instruction_set.genome)
    else:
        os.makedirs(path)
        child_instruction_set = InstructionSet(dom.genome_size, 2,True,dom.thread_length, dom.mutation_rate)
        child_instruction_set.setGenome(child1_genome)
        child_instruction_set.mutate()
        child1 = Organism(dom.generation + 1, 0,dom.genome_size,2,True,dom.thread_length, dom.mutation_rate, dom, rec, child_instruction_set.genome)
        #print [i.char for i in child1.genome]
   # print 'child %s threads:' % child1.filename
   # for thread in child1.threads:
   #     print thread.decoded_instructions
   #     print [i.group_id for i in thread.connected_pins]
    child1.save_to_file(path)
   # print 'Dom  Rec  Crossover  real_offspring'
   # for i in range(len(child1_genome) - 1):
   #     print '%s      %s      %s          %s' % (dom.genome[i].char, rec.genome[i].char, child1_genome[i].crossover_point,child1_genome[i].char)
    #if is_same_genome(dom, child1): print 'THEYRE SAME'
    #else: print 'THYRE DIFF'
    return child1
def generate_viable():
    # writes a 'progress bar' to the console
    def progress(x):
        out = '\r %s organisms tested' % x  # The output
        print out,

    genomes_tested = 0
    finished = False
    while not finished:
        test = Organism(0, 0, 560,
            800, True, 80, 2000)
        if len(test.connections) > 2: #test.is_viable():
            print "-------------------------------------//"
            print "connections: "
            for thread in test.threads:
                print "new thread connections:"
                for connection in thread.connected_pins:
                    print connection.group_id, connection.number
            print "-------------------------------------//"
            gen = ""
            for base in test.genome:
                gen += str(base.char)
            print gen
            finished = True
        else:
            del test
            genomes_tested += 1
            progress(genomes_tested)
