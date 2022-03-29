"""
Process Religion CSV
- read file with each instance of religion mentions
- combine and reformat so that each row represents one religion in one year
- write to new CSV

"""

import csv #provides classes for reading and writing data to a csv file
# input csv containing each instance as one row
input_file = "/Users/alyssanash/Desktop/DSSF/collegenews/individual/religions-context.csv"
keywords = {} # create empty dictionary
with open(input_file, newline="") as csvfile: # open the file
    keyword_reader = csv.reader(csvfile, quotechar="'") # create csv reader
    header = next(keyword_reader) # skip the header row
    for row in keyword_reader: # for every row:
        year = row[1][:4] # get the year from the file name
        religion = row[2] # get the religion name
        if year in keywords.keys(): # if the year is already in the dictionary:
            if religion in keywords[year].keys(): # if the religion is already in the dictionary for that year:
                keywords[year][religion] += 1 # increase the count by 1
            else: # if it's not in the dictionary for that year: 
                keywords[year][religion] = 1 # add it to the dictionary with a count of 1
        else: # if the year is not already in the dictionary
            keywords[year] = {} # create an empty dictionary for the year
            keywords[year][religion] = 1 # add the religion to the dictionary for the year with a count of 1

rows = [] # create an empty list
for year in keywords.keys(): # for each year:
    for religion in keywords[year].keys(): # for each religion mentioned in that year:
        row = [year, religion, keywords[year][religion]] # create a row representing the year, religion, and number of mentions
        rows.append(row) # add the row to the rows list

# write to new csv in format [year, religion, count]
header = ["year", "religion", "count"] #name header cells
with open("religions-processed.csv", "w", encoding = "utf-8", newline = '') as outfile: #open and write to csv file
    writer = csv.writer(outfile) #create csv writer
    writer.writerow(header) #write header row
    writer.writerows(rows) #write information rows

