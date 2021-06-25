#keyword search and store for college news

#import statements 
import re #regular expressions, checks if a string matches a regular expression
import os #operating system, accesses its information
#import datetime #provides classes for working with dates and times: use only if you need to alter date format
import csv #provides classes for reading and writing data to a csv file

#search for all instances of a keyword in each college news issue
rows = [] #create a list
directory = "/Users/amcgrath1/college-news/issues/" #put directory path to your folder with all college news issues here after r and in quotes


#filenames = os.listdir(directory)
keyword = r'word\w*' #create regex object for your given keyword

for filename in os.listdir(directory): #for every file in the folder, do these steps:
    if filename.endswith(".txt"): #if file ends in .txt (which all should)
        ### NB: path for PC is different
        newfilename = directory + filename #add folder name to file name
        f = open(newfilename, "r", encoding = "utf-8") #open file
        cn_text = f.read() #read file
        #keyword = "word" #put desired keyword here in quotes
        #if needed, put keyword with regex token below in quotes
        keyword_list = re.findall(keyword, cn_text, flags=re.IGNORECASE) #find all keyword instances, regardless of capitalization, in file
        keywordcount = len(keyword_list) #count keyword instances found
        #match = re.search(r"\d{4}-\d{2}-\d{2}", filename) #search file name for date
        #date = datetime.datetime.strptime(match.group(), "%Y-%m-%d").date() #pull date from rest of file name
        date = filename[2:12] # slice the filename to get date yyyy-mm-dd
        data = [filename, date, keyword, keywordcount] #group file name (minus issues/ and .txt parts), date, keyword, and keyword count in a list
        rows.append(data) #put data into rows variable

#write csv file to store keyword information
#use GUI to create and save an empty csv file
header = ["filename", "date", "keyword", "count"] #name header cells
#put saved csv file name below in quotes
with open("testsearch3.csv", "w", encoding = "utf-8", newline = '') as outfile: #open and write to csv file
    writer = csv.writer(outfile) #create csv writer
    writer.writerow(header) #write header row
    writer.writerows(rows) #write information rows
