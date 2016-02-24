import random
import string


class Base:
    def __init__(self):
        self.char = random.randint(0, 1)
        self.crossover_point = 0 # Crossover hotspots are set later by InstructionSet
            
    def set_crossover_point(self, new_val):
            self.crossover_point = new_val
            return self.crossover_point

    def set_char(self, new_val):
            self.char = new_val
            return self.char


class InstructionSet:
    def __init__(self, size, crossover_point_number,unrestricted_distribution, gene_length, mutation_rate ):
        self.genome = []
        self.mutation_chance = mutation_rate
        x = size  # a place holder, the length of the genome
        counter = 0 
        for num in range(0, x ):
            self.genome.append(Base())
            # in the event there are no break points at all
            # maybe we dont want this though? Can discuss later
        if unrestricted_distribution:
            while counter != crossover_point_number:
                random.choice(self.genome).set_crossover_point(1)
                counter +=1 
        else:
            potential_locations = [i*gene_length for i in range (1, (len(self.genome)/gene_length)) ]
            while counter != crossover_point_number:
                rand_index = random.choice(potential_locations)
                self.genome[rand_index].set_crossover_point(1)
                potential_locations.remove(rand_index)
                counter +=1
            print potential_locations
        assert counter == crossover_point_number 
        """for s in self.genome:
            counter += s.crossover_point
        if counter < 1:
            random.choice(self.genome).set_crossover_point(1)"""

    def setGenome(self, new_genome):
        self.genome = new_genome

    
    def mutate(self):
        #mutation_chance = 20000 #THIS IS THE REAL ONE
        mutation_chance = self.mutation_chance
        for i in range(len(self.genome)):
            rand_int1 = random.randint(1, mutation_chance)
            rand_int2 = random.randint(1, mutation_chance)
            if rand_int1 == mutation_chance:
                print 'Crossover_point mutation at index: %s' % i
                if self.genome[i].crossover_point == 0:
                    self.genome[i].set_crossover_point(1)
                    print '0 --> %s' % self.genome[i].crossover_point
                else:
                    self.genome[i].set_crossover_point(0)
                    print '1 --> %s' % self.genome[i].crossover_point
            if rand_int2 == mutation_chance:
                print 'Char mutation at index: %s' % i
                if self.genome[i].char == 0:
                    self.genome[i].set_char(1)
                    print '0 --> %s' % self.genome[i].char
                else:
                    self.genome[i].set_char(0) 
                    print '1 --> %s' % self.genome[i].char
