from ..Organism import *
from nose.tools import *

#paramters for organism generation
generation = 0
generational_index = 0
genome_size = 2100
num_crossover_points= 4
unrestricted_crossover_point_distribution = True
thread_length = 300
parent1 = None
parent2 = None
genome= None

#creates a new organism object
def generate_organism():
	#create organism with the specified parameters
	return Organism(generation,generational_index,genome_size,num_crossover_points,
		thread_length,unrestricted_crossover_point_distribution,thread_length, parent1, parent2, genome)

"""
ensure the proper organism properties are initialized
"""
def test_initialization():
	test_org = generate_organism()
	#assert organism pin groups are of the correct type
	assert(type(test_org.group1) is Group1)
	assert(type(test_org.group2) is Group2)
	assert(type(test_org.group3) is Group3)
	assert(type(test_org.group4) is Group4)
	assert(type(test_org.group5) is Group5)
	assert(type(test_org.group6) is Group6)
	assert(type(test_org.groupPl) is GroupPl)
	assert(type(test_org.groupPr) is GroupPr)
	assert(type(test_org.groupRl) is GroupRl)
	assert(type(test_org.groupRr) is GroupRr)
	assert(type(test_org.groupBl) is GroupBl)
	assert(type(test_org.groupBr) is GroupBr)
	assert(type(test_org.groupFl) is GroupFl)
	assert(type(test_org.groupFr) is GroupFr)
	#assert the decoder is initialized
	assert(type(test_org.decoder) is Decoder), type(test_org.decoder )

#test = generate_organism()
#ensure that the organism's connected pins are marked as "unavailable" in the corresponding pin groups
#def test_pin_availability():
#	connected_pins = test.connected_pins
#	for pin in connected_pins: