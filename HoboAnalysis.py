
import csv
from collections import defaultdict
def energyAcquired(*args):
    columns = defaultdict(list)
    result = []
    for arg in args:
        with open(arg) as f:
            reader = csv.reader(f)
            reader.next()
            for row in reader:
                for (i,v) in enumerate(row):
                    try:
                        columns[i].append(v)
                    except ValueError:
                        pass
            for i in filter(lambda x: len(x) < 4, columns[2]):
                result.append(float(i))
            return sum(result)
