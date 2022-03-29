#keyword context search and store for college news
# Writes small files containing context passages for each issue in which the keyword is mentioned

#import statements 
import re #regular expressions, checks if a string matches a regular expression
import os #operating system, accesses its information
import csv #provides classes for reading and writing data to a csv file

#search for all instances of a keyword in each college news issue
rows = [] #create list
directory = "/Users/Aanandi/Desktop/projects/issues/" #put directory path to your folder with all college news issues here

keywords = [r'india', r'pakistan',r'hindu',r'muslim']

#keyword = r"word\w*" #create regex object for desired keyword


for filename in os.listdir(directory): #for every file in the folder, do these steps:
    if filename.endswith(".txt"): #if file ends in .txt (which all issue files should):
        newfilename = directory + filename #add folder name to file name
        f = open(newfilename, "r", encoding = "utf-8") #open file
        cn_text = f.read() #read file
        date = filename[2:12]
        charscount = len(cn_text) #counts characters in file
        chars = 200 #number of desired characters before and after keyword
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
                n = endcontext
                cleantext = context.replace('\n', ' ')
                data = [filename, keyword, cleantext, date] #group file name, keyword, and context in a list
                rows.append(data) #put data into rows variable

#write csv file to store keyword information
#use GUI to create and save an empty csv file
header = ["file name", "keyword", "context","date"] #name header cells
#put saved csv file name below in quotes
with open("india-pakistan4.csv", "w", encoding = "utf-8", newline = '') as outfile: #open and write to csv file
    writer = csv.writer(outfile) #create csv writer
    writer.writerow(header) #write header row
    writer.writerows(rows) #write information rows

# contexts = {}
# for item in rows:
#     filename = item[0]
#     key = item[1]
#     con = item[2]
#     date= item[3]        
#     newfile = key[0:3] + '-' + filename
#     if newfile not in contexts.keys():
#         contexts[newfile] = con
#     else:
#         contexts[newfile] += '\n' + con


# outfile = "/Users/Aanandi/projects/india-pakistan-chunks/"
# for item in contexts:
#     outpath = outfile + item
#     with open (outpath, 'w', encoding='utf-8') as f:
#         f.write(contexts[item])
