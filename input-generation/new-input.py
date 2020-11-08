from data import CaseData,OtherData,ProjectData
from os import path
import jj
import csv


casesObject = CaseData()
cases = casesObject.cases
csvFileDir = path.join(path.dirname(path.realpath(__file__)),"new-inputs.csv")
csvFile = open(csvFileDir,"wb")
writer = csv.writer(csvFile)


output={}
for index,case in enumerate(cases):
    # project = ProjectData().findProject(case["project"])
    if not output.has_key(case["project"]+"|"+case["version"]):
        output[case["project"]+"|"+case["version"]] = []

    output[case["project"] + "|" + case["version"]].append(case["name"])


for run in output.keys():
    project_id=run.split("|")[0]
    project = ProjectData().findProject(project_id)
    version=run.split("|")[1]
    crashesArr=output[run]
    # logs_dirs_json = json.dumps(crashesArr)
    crashes=""
    for c in crashesArr:
        crashes=crashes+c+"|"
    crashes = crashes[:-1]

    row= [project["name"],project["package"],version,crashes]
    writer.writerow(row)

csvFile.close()