import threading
from os import path,chdir, makedirs
import json
import re
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




class RunBotsing(threading.Thread):
    def __init__(self, name, java_file_dir, libraryString, theQueue=None, observerThread=None,isMultiObjective=False):
        threading.Thread.__init__(self)
        self.theQueue = theQueue
        self.java_file_dir = java_file_dir
        self.name = name
        self.libraryString = libraryString
        self.observerThread = observerThread
        self.isMultiObjective = isMultiObjective

        print ("Thread #" + name + " is initialized.")


class Observer(threading.Thread):
    def __init__(self,number_of_threads_to_observe):
        threading.Thread.__init__(self)
        print "Observer Thread is initialized"