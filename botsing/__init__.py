import threading
from os import path, makedirs
import json
import re
from time import time,sleep
from subprocess import PIPE,Popen
import errno
from helper import BotsingOutputAnalysor
# Read stack trace and find valid frames


class LogReader():
    ExceptionName = ""
    all_frames_count = 0
    project_frames_count = 0

    def getValidFrameLevels(self, log_dir, project_package):
        self.all_frames_count = 0
        self.project_frames_count = 0
        #reading Exceptions:
        dir_path = path.dirname(path.realpath(__file__))
        with open(path.join(dir_path,"..","experiment-runner","inputs","exceptions.txt"), 'r') as content_file:
            content = content_file.read()
        exceptionList = json.loads(content)
        for index,ex in enumerate(exceptionList):
            exceptionList[index] = re.sub(r"\W", "", ex)
        valid_frames = []
        log_file = open(log_dir, "r")
        counter = 0
        for line in log_file:

            if re.sub(r"\W", "", line) not in exceptionList:
                if counter > 0:
                    splited_line = line.split('.')
                    if len(splited_line) > 1 and (project_package in splited_line or self.appeared_in_other_format(project_package,splited_line)):
                        valid_frames.append(counter)
                        self.project_frames_count += 1
                    if (line.lstrip() != ""):
                        self.all_frames_count += 1
                else:
                    splited_line = line.split(':')
                    self.ExceptionName = splited_line[0]
            counter += 1

        log_file.close();
        return valid_frames

    def appeared_in_other_format(self,project_package,splited_line):
        result =  False
        for part in splited_line:
            if ''.join([i for i in project_package if not i.isdigit()]) == ''.join([i for i in part if not i.isdigit()]):
                result = True
        return result


    def getExceptionName(self):
        return self.ExceptionName

    def getAllFramesCount(self):
        return self.all_frames_count

    def getProjectFramesCount(self):
        return self.project_frames_count




class RunJar(threading.Thread):
    botsing_path = path.dirname(path.realpath(__file__))

    def __init__(self, name, java_file_dir, libraryString, theQueue=None, observerThread=None,isMultiObjective=False):
        threading.Thread.__init__(self)
        self.theQueue = theQueue
        self.java_file_dir = java_file_dir
        self.name = name
        self.libraryString = libraryString
        self.observerThread = observerThread
        self.isMultiObjective = isMultiObjective

        print ("Thread #" + name + " is created.")
    # if achieved to computation finished, stop the process and its threads.
    def kill_for_threshold(self,process,configurations):
        print ("*******************")
        print ("Reporter #" + self.name + ":" + "The following Procces is pass threshold: ")
        print ("Case: " + configurations["case"])
        print ("frame level: " + str(configurations["frame"]))
        print ("population: " + str(configurations["population"]))
        print ("final fitness function should not be empty!")
        print ("*******************")
        process.terminate()

    def run(self):
        log_helper = BotsingOutputAnalysor()
        while not self.theQueue.empty():
            csv_result = {}
            configurations = self.theQueue.get()
            log_dir = path.join(self.botsing_path,"resources","logs",configurations["application"].upper(),configurations["case"],configurations["case"]+".log")
            bins_dir = path.join(self.botsing_path,"resources","targeted-software",configurations["application"].upper()+"-bins",configurations["application"].upper()+"-"+configurations["version"])
            self.theQueue.task_done()
            cmd = ["java","-Xmx4000m","-jar",path.join(self.botsing_path,"libs","botsing.jar"),"-crash_log",log_dir,"-projectCP",bins_dir,"-target_frame",str(configurations["frame"])]
            popen = Popen(cmd, stdout=PIPE, stderr=PIPE, universal_newlines=True)
            csv_result["is_protected/private"] = "Yes"
            self.dir_path = path.dirname(path.realpath(__file__))
            execution_log_path = path.join(self.dir_path,"..","experiment-runner", "outputs", "logs", configurations["case"],
                                               "frame-" + str(configurations["frame"]),
                                               "R" + str(configurations["execution_idx"]) + "_PM" + configurations[
                                                   "p_functional_mocking"] + "_Mperc" + configurations[
                                                   "functional_mocking_percent"] + "_SB" + configurations[
                                                   "search_budget"] + "_POP" + configurations["population"], "out")

            # openning out log file
            filename = path.join(execution_log_path,
                                 configurations["case"] + "-frame" + str(configurations["frame"]) + "-" + "out.txt")
            if not path.exists(path.dirname(filename)):
                try:
                    makedirs(path.dirname(filename))
                except OSError as exc:  # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise

            self.observerThread.start_process(int(self.name), popen, configurations)
            try:
                error = popen.stderr
                f = open(filename, "w")
                evalIndicator=0
                for stdout_line in iter(popen.stdout.readline, ""):
                    log_helper.analyze(stdout_line,csv_result,self.name,configurations["population"])
                    f.write(stdout_line)

            finally:
                self.observerThread.process_is_finished(int(self.name))
                f.close()
            print ("Reporter #" + self.name + " _ Case " + configurations["case"] +" _ Frame "+str(configurations["frame"])+" _ Population "+str(configurations["population"])+": EvoCrash Execution is finished. out log file is saved.")
            csv_result["application"] = configurations["application"]
            csv_result["case"] = configurations["case"]
            csv_result["version"] = configurations["version"]
            csv_result["execution_idx"] = configurations["execution_idx"]
            csv_result["frame_level"] = str(configurations["frame"])
            csv_result["exception_name"] = configurations["getExceptionName"]
            csv_result["p_functional_mocking"] = configurations["p_functional_mocking"]
            csv_result["functional_mocking_percent"] = configurations["functional_mocking_percent"]
            csv_result["p_reflection_on_private"] = configurations["p_reflection_on_private"]
            csv_result["reflection_start_percent"] = configurations["reflection_start_percent"]
            csv_result["search_budget"] = configurations["search_budget"]
            csv_result["population"] = configurations["population"]
            error_path = path.join(self.dir_path,"..", "experiment-runner","outputs""logs",configurations["case"],"frame-"+str(configurations["frame"]),"R"+str(configurations["execution_idx"])+"_PM"+configurations["p_functional_mocking"]+"_Mperc"+configurations["functional_mocking_percent"]+"_SB"+configurations["search_budget"]+"_POP"+configurations["population"],"err")
            log_helper.save_logs(str(error), csv_result,error_path)
            log_helper.write_on_csv_file(csv_result)
            print ("Reporter #" + self.name + " _ Case " + configurations["case"] + " _ Frame " + str(
                configurations["frame"]) + " _ Population " + str(
                configurations["population"]) + ": results are added to csv file")

        self.observerThread.finishing_thread(int(self.name))



