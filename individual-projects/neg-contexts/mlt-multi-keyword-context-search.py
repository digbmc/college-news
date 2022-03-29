#keyword context search and store for individual project (negro and related words in the college news)

#import statements 
import re #regular expressions, checks if a string matches a regular expression
import os #operating system, accesses its information
import csv #provides classes for reading and writing data to a csv file

#define keyword context search function
def get_contexts(keyword, text, chars):
    n = 0 
    context_passages = []
    for instance in re.finditer(keyword, text[n:], flags=re.IGNORECASE):
        startindex, endindex = instance.span()
        if startindex > chars:
            startcontext = startindex - chars 
        else:
            startcontext = 0
        if startindex + chars > len(text) - 1:
            endcontext = len(text) - 1
        else:
            endcontext = startindex + chars
        context = cn_text[startcontext:endcontext] 
        n = endindex
        cleantext = context.replace('\n', ' ')
        context_passages.append(cleantext)
    return context_passages

#search for keyword and all of its contexts in each college news issue
rows = [] #create a list 
directory = r"C:\Users\arina\OneDrive\Documents\projects\issues" #directory path to folder with text files of college news issues
for filename in os.listdir(directory): #for every file in the folder, do these steps:
    if filename.endswith(".txt"): #if file ends in .txt (which all should - to avoid processing hidden files):
        date = filename[2:12] #slice file name to get date in yyyy-mm-dd format
        newfilename = "issues/" + filename #add folder to file name
        f = open(newfilename, "r", encoding = "utf-8") #open file
        cn_text = f.read() #read file
        keywords = ["negro", "negra", "negress", "negritude", "negru"] #list of desired keywords
        for word in keywords: #for each keyword in list of desired keywords, do these steps:
            passages = get_contexts(word, cn_text, 100) #call keyword context search function
            if len(passages) == 1: #if keyword has one context in file:
                count = len(passages) #count contexts to get number of keyword instances
                context = passages[0] #save context
                data = [filename, date, word, count, context] #group file name, date, keyword, number of keyword instances, and keyword context in a list
                rows.append(data) #put data into rows list
            if len(passages) > 1: #if keyword has more than one context in file:
                alsocount = len(passages) #count contexts to get number of keyword instances
                firstlastcontext = ["First: " + passages[0], #label and save first context
                "Last: " + passages[-1]] #label and save last context
                alsodata = [filename, date, word, alsocount, firstlastcontext] #group file name, date, keyword, number of keyword instances, and keyword context in a list
                rows.append(alsodata) #put data into rows list

#write csv file to store keyword context information
header = ["filename", "date", "keyword", "count", "context"] #name header cells
#put desired csv file name below in quotes
with open("cn-multi-keyword-context.csv", "w", encoding = "utf-8", newline = '') as outfile: #open and write to csv file
    writer = csv.writer(outfile) #create csv writer
    writer.writerow(header) #write header row
    writer.writerows(rows) #write information rows