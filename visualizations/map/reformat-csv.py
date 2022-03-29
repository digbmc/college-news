"""
Process list of place mentions into list of unique place names
- read csv of individual mentions (cleaned in OpenRefine)
- track the number of mentions, number of issues, and variations for each keyword
- write results to a csv
"""

import csv # used to read and write data in a csv format

# read and process the csv
input_file = "geomapping/gpe-full-july12-cleaning.csv" # filepath for input file
counts = {} # create dictionary for total count of mentions of the keyword
issues = {} # create dictionary for different issues associated with a keyword
variations = {} # create dictionary for the variations of the keyword
with open(input_file, newline="") as csvfile: # open the input file
    input_reader = csv.reader(csvfile) # read the csv
    header = next(input_reader) # skip the header line of the csv
    for row in input_reader: # for every row in the csv:
        issue = row[0] # select the issue filename
        gpe = row[1] # select the original name of the location
        gpe_clean = row[2] # select the cleaned name of the location
        count = row[3] # select the number of mentions of this location in this issue
        if gpe_clean in counts.keys(): # if the location is already in our dictionaries:
            counts[gpe_clean] += int(count) # add the count to the total count
            issues[gpe_clean].add(issue) # add the issue to the issues set
            variations[gpe_clean].add(gpe) # add the variation to the variations set
        else:
            counts[gpe_clean] = int(count) # set the total count to the current count
            issues[gpe_clean] = {issue} # create a set of issues and add the current issue
            variations[gpe_clean] = {gpe} # create a set of variations and add the current spelling

# add up counts for each place name
rows = [] # create an empty list of rows to write to a csv
header = ["place", "total count", "number of issues", "variations"] # create the header for the csv
for place in counts.keys(): # for each location found in the input csv: 
    row = [place, counts[place], len(issues[place]), variations[place]] # make a row of the place, total counts, total issues, and variations
    rows.append(row) # add the row to the list of rows

# write to csv
with open("gpe-processed.csv", "w", encoding = "utf-8", newline = '') as outfile: #open and write to csv file
    writer = csv.writer(outfile) #create csv writer
    writer.writerow(header) #write header row
    writer.writerows(rows) #write information rows