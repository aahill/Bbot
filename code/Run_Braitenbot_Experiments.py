import Organism
import RankAndCrossGeneration as cross
import wrtieOrganismDataToCsv as data
import compare_offspring_to_parents as compare
import unpickler


"""*Input:* path, to where you want these bots to be saved.
 max_bots, int, number of bots you wanna generate
 generational index, int, tracks the order in which the orgs in a gen were created
thread_len, int, number of bases that code for a single thread
num_crossover,int, number of crossover points in each genome
co_distribution,bool, if True, copoints can appear anywhere, else, they are contained to the interthread regions
mutation_rate,int, chance of anyone Base being mutated.
alt_mode, bool,if True, interactive development is used, else, independent,
development is used

Default values for these parameters correspond to parameters used in experiment

*Output:* A dir containing max_bots numbered of pickled organism files."""
def generatePopulation(path,max_bots=10,genome_size=560,
                       num_crossover=2, co_distribution=True,
                       thread_len=80, mutation_rate = 2000,
                       alt_mode=False):
      count = 0
      while(count < 10):
          org = Organism.Organism(1, count, genome_size,
                                  num_crossover, co_distribution,
                                  thread_len, mutation_rate, None,
                                  None,None,alt_mode)
          if org.is_viable():
              org.save_to_file(path+'/Gen1')
              count += 1


"""*INPUT* infile, csv created by writeOrganismDataToCsv function
outfile, csv, the name of the file created by this function.
number_of_gens, int, number of genertions in the infile
*OUTPUT*: Nicely formatted csv with data comparing each offspring with
its parents on the same line. Useful for data analyses."""
def compare_offspring_gen_to_parent_gen(infile, outfile,number_of_gens):
    result_file= opent(outfile, 'a')
    wr = csv.writer(results_file, dialect='excel')
    wr.writerow(['child','child_fitness','child_xover''parent1', 'parent_1_fitness',
                 'parent1_co_points','parent2',
                 'parent2_fitness', 'parent2_co_points' ,
                 'mean_parent_co_points','selection_differential_co_points',
                 'mean_parents_fitness','selection_differential_fitness'])
    for i in range(2, number_of_gens-1):
        compare.compare_offspring_to_parent(f, i, results_file)

##----------------------------------------------------------------------------------------
##
##  STEPS FOR RUNNING PHYSICAL ROBOT EXPERIMENT
##
##----------------------------------------------------------------------------------------

# DIRECTIONS: Uncomment function names one step at a time, add appropriate input parameters,
# and then run this  file in terminal:
# >>$ python2 Run_Braitenbot_Experiments.py


### Step 1:
##  Generate an initial population of Braitenbots (here Organisms or orgs)
##  Note: default parameters are the ones used for initial experiment 
##  Make sure your directory path looks like this: /your/dir/path/Gen1

#generatePopulation() 

## This will create a dir, containing sub-dirs corresponding to each org in the generation

### Step2:
##  Print out the phenotypes for each organism:

# unpickler.unpickle_and_print()

## Run each org and place HOBO csv in corresponding org dir.

### Step 3:
##  Cross the current gen and create a new one:

# cross.thresholdedCrossGeneration()

### Step 4: repeate steps 2 and 3 until there are a sufficient number of gens.

## Step 5:
## Collate the data into one csv

# data.writeOrganismDataToCsv()
# compare_offspring_gen_to_parent_gen()
