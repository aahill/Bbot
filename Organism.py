class Thread:
    def __init__(self, thread_decoder):
        self.binary = []
        self.decoded_instructions = []
        self.connected_pins = []
        self.decoder = thread_decoder

    # simply calls the decoder to decode the thread's instructions
    def decode(self):
        self.decoded_instructions = self.decoder.generate_coords(self.binary)
class Organism:
    def __init__(self, generation, generational_index,genome_size, num_crossover_points, unrestricted_crossover_point_distribution, thread_length, parent1=None, parent2=None, genome=None):
        # store perfromance on behavioral task
        self.performance_1 = None
        self.performance_2 = None
        self.reproduction_possibilities = None
        self.generation = generation
        self.generational_index = generational_index
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
        self.instruction_set = InstructionSet(genome_size, num_crossover_points,unrestricted_crossover_point_distribution, thread_length)
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
                    thread_binary = ([self.genome[i].char for i in range(genome_index, \ genome_index+thread_length)])
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
        
        <build_thread_coordinates>>
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
    """"for i in range (0, len(dom_stuff)- 1):
        print '%s  %s' %  (dom_stuff[i], rec_stuff[i])
    print dom_stuff"""


    # This takes care of  of saving the Org.
    # if the path specified does not exist a new directory
    # will be created

    count = 0
    if os.path.isdir(path):
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                count += 1
        child_instruction_set = InstructionSet(2100, 2,True,300)
        child_instruction_set.setGenome(child1_genome)
        child_instruction_set.mutate()
        child1 = Organism(dom.generation + 1, count,2100,2,True,300, dom, rec, child_instruction_set.genome)
    else:
        os.makedirs(path)
        child_instruction_set = InstructionSet(2100, 2,True,300)
        child_instruction_set.setGenome(child1_genome)
        child_instruction_set.mutate()
        child1 = Organism(dom.generation + 1, 0,2100,2,True,300, dom, rec, child_instruction_set.genome)
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
        test = Organism(0, 0)
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
