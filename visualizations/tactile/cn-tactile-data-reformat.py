#this is all Al Nash's code
# process list of place mentions into list of unique place names

import csv

# read the csv
input_file = "commencement-gpe-full-clean.csv"
counts = {} # create empty dictionary for total count of mentions
issues = {}
variations = {}
with open(input_file, newline="") as csvfile: # open the input file
    input_reader = csv.reader(csvfile) # read the csv
    header = next(input_reader)
    for row in input_reader: # for every row in the csv:
        issue = row[0]
        gpe = row[1]
        gpe_clean = row[2]
        count = row[3]
        if gpe_clean in counts.keys():
            counts[gpe_clean] += int(count)
            issues[gpe_clean].add(issue)
            variations[gpe_clean].add(gpe)
        else:
            counts[gpe_clean] = int(count)
            issues[gpe_clean] = {issue}
            variations[gpe_clean] = {gpe}

# add up counts for each place name
rows = []
header = ["place", "total count", "number of issues", "variations"]
for place in counts.keys():
    row = [place, counts[place], len(issues[place]), variations[place]]
    rows.append(row)

# print to csv
with open("commencement-gpe-reformat.csv", "w", encoding = "utf-8", newline = '') as outfile: #open and write to csv file
    writer = csv.writer(outfile) #create csv writer
    writer.writerow(header) #write header row
    writer.writerows(rows) #write information rows