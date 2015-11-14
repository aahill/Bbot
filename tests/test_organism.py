from ..Organism import *
from nose.tools import *

#paramters for organism generation
generation = 0
generational_index = 0
genome_size = 6000
num_crossover_points= 200
unrestricted_crossover_point_distribution = .5
thread_length = 300
#
#parent1=None
#parent2=None
#genome=None
def generate_organism():
	return Organism(generation,generational_index,genome_size,num_crossover_points,thread_length)


test = generate_organism()
#ensure that the organism's connected pins are marked as "unavailable" in the corresponding pin groups
def test_pin_availability():
	connected_pins = test.connected_pins
	for pin in connected_pins:
		

