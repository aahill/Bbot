import re
import csv
import os
import json_load_file

#compares each child genome to its parents in terms of thread data

def compare_all_in_dir(main_directory):
    #track whether a header has been added to the csv rows
    header = False
    #store all csv rows for later appending into a csv file
    csv_rows = []

    #helper function to count the number of empty and non-empty threads
    #takes in an organism
    def count_empty_threads(org, name):
        header = ["num empty threads in " +name, "num nonempty threads in " +name]
        empty = 0
        non_empty = 0
        for t in org.threads:
            if len(t.connected_pins) == 0:
                empty += 1
            else:
                non_empty += 1
        return (header, [empty, non_empty])

    #helper function to count the number of sensor, motor, and neuron connections 
    def count_connections(org, name):
        header = [
        "total number of sensor/motor threads in " +name,
        "avg. length of thread in " +name,
        "total number IR connections in " +name,
        "total number of sensor connections in " +name,
        "total number photosensor connections in " +name,
        "total number of motor connections in " +name,
        ]
        avg_thread_length = 0.0
        num_sensor_connections = 0
        num_motor_connections = 0
        #number of connections made to ir
        num_ir_connections = 0
        #number of connections made to photosensors
        num_photosensor_connections = 0
        #number of threads that have connections from motor to sensor
        num_motor_sensor_threads = 0


        #iterate through threads' pins and determine what type of connections 
        #have been made
        for thread in org.threads:
            avg_thread_length += len(thread.connected_pins)
            for pin in thread.connected_pins:
                if pin.group_id.lower() in ['pl','pr']:#, 'rl', 'rr']:
                    num_sensor_connections += 1
                    num_ir_connections += 1

                if pin.group_id.lower() in ['rl', 'rr']:
                    num_sensor_connections += 1
                    num_photosensor_connections += 1

                elif pin.group_id.lower() in ['fl','bl','fr','br']:
                    num_motor_connections += 1

            #transform list of connected pins into set notation containing the first two letters of the pin ids
            set_notation_connected_pins = set([pin.group_id for pin in thread.connected_pins])

            #see if motors are in the list of connected pins
            if len(set_notation_connected_pins.intersection(['fl','bl','fr','br'])) > 0:
                #see if sensors are in the list of connected pins
                if len(set_notation_connected_pins.intersection(['pl','pr', 'rl', 'rr'])) > 0:
                    num_motor_sensor_threads += 1

        avg_thread_length = avg_thread_length/len(org.threads)
        data = [ num_motor_sensor_threads, avg_thread_length, num_ir_connections, num_sensor_connections,
            num_photosensor_connections, num_motor_connections]

        return (header, data)

    #iterate through all gen files in the main directory
    for root, gen_dirs, files in os.walk(main_directory):
        #iterate through all organism files in the gen dirs, except for the ones in gen1
        for gen in gen_dirs:
            for root, dirs, files in os.walk(os.path.join(main_directory,gen)):
                for f in files:
                    #only extract data from pickled organisms, which are the only
                    #.txt files in the directory. NOTE: the baseline does not have
                    #a .txt file
                    if f.endswith('.txt'):
                        print "current_child: ", f 
                        #main section where parents are found
                        try:
                            curr_org = json_load_file.json_load_file (root+'/'+f)
                            child_data1 = count_empty_threads(curr_org,"self")
                            child_data2 = count_connections(curr_org,"self")
                            #append name info to the rows
                            child_data_header = ["ID"]+child_data1[0]+child_data2[0]
                            child_data_all = [f[:-4]]+child_data1[1]+child_data2[1]
                        except IOError:
                            print "error encountered getting organism file"
                        #only get the parent data if the organism is in org 2 or later
                        gen_index = gen[-1] 
                        if int(gen_index) > 1:
                            #set up all data to be collected from organism
                            #parent1 name
                            parent1_name = ""
                            parent2_name = ""

                            #beginning of parent1's identifier
                            parent1_id = f[4:7]
                            #beginning of parent2's identifier
                            parent2_id = f[8:11]
                            #parents location
                            parents_location = os.path.join(main_directory, "Gen"+str(int(gen_index)-1))
                            #get parent1 data
                            for root2, org_dirs, org_files in os.walk(parents_location):
                                for org in org_files:
                                    if org.endswith(".txt") and org.startswith(parent1_id):
                                        print "parent1: ", org
                                        #the parent's folder is its name without the .txt file extension
                                        org_folder = org[:-4]
                                        parent1 = json_load_file.json_load_file (os.path.join(parents_location,org_folder,org))
                                        parent1_data1 = count_empty_threads(parent1,"parent1")
                                        parent1_data2 = count_connections(parent1,"parent1")
                                        #append data into a csv row
                                        parent1_data_all = parent1_data1[1] + parent1_data2[1]
                                        parent1_header = parent1_data1[0] + parent1_data2[0]

                                    if org.endswith(".txt") and org.startswith(parent2_id):
                                        print "parent2: ", org
                                        #the parent's folder is its name without the .txt file extension
                                        org_folder = org[:-4]
                                        parent2 = json_load_file.json_load_file (os.path.join(parents_location,org_folder,org))
                                        parent2_data1 = count_empty_threads(parent2,"parent2")
                                        parent2_data2 = count_connections(parent2,"parent2")
                                        #append data into a csv row
                                        parent2_data_all = parent2_data1[1] + parent2_data2[1]
                                        parent2_header = parent2_data1[0] + parent2_data2[0]
                            #create csv rows
                            if not header:
                                csv_rows.append(child_data_header + parent1_header + parent2_header)
                                header = True
                            csv_rows.append(child_data_all + parent1_data_all + parent2_data_all)
                        #if the org is of gen 1, just output its data (technically still classified as a child)
                        else:
                            csv_rows.append(child_data_all)
                                        
    #for row in csv_rows:
    #    print row
    results_file = open('child_parent_thread_data.csv', 'a')
    wr = csv.writer(results_file, dialect='excel')
    for row in csv_rows:
        wr.writerow(row)
d = "/Users/Aaron/Projects/Braitenbot_Data/Robot_Data/Development"
compare_all_in_dir(d)

