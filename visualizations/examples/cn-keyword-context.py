#keyword context search and store for college news

#import statements 
import re #regular expressions, checks if a string matches a regular expression
import os #operating system, accesses its information
import csv #provides classes for reading and writing data to a csv file

#search for all instances of a keyword in each college news issue
rows = [] #create list
directory = "/Users/amcgrath1/college-news/issues/" #put directory path to your folder with all college news issues here

keywords = [r'may(\s?)day', r'lantern night']

#keyword = r"word\w*" #create regex object for desired keyword


for filename in os.listdir(directory): #for every file in the folder, do these steps:
    if filename.endswith(".txt"): #if file ends in .txt (which all issue files should):
        newfilename = directory + filename #add folder name to file name
        f = open(newfilename, "r", encoding = "utf-8") #open file
        cn_text = f.read() #read file
        charscount = len(cn_text) #counts characters in file
        chars = 100 #number of desired characters before and after keyword
        n = 0
        for keyword in keywords:
            for instance in re.finditer(keyword, cn_text[n:], flags=re.IGNORECASE): #find keyword, regardless of capitalization, and for each instance do these steps:
                startindex, endindex = instance.span()
                if startindex > chars:
                    startcontext = startindex - chars 
                else:
                    startcontext = 0
                if startindex + chars > charscount - 1:
                    endcontext = charscount - 1
                else:
                    endcontext = startindex + chars
                context = cn_text[startcontext:endcontext] 
                n = endindex
                cleantext = context.replace('\n', ' ')
                data = [filename, keyword, cleantext] #group file name, keyword, and context in a list
                rows.append(data) #put data into rows variable

#write csv file to store keyword information
#use GUI to create and save an empty csv file
header = ["file name", "keyword", "context"] #name header cells
#put saved csv file name below in quotes
with open("lantern-may-context.csv", "w", encoding = "utf-8", newline = '') as outfile: #open and write to csv file
    writer = csv.writer(outfile) #create csv writer
    writer.writerow(header) #write header row
    writer.writerows(rows) #write information rows