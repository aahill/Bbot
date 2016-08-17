import csv
import re
from collections import defaultdict
# len_of_trial (in minutes) refers to how long the braitenbot collected light data
def energyAcquired(file, len_of_trial):
    columns = defaultdict(list)
    result = []
    with open(file) as f:
        reader = csv.reader(f)
        reader.next()
        for row in reader:
            for (i,v) in enumerate(row):
                try:
                    columns[i].append(v)
                except ValueError:
                    pass
        # Filters out all the data from the csv that isnt a number and sums all the
        # numbers together.
        for i in filter(lambda x: re.search(r'\b\d+\.\d+\b', x) != None, columns[2]):
            result.append(float(i))
        result = result[:(len_of_trial * 60)]
        return sum(result)
#print energyAcquired('/home/jake/Downloads/initial_test_robot1_trial1.csv', 1)
