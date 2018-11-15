import re
from os import path, makedirs
import errno
import fcntl
import csv

class BotsingOutputAnalysor():
    def analyze(self,stdout_line,csv_result,thread_name,population):
        reporter = "Thread #"+thread_name+ " : "
        if "Starting the dependency analysis." in stdout_line:
            print(reporter+"Starting the dependency analysis")
        elif "Analysing dependencies done!" in stdout_line:
            print(reporter+"Analysing dependencies done!")
        elif "The target method is public!" in stdout_line:
            csv_result["is_public/protected"] = "No"
        elif "Initializing the first population with size of" in stdout_line:
            print(reporter + "Initializing the first population")
        elif "The new best fitness value (" in stdout_line:
            splitted_line_1 = stdout_line.split(">):")
            splitted_line_1 = splitted_line_1[1].split("|")
            ff = splitted_line_1[0]
            fitness_value_evaluation = int(re.sub("[^0-9]", "", splitted_line_1[1]))
            time_passed = ""
            if len(splitted_line_1) >= 3:
                time_passed = long(re.sub("[^0-9]", "", splitted_line_1[2]))
                time_passed = ", "+str(time_passed)
            if "fitness_function_evolution" in csv_result:
                csv_result["fitness_function_evolution"] += "["+ff+", "+str(fitness_value_evaluation)+str(time_passed)+"]"
            else:
                csv_result["fitness_function_evolution"] = "["+ff+", "+str(fitness_value_evaluation)+str(time_passed)+"]"

            csv_result["fitness_function_value"] = ff
            csv_result["fitness_function_time"] = re.sub("[^0-9]", "", time_passed)
            csv_result["fitness_evaluations"] = str(fitness_value_evaluation)
            print (reporter+"The new best fitness value is: "+ff+" -> "+splitted_line_1[1])
        elif "Best fitness in the current population" in stdout_line:
            splitted_line_1 = stdout_line.split(">):")
            splitted_line_1 = splitted_line_1[1].split("|")
            fitness_evaluation = int(re.sub("[^0-9]", "", splitted_line_1[1]))
            time_passed=""
            if len(splitted_line_1) >= 3:
                time_passed = long(re.sub("[^0-9]", "", splitted_line_1[2]))
                time_passed = str(time_passed)+" Seconds"
            if fitness_evaluation % (int(population)*10) == 0:
                print(reporter+"Search duration: "+str(fitness_evaluation)+" fitness evaluations "+str(time_passed))
        elif "** The search process is finished." in stdout_line:
            print(reporter+"The search process is finished.")


    def save_logs(self,err,csv_result,error_path):
        #write err
        filename = path.join(error_path,csv_result["case"]+"-frame"+str(csv_result["frame_level"])+"-"+"err.txt")
        if not path.exists(path.dirname(filename)):
            try:
                makedirs(path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        f=open(filename,"w")
        f.write(err)
        f.close()

    def write_on_csv_file(self, csv_result):
        csv_file_dir = path.join(path.dirname(path.realpath(__file__)),"..", "experiment-runner","outputs", "csv", "results.csv")
        title_order = ["application",
                       "case",
                       "version",
                       "execution_idx",
                       "exception_name",
                       "frame_level",
                       "p_functional_mocking",
                       "functional_mocking_percent",
                       "p_reflection_on_private",
                       "reflection_start_percent",
                       "search_budget",
                       "population",
                       "fitness_function_value",
                       "fitness_function_time",
                       "fitness_evaluations",
                       "fitness_function_evolution"
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


