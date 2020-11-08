import csv


fuckedup_cases=[]

csv_file = open("results.csv")
reader = csv.reader(csv_file)

for row in reader:
    ff_evo=row[9]
    old_ff= 7.0
    # print ff_evo
    non_cleaned_elements=ff_evo.split(']')
    for e in non_cleaned_elements:
        if not e == "":
            temp=e[1:]
            splitted_temp=temp.split(',')
            ff=float(splitted_temp[0])
            tries=splitted_temp[1]
            if len(tries) > 5:
                print "case: " + row[2]
                print "detect: "+tries
                if row[2] not in fuckedup_cases:
                    fuckedup_cases.append(row[2])
                break

            if ff < old_ff:
                old_ff=ff
            else:
                print "case: " + row[2]
                print "detect: "+ff_evo
                if row[2] not in fuckedup_cases:
                    fuckedup_cases.append(row[2])
                break

print "~~~~~~"
print len(fuckedup_cases)
print fuckedup_cases


