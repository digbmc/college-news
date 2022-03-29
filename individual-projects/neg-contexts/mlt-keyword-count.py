#keyword count search and store for individual project (negro and related words in the college news)

#import statements 
import re #regular expressions, checks if a string matches a regular expression
import os #operating system, accesses its information
import csv #provides classes for reading and writing data to a csv file

#search for all instances of a keyword in each college news issue
rows = [] #create list
keyword = "negro" #desired keyword
directory = r"C:\Users\arina\OneDrive\Documents\projects\issues" #directory path to folder with text files of college news issues
for filename in os.listdir(directory): #for every file in the folder, do these steps:
    if filename.endswith(".txt"): #if file ends in .txt (which all should - to avoid processing hidden files)
        newfilename = "issues/" + filename #add folder name to file name
        f = open(newfilename, "r", encoding = "utf-8") #open file
        cn_text = f.read() #read file
        keyword_list = re.findall(keyword, cn_text, flags=re.IGNORECASE) #find all keyword instances, regardless of capitalization, in file
        keywordcount = len(keyword_list) #count keyword instances found
        date = filename[2:12] #pull date from file name
        data = [filename, date, keyword, keywordcount] #group file name, date, keyword, and keyword count in list
        rows.append(data) #put data into rows variable

#write csv file to store keyword count information
header = ["filename", "date", "keyword", "count"] #name header cells
#put desired csv file name below in quotes
with open("cn-negro-count.csv", "w", encoding = "utf-8", newline = '') as outfile: #open and write to csv file
    writer = csv.writer(outfile) #create csv writer
    writer.writerow(header) #write header row
    writer.writerows(rows) #write information rows