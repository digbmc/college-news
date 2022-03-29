#keyword context search and store for individual project (negro and related words in the college news)

#import statements 
import re #regular expressions, checks if a string matches a regular expression
import os #operating system, accesses its information
import csv #provides classes for reading and writing data to a csv file

#search for all instances of a keyword and its context in each college news issue
rows = [] #create list
directory = r"C:\Users\arina\OneDrive\Documents\projects\issues" #directory path to folder with text files of college news issues
keyword = "negro" #also did negra, negress, negritude, and negru
for filename in os.listdir(directory): #for every file in the folder, do these steps:
    if filename.endswith(".txt"): #if file ends in .txt (which all should - to avoid processing hidden files)
        newfilename = "issues/" + filename #add folder name to file name
        f = open(newfilename, "r", encoding = "utf-8") #open file
        cn_text = f.read() #read file
        charscount = len(cn_text) #count characters in file
        chars = 100 #number of desired characters before and after keyword
        n = 0
        for instance in re.finditer(keyword, cn_text[n:], flags=re.IGNORECASE): #find keyword, regardless of capitalization, and for each instance grab context through steps below:
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
            data = [filename, keyword, context] #group file name, keyword, and context in list
            rows.append(data) #put data into rows variable

#write csv file to store keyword context information
header = ["file name", "keyword", "context"] #name header cells
#put desired csv file name below in quotes
with open("cn-negro-context.csv", "w", encoding = "utf-8", newline = '') as outfile: #open and write to csv file
    writer = csv.writer(outfile) #create csv writer
    writer.writerow(header) #write header row
    writer.writerows(rows) #write information rows