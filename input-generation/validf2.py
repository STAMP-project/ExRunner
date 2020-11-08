import sys
import fcntl
import csv
import re
import os


## input arguments
execution_idx=sys.argv[1]
application=sys.argv[2]
case=sys.argv[3]
version=sys.argv[4]
frame_level=sys.argv[5]
search_budget=sys.argv[6]
p_object_pool=sys.argv[7]
seed_clone=sys.argv[8]
seed_mutations=sys.argv[9]

dir_path = os.path.dirname(os.path.realpath(__file__))
log_dir = os.path.join(dir_path, "..", "logs",case+"-"+frame_level+"-"+execution_idx+"-out.txt")
out_dir = os.path.join(dir_path, "..", "results","results.csv")
##




### functions
def write_on_csv_file(csv_result,csv_file_dir):
    title_order = [
                   "execution_idx",
                   "application",
                   "case",
                   "version",
                   "exception_name",
                   "frame_level",
                   "search_budget",
                   "fitness_function_value",
                   "number_of_fitness_evaluations",
                   "fitness_function_evolution",
                   "p_object_pool",
                   "seed_clone",
                   "seed_mutations"
                   ]

    fields = []

    for cell in title_order:
        if cell in csv_result.keys():
            fields.append(csv_result[cell])
        else:
            fields.append("")

    with open(csv_file_dir, "a") as  g:
        fcntl.flock(g, fcntl.LOCK_EX)
        writer = csv.writer(g)
        writer.writerow(fields)
        fcntl.flock(g, fcntl.LOCK_UN)
###



csv_result = {"execution_idx": execution_idx,
              "application": application,
              "case": case,
              "version": version,
              "frame_level": frame_level,
              "search_budget": search_budget,
              "p_object_pool": p_object_pool,
              "seed_clone": seed_clone,
              "seed_mutations": seed_mutations,
              "fitness_function_value":"",
              "fitness_function_evolution":""}

with open(log_dir, "r") as ins:
    for stdout_line in ins:
        if  "Best fitness in the current population" in stdout_line:
            splitted_line_1 = stdout_line.split("population:")
            splitted_line_1 = splitted_line_1[1].split("|")
            csv_result["number_of_fitness_evaluations"] = int(re.sub("[^0-9]", "", splitted_line_1[1]))
            distribution_ff = splitted_line_1[0].strip()
            if distribution_ff != csv_result["fitness_function_value"]:
                csv_result["fitness_function_value"]=distribution_ff
                csv_result["fitness_function_evolution"]+="["+distribution_ff+","+str(csv_result["number_of_fitness_evaluations"])+"]"
        elif "Exception type is detected:" in stdout_line:
            splitted_line_1 = stdout_line.split("Exception type is detected: ")
            csv_result["exception_name"]=splitted_line_1[1].replace('\n', ' ').replace('\r', '').strip()
        elif "Best fitness in the initial population is:" in stdout_line:
            splitted_line_1 = stdout_line.split("population is:")
            csv_result["number_of_fitness_evaluations"] = 100
            distribution_ff = splitted_line_1[1].strip()
            csv_result["fitness_function_value"]=distribution_ff
            csv_result["fitness_function_evolution"]+="["+distribution_ff+","+str(csv_result["number_of_fitness_evaluations"])+"]"



write_on_csv_file(csv_result,out_dir)
