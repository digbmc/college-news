"""
Add Topic Data
- read topic modeling output
- combine with keyword search data
- write to new csv

"""

import csv # provides classes for reading and writing data to a csv file
import re # finds regular expression patterns
from collections import Counter # used to find most frequent topic

topics = {} # create a dictionary
# topic input csv
input_file = "/Users/alyssanash/Desktop/DSSF/collegenews/individual/output/output_csv/topics-in-docs.csv"
with open(input_file, newline="") as csvfile: # open the file
    topic_reader = csv.reader(csvfile, quotechar="'") # create the csv reader
    header = next(topic_reader) # skip the header row
    for row in topic_reader: # for every row:
        filepath = row[1] # get the filepath
        filename = filepath[67:] # extract the filename from the filepath
        match = re.search(r"([\w']+)_([\w']+)_", filename) # isolate the religion and year from the filename
        religion = match.group(1) # get the religion
        year = match.group(2) # get the year
        topic = row[2] # get the most relevant topic for this context chunk
        if year in topics.keys(): # if the year is in the dictionary:
            if religion in topics[year].keys(): # if the religion is in the dictionary for that year:
                topics[year][religion].append(topic) # add the topic 
            else:
                topics[year][religion] = [topic] # create a new list for topics and include this topic
        else:
            topics[year] = {} # create a dictionary for the year
            topics[year][religion] = [topic] # create a list for this religion in this year, adding the topic
top_topics = {} # create new dictionary
for year in topics.keys(): # for each year:
    for religion in topics[year].keys(): # for each religion:
        occurence_count = Counter(topics[year][religion]) # create a Counter object
        if year not in top_topics: # if the year is not in the top topics dictionary, add it
            top_topics[year] = {}
        # set the topic for the religion/year to the most common topic
        top_topics[year][religion] = occurence_count.most_common(1)[0][0] 

topic_file = "/Users/alyssanash/Desktop/DSSF/collegenews/individual/output2/output_csv/topic-words.csv" # topic words input
topic_words = {} # create new dictionary
with open(topic_file, newline="") as csvfile: # open the csv
    topic_reader = csv.reader(csvfile, quotechar="'") # create a csv reader
    header = next(topic_reader) # skip the header row
    for row in topic_reader: # for each row
        key = row[0] # get the number for each topic
        val = row[1] # get the words for each topic
        topic_words[key] = val # add the number + words to the dictionary

rows = [] # create a new list
process_file = "/Users/alyssanash/Desktop/DSSF/collegenews/individuals/religions-processed.csv" # name of file with initial data
with open(process_file, newline="") as csvfile: # open the file
    keyword_reader = csv.reader(csvfile, quotechar="'") # create a csv reader
    header = next(keyword_reader) # skip the header row
    for row in keyword_reader: # for every row:
        year = row[0] # get the year
        religion = row[1] # get the religion
        count = row[2] # get the count
        topic = top_topics[year][religion] # get the top topic
        topic_text = topic + ": " + topic_words[topic] # combine topic number and associated words
        new_row = [year, religion, count, topic_text] # create a new row 
        rows.append(new_row) # add the row to the csv

# write to new csv in format [year, religion, count, topic]
header = ["year", "religion", "count", "topic"] #name header cells
with open("religions-output-topics.csv", "w", encoding = "utf-8", newline = '') as outfile: #open and write to csv file
    writer = csv.writer(outfile) #create csv writer
    writer.writerow(header) #write header row
    writer.writerows(rows) #write information rows