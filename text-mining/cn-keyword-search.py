#keyword search and store for college news

#import statements 
import re #regular expressions, checks if a string matches a regular expression
import os #operating system, accesses its information
import csv #provides classes for reading and writing data to a csv file

#search for all instances of a keyword in each college news issue
rows = [] #create list
keyword = r'word\w*' #create regex object for desired keyword
directory = r"C:\Users\arina\Desktop\projects\issues" #put directory path to your folder with all college news issues here
for filename in os.listdir(directory): #for every file in the folder, do these steps:
    if filename.endswith(".txt"): #if file ends in .txt (which all issue files should)
        newfilename = "issues/" + filename #add folder name to file name
        f = open(newfilename, "r", encoding = "utf-8") #open file
        cn_text = f.read() #read file
        keyword_list = re.findall(keyword, cn_text, flags=re.IGNORECASE) #find all keyword instances, regardless of capitalization, in file
        keywordcount = len(keyword_list) #count keyword instances found
        date = filename[2:12] #pull date from file name
        data = [filename, date, keyword, keywordcount] #group file name, date, keyword, and keyword count in a list
        rows.append(data) #put data into rows variable

#write csv file to store keyword information
#use GUI to create and save an empty csv file
header = ["filename", "date", "keyword", "count"] #name header cells
#put saved csv file name below in quotes
with open("csv-file-name.csv", "w", encoding = "utf-8", newline = '') as outfile: #open and write to csv file
    writer = csv.writer(outfile) #create csv writer
    writer.writerow(header) #write header row
    writer.writerows(rows) #write information rows