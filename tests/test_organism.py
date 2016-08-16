from code.Organism import *
from code.PinAndPinGroup import *
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

#creates a new organism object with __init__ called
def generate_organism():
	#create organism with the specified parameters
	return Organism(generation,generational_index,genome_size,num_crossover_points,
		thread_length,unrestricted_crossover_point_distribution,thread_length, parent1, parent2, genome)

#create an organism without the __init__ called 
def generate_uninitialized():
	#by using __new__, it is possible to instantiate the organism without initializing any attributes
	#useful for testing individual methods/properties/etc.
	return Organism.__new__(Organism, generation,generational_index,genome_size,num_crossover_points,
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
	assert(type(test_org.decoder) is Decoder)
	#ensure the lenght of the organism's genome is equal to genome_size
	assert(len(test_org.genome) == genome_size)

"""
ensure threads get created by placing appropriately sized sections of 
the organism's genome get placed in lists, which are then appended to the 
organism's 'threads' attribute - in this test, test the case in which
not every thread has enough bases to have threds of equal length
"""
def test_create_uneven_threads():
	test = generate_uninitialized()
	test.threads = []
	#an organism's threads consist of the binary characters extracted from a sequence of bases
	#therefore, a list of bases must be created. 7 is chosen arbitrarily
	base_list = [Base() for x in range(7)] 
	test.genome = base_list
	#set the thread length such that one thread will have an unequal number of binary characters
	thread_length = 2;
	#decoder object needed for thread creation, but not used in this test
	test.decoder = Decoder()

	test.create_threads(thread_length)
	#ensure the correct number of threads were appended to the organism
	assert(len(test.threads) == 4)
	#ensure the first 3 threads have the 2 bases, and the last only has 1
	for x in range(3):
		assert(len(test.threads[x].binary) == 2)
	assert(len(test.threads[3].binary) == 1)

"""
perform the above test but with th ecase that all threads
are able to have threads of equal length
"""
def test_create_even_threads():
	test = generate_uninitialized()
	test.threads = []
	#an organism's threads consist of the binary characters extracted from a sequence of bases
	#therefore, a list of bases must be created. 
	base_list = [Base() for x in range(8)] 
	test.genome = base_list
	#set the thread length such that one thread will have an equal number of binary characters
	thread_length = 2;
	#decoder object needed for thread creation, but not used in this test
	test.decoder = Decoder()

	test.create_threads(thread_length)
	#ensure the correct number of threads were appended to the organism
	assert(len(test.threads) == 4)
	#ensure the all threads have the 2 bases
	for x in range(len(test.threads)):
		assert(len(test.threads[x].binary) == 2)

"""
perform the above test but with an empty genome. The result should be
no threads in the organism
"""
def test_create_threads_empty():
	test = generate_uninitialized()
	test.threads = []
	#an organism's threads consist of the binary characters extracted from a sequence of bases
	#an empty list is required for this test
	test.genome = []
	thread_length = 2;
	#decoder object needed for thread creation, but not used in this test
	test.decoder = Decoder()

	test.create_threads(thread_length)
	#ensure the correct number of threads were appended to the organism
	assert(len(test.threads) == 0)

"""
using the binary genome string of an organism verified to have working connections, 
instantiate the organism, and ensure the correct pins have been set to unavailable
NOTE: the genome string corresponds to the organism 3_8_2_9_2_5Development from the
december prelimineary trial experiments
"""
def test_organism_connections():
	verified_genome = "010010100001011101001011100100011111100010011001"+\
	"010000011011101000111100111111110011101101011011101100011110001010110"+\
	"111001001111110001010000101100001110111011011110010100011101100000101"+\
	"011011101010011001100010100011001001011010000100011101011000011010100"+\
	"011110111000001110111110111011011111011110001001001100001100101001100"+\
	"110100111111110100010001111011011110011010111010110000000101011101011"+\
	"000001010010011101100100010001110000111000101000100101001011101000010"+\
	"101100011000111000010100101100011110001001011110111111001010111101100"+\
	"10110101110111101010000111100"

	test_org = generate_uninitialized()
	test_org.decoder = Decoder()
	#recomend the thread length be 80, which is the thread length used
	#when the verified organism was created
	thread_length = 80
	#because __init__ function is curcumvented, manually initialize the 
	#test organism's properties
	# initialize pin groups
	test_org.group1 = Group1()
	test_org.group2 = Group2()
	test_org.group3 = Group3()
	test_org.group4 = Group4()
	test_org.group5 = Group5()
	test_org.group6 = Group6()
	test_org.groupPl = GroupPl()
	test_org.groupRl = GroupRl()
	test_org.groupRr = GroupRr()
	test_org.groupPr = GroupPr()
	test_org.groupBl = GroupBl()
	test_org.groupBr = GroupBr()
	test_org.groupFl = GroupFl()
	test_org.groupFr = GroupFr()
	test_org.pinGroups = [test_org.group1, test_org.group2, test_org.group3, test_org.group4, test_org.group5, test_org.group6, test_org.groupPl,
	                test_org.groupRl, test_org.groupRr, test_org.groupPr, test_org.groupBl, test_org.groupBr, test_org.groupFl, test_org.groupFr]
	test_org.threads = []
	test_org.connections = []


	#convert verified genome string into a split list of characters
	genome_list = list(verified_genome)

	#the organism's genetic code must be created, and alterted to mach the characters
	#from the verified genome
	org_genome = [Base() for x in range(len(genome_list))]
	for x in range(len(org_genome)):
		org_genome[x].char = genome_list[x]
	test_org.genome = org_genome

	#ensure the genome string copied over is identicle to the verified genome
	test_org_genome_string = ""
	for x in range(len(test_org.genome)):
		test_org_genome_string += test_org.genome[x].char
	assert(test_org_genome_string == verified_genome)


	#create threads and thread coordinates as usual
	test_org.create_threads(thread_length)
	#ensure the correct number of threads are created (genome_length/thread_length)
	assert(len(test_org.threads) == 7), len(test_org.threads)

	test_org.generate_thread_instructions()
	test_org.build_thread_coordinates()

	#ensure only one thread (the fourth) has any connections 
	for x in range(3):
		assert(len(test_org.threads[x].connected_pins) == 0)

	assert(len(test_org.threads[3].connected_pins) == 4), "got " + str(([pin.group_id+str(pin.number) for pin in test_org.threads[3].connected_pins])) + "instead of something else"

	for x in range(4,len(test_org.threads)):
		assert(len(test_org.threads[x].connected_pins) == 0)

	#check that all connected pins are marked as unavailable 
	for x in range(len(test_org.connections)):
		assert(test_org.connections[x].available == False)
	#ensure the pins used in the organism's connections are marked as 'unavailable', and
	#all others are marked as 'available' by using the tuples in the decoded_instructions
	#attribute, which provides an index into the pin group matrix
	##inst1 = test_org.connections[0]
	##assert((test_org.connections[inst1[1]][inst1[2]]).available == False)
	#thread = 
	#thread.decoded_instructions
	#for connection_tuple in test_org.decoded_instructions:


#test = generate_organism()
#ensure that the organism's connected pins are marked as "unavailable" in the corresponding pin groups
#def test_pin_availability():
#	connected_pins = test.connected_pins
#	for pin in connected_pins:
