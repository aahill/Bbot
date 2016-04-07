import random
import string


#*input:* None\\
#*Output:* A Base object with two binary attributes, char and crossover_point.Char has $1/2$ chance of being 1 or 0, crossover_point is initialized to 0.\\
class Base:
    def __init__(self):
        #the binary nucleobase analog 
        self.char = random.randint(0, 1)
        #the binary crossover point value, for use in reproduction
        self.crossover_point = 0 # Crossover hotspots are set later by InstructionSet
    #sets the crossover point value to a new value
    def set_crossover_point(self, new_val):
            self.crossover_point = new_val
            return self.crossover_point
    #sets the char value to a new value
    def set_char(self, new_val):
            self.char = new_val
            return self.char



#*Input:* size, the length of the genome
# crossover_point_number, the number of allowed crossover points
# unrestricted_distribution, a boolean for whether
#gene_length

#*Output:* An InstructionSet object with a genome attribute.
#A genome is a list containing 2000 Base objects of which at least one has a crossover_point value == 1.\\

class InstructionSet:
    def __init__(self, size, crossover_point_number,unrestricted_distribution, gene_length, mutation_rate ):
        self.genome = []
        self.mutation_chance = mutation_rate
        self.co_point_location =[] ## Keeps track of indecies of copoints
        self.unrestricted_distribution = unrestricted_distribution

        x = size  # a plac holder, the length of the genome
        counter = 0 
        for num in range(0, x ):
            self.genome.append(Base())
            # in the event there are no break points at all
            # maybe we dont want this though? Can discuss later

        #Calculates index between coding regions for xover points 
        self.potential_locations  =  [i for i in range(gene_length, len(self.genome), gene_length) ]

        if unrestricted_distribution:
            while counter != crossover_point_number:
                random.choice(self.genome).set_crossover_point(1)
                counter +=1 
        else:
            xover_indices =[i for i in self.potential_locations]
            while counter != crossover_point_number:
                rand_index = random.choice(xover_indices)
                self.genome[rand_index].set_crossover_point(1)
                xover_indices.remove(rand_index)
                counter +=1
            #print potential_locations
        assert counter == crossover_point_number 

    # determines the indices at which the copoints for a genome are located
    def setCOPointLocation(self):
        co_points = []
        for i in range(len(self.genome)):
            if self.genome[i].crossover_point == 1:
                co_points.append(i)
        self.co_point_location = co_points

    def setGenome(self, new_genome):
        self.genome = new_genome
        self.setCOPointLocation()

    # Counts the number of crossover points

    
    def mutate(self):
        #mutation_chance = 20000 #THIS IS THE REAL ONE
        mutation_chance = self.mutation_chance
        # A bool, determines where copoints are allowed to go.
        unrestricted_distribution = self.unrestricted_distribution
        for i in range(len(self.genome)):
            rand_int1 = random.randint(0, mutation_chance)
            rand_int2 = random.randint(0, mutation_chance)
            if rand_int1 == mutation_chance:
                #If True, xover can happen anywhere
                if unrestricted_distribution:
                    self.genome[i].set_char(1-self.genome[i].crossover_point)
                #If false, can only occur between coding regions
                else:
                    rand_index = random.choice(self.potential_locations)
                    self.genome[rand_index].set_crossover_point(1- \
                                                                self.genome[rand_index].crossover_point)
    
                    print ('%s --> %s' %
                           (1-self.genome[i].crossover_point, self.genome[i].crossover_point))
    
                    # print 'Crossover_point mutation at index: %s' % i
                    # if self.genome[i].crossover_point == 0:
                    #     self.genome[i].set_crossover_point(1)
                    #     print '0 --> %s' % self.genome[i].crossover_point
                    # else:
                    #     self.genome[i].set_crossover_point(0)
            if rand_int2 == mutation_chance:
                print 'Char mutation at index: %s' % i
                self.genome[i].set_char(1-self.genome[i].char)
                print('%s ---> %s' % (1-self.genome[i].char, self.genome[i].char))
                # if self.genome[i].char == 0:
                #     self.genome[i].set_char(1)
                #     print '0 --> %s' % self.genome[i].char
                # else:
                #     self.genome[i].set_char(0) 
                #     print '1 --> %s' % self.genome[i].char
