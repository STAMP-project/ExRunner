import sys
import json
import os

## input arguments
project=sys.argv[1]
version=sys.argv[2]
target_class=sys.argv[3]
dir_path = os.path.dirname(os.path.realpath(__file__))
xml_path= os.path.join(dir_path, "..", "..",  "analysis-result",project,project+"-"+version,"carvedTests","tests.xml")
##

result="none"

with open(xml_path) as f:
    data = json.load(f)

if data.has_key(target_class):
    list=data[target_class]
    if len(list) > 0:
        result=""
        for test in list:
            result+=(test+":")
        result = result[:-1]
print result