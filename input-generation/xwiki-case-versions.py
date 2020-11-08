from data import CaseData
import json

casesObject = CaseData()

cases = casesObject.cases

xwikiVersions = []
xwikiVersionDict = {}
for index,case in enumerate(cases):
    if case["project"] == "0":
        print case
        xwikiVersionDict[case["name"]]=case["version"]
        if case["version"] not in xwikiVersions:
            xwikiVersions.append(case["version"])

print len(xwikiVersions)


versions_json = json.dumps(xwikiVersionDict)

print versions_json

with open('versions.json', 'w') as json_file:
    json.dump(xwikiVersionDict, json_file)