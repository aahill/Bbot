from AlternateOrganism import *

#self, generation, generational_index,genome_size, num_crossover_points, unrestricted_crossover_point_distribution, thread_length, parent1=None, parent2=None, genome=None):
 

done = False
while not done:
  test = Organism(0,0,2100,4,True,300)
  pins = []
  for thread in test.threads:
    for connection in thread.connected_pins:
      id = connection.group_id + ',' + str(connection.number)
      pins.append(id)
  if len(set(pins)) != len(pins):
    done = True
    print pins
