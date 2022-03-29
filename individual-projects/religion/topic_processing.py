"""
Topic Processing for Religion Data
- read context chunks from csv
- generate a unique file name for each chunk
- write each chunk to a text file
- generate metadata csv for new files

"""

import csv # provides classes for reading and writing data to a csv file
import os # interface for accessing information about the operating system

input_file = "/Users/alyssanash/Desktop/DSSF/collegenews/religions-context.csv" # input csv with context data
keywords = {} # create a dictionary
with open(input_file, newline="") as csvfile: # open the input file
    keyword_reader = csv.reader(csvfile, quotechar='"') # read the csv
    header = next(keyword_reader) # skip the header row
    for row in keyword_reader: # for each row in the csv:
        year = row[1][:4] # extract the year from the file name
        religion = row[2] # get the religion name
        context = row[4] # get the context chunk
        if year not in keywords.keys(): # if the year is not in the dictionary:
           keywords[year] = {} # add the year to the dictionary
        if religion in keywords[year].keys(): # if the religion is in the dictionary for that year:
            keywords[year][religion].append(context) # add the context chunk to the list for that religion+year
        else: # if the religion is not in the dictionary:
            keywords[year][religion] = [context] # add it to the dictionary and put the context chunk in the list

if os.path.exists("/Users/alyssanash/Desktop/DSSF/collegenews/individual/topics") == False: # if there isn't already a folder named "topics", make one
        os.mkdir("/Users/alyssanash/Desktop/DSSF/collegenews/individual/topics")

rows = [] # create an empty list

for chunk_year in keywords.keys(): # for every year in the dictionary:
    for chunk_religion in keywords[chunk_year].keys(): # for every religion in the dictionary:
        num = 0 # set a counter
        for chunk in keywords[chunk_year][chunk_religion]: # for every chunk in that year+religion:
            filename = chunk_religion + "_" + chunk_year + "_C" + str(num) + ".txt" # create a filename from the religion, year, and counter
            filepath = "/Users/alyssanash/Desktop/DSSF/collegenews/individual/topics2/" + filename # add the file path to the file name
            num += 1 # update the counter
            meta_row = [filename, chunk_year, chunk_religion] # create a row for the metadata csv
            rows.append(meta_row) # add the metadata row to the list of rows
            with open(filepath, "w") as f: # open a new file
                f.write(chunk) # write the text chunk into the file


# write to new csv in format [filename, year, religion]
header = ["filename", "year", "religion"] # name header cells
with open("religion-chunks-metadata.csv", "w", encoding = "utf-8", newline = '') as outfile: #open and write to csv file
    writer = csv.writer(outfile) #create csv writer
    writer.writerow(header) #write header row
    writer.writerows(rows) #write information rows
