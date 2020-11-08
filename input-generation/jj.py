from sys import argv
import json


inputs= []
for index, argument in enumerate(argv, start=0):
    if index == 0:
        continue

    inputs.append(argument)
print json.__file__
print json.dumps(inputs)
