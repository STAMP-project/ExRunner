import os
from sys import argv, version,path
from inputs import Input
dir_path = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(dir_path)
path.insert(0,parentdir)
from botsing import LogReader
from botsing import RunBotsing
from botsing import Observer

is_py2 = version[0] == '2'
if is_py2:
    import Queue as qu
else:
    import queue as qu

if __name__ == '__main__':
    # directories definitions
    dir_path = os.path.dirname(os.path.realpath(__file__))
    # java_file_dir = os.path.join(dir_path, "..", "botsing", "src")
    botsing_libs = os.path.join(dir_path, "..", "botsing", "libs")
    log_path = os.path.join(dir_path, "..", "botsing", "resources", "logs", )



    #get the input arguments (default value is 5):
    maximum_number_of_threads = 5
    isMultiObjective = False
    if len(argv) == 3:
         if argv[1] == "m" or argv[1] == "M":
             isMultiObjective= True

         maximum_number_of_threads = int(argv[2])

    if len(argv) == 2:
        if argv[1].isdigit():
            maximum_number_of_threads = int(argv[1])
        else:
            if argv[1] == "m" or argv[1] == "M":
                isMultiObjective = True


    #initializing logReader
    # logReader = LogReader

    # get inputs from csv
    input_fetcher = Input()
    runs_configs = input_fetcher.fetchInputs()
    number_of_runs = len(runs_configs)
    print ("number of runs: " + str(number_of_runs))

    # Define a queue. all of the runs will be stored in it
    queue = qu.Queue()



    # initilize the log reader
    log_reader = LogReader()

    #add all of the runs to the Queue
    for currentRun in runs_configs:
        # Get valid frames from log files
        validFrames = log_reader.getValidFrameLevels(
        os.path.join(log_path, currentRun["application"].upper(), currentRun["case"].strip(),
        currentRun["case"].strip() + ".log"), currentRun["package"])
        currentRun["getExceptionName"] = log_reader.getExceptionName()
        currentRun["all_frames_count"] = log_reader.getAllFramesCount()
        currentRun["project_frames_count"] = log_reader.getProjectFramesCount()
        currentRun["isMulti"] = 1 if isMultiObjective else 0;
        for frame in validFrames:
            currentRun["frame"] = frame
            queue.put(currentRun.copy())

    #Create observer Thread
    observerThread = Observer(maximum_number_of_threads)
    observerThread.start()


    #Starting threads
    index = 0
    threads = []
    for OneOf in range(maximum_number_of_threads):
        thread = RunBotsing(name=str(index + 1),java_file_dir="",libraryString="",theQueue=queue,observerThread=observerThread,isMultiObjective=isMultiObjective)
        thread.start()
        threads.append(thread)
        index+=1
    try:
        for index, i in enumerate(threads):
            print ("waiting for Thread # " + str(index+1))
            i.join()
    except Exception as exc:
        print (exc)