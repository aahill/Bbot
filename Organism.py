
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
