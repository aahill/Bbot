import json_load_file
import os
from Organism import *
import shutil
import random
import tempfile

def unpickle_and_print(directory):
    for root, dir, files in os.walk(directory):
        for f in files:
            print root +'/' + f 
            if f.endswith('.txt'):
                try:
                    org = json_load_file.json_load_file (root +'/' + f )
                    #print [i.crossover_point for i in org.genome]
                    for thread in org.threads:
                        print thread.decoded_instructions
                        print "-------------------------------------//"
                        print "Org: %s" % org.filename
                        print "connections: "
                        for thread in org.threads:
                            print [i.group_id for i in thread.connected_pins]
                            print "new thread connections:"
                            for connection in thread.connected_pins:
                                print connection.group_id, connection.number
                            print "-------------------------------------//"
                        break
                except IOError:
                    print 'error'

def fix_crossover_points(old_directory, new_directory, crossover_prob):
    shutil.copytree(old_directory, new_directory, symlinks=False, ignore=None)
    for root, dir, files in os.walk(new_directory):
        for f in files:
            print root +'/' + f 
            if f.endswith('.pkl'):
                try:
                    org = pickle.load(open (root +'/' + f , 'rb'))
                    for base in org.genome:
                        if crossover_prob == 0:
                            base.crossover_point = 0 
                        else:
                            rand = random.randint(1, crossover_prob)
                            if rand <= crossover_prob - 1:
                                base.crossover_point = 0
                            else:
                                base.crossover_point = 1
                    dirpath = tempfile.mkdtemp()
                    org.save_to_file(dirpath)
                    shutil.copy2(dirpath +'/'+os.path.splitext(f)[0]+'/'+ f, root +'/'+f)
                    shutil.rmtree(dirpath)
                except IOError:
                    shutil.rmtree(new_directory)
                            

    

if __name__ == '__main__':
    #unpickle_and_print('/home/jake/Dropbox/BraitenbotCode/2015-06-23TEST/Gen2')
    #fix_crossover_points('/home/jake/Dropbox/BraitenbotCode/2015-06-23TEST/Gen1/', '/home/jake/Dropbox/BraitenbotCode/2015-06-23TEST/Gen1_3000_corssover_prob', 3000)
<<<<<<< HEAD
    unpickle_and_print('/Users/Aaron/Projects/bot_prelims/2015-11-11-preliminary-robo-experiments/Development/Gen3')
=======
    unpickle_and_print('/home/jake/org/Thesis_Stuff/2015-11-11-preliminary-robo-experiments/Random_Development/Gen1')
>>>>>>> a16e446d6fa2618a4c0313bce3e476303f798cd2