class Observer(threading.Thread):
    list_of_threads = []
    max_time = 10 * 60  # if Crash Replication tool does not response for 10 minutes, the observer will stop that instance of the tool.

    def __init__(self, number_of_threads_to_observe):
        threading.Thread.__init__(self)
        for i in range(number_of_threads_to_observe):
            threadDic = {}
            threadDic["alive"] = True
            threadDic["startTime"] = None
            threadDic["lastOutput"] = None
            threadDic["process"] = None
            threadDic["configurations"] = None
            self.list_of_threads.append(threadDic)

    def observer_kill(self, process, configurations):
        print ("~~~~~~~~~~~~~~~~~~~")
        print ("Reporter #" + self.name + ":" + "The following Procces is killed by observer: ")
        print ("Case: " + configurations["case"])
        print ("frame level: " + str(configurations["frame"]))
        print ("population: " + str(configurations["population"]))
        print ("~~~~~~~~~~~~~~~~~~~")
        process.terminate()  # the process and its children will be terminated

    def run(self):
        while True:
            killme = True
            for th in self.list_of_threads:
                if th["alive"]:
                    killme = False
                    break

            if killme:
                break

            for index, th in enumerate(self.list_of_threads):
                if th["startTime"] is not None:
                    timepassed = time() - th["startTime"]
                    if timepassed >= self.max_time:
                        self.observer_kill(th["process"], th["configurations"])
                        self.process_is_finished(index + 1)

            sleep(10)

    def start_process(self, id, process, configurations):
        index = id - 1
        self.list_of_threads[index]["alive"] = True
        self.list_of_threads[index]["startTime"] = time()
        self.list_of_threads[index]["lastOutput"] = time()
        self.list_of_threads[index]["process"] = process
        self.list_of_threads[index]["configurations"] = configurations

    def new_output(self, id):
        index = id - 1
        self.list_of_threads[index]["lastOutput"] = time()

    def process_is_finished(self, id):
        index = id - 1
        self.list_of_threads[index]["startTime"] = None
        self.list_of_threads[index]["lastOutput"] = None
        self.list_of_threads[index]["process"] = None
        self.list_of_threads[index]["configurations"] = None

    def finishing_thread(self, id):
        index = id - 1
        self.list_of_threads[index]["alive"] = False
        self.process_is_finished(id)
