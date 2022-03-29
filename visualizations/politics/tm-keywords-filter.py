import math #import math module to get access to mathematical functions
import os #import operating system (allows you to navigate or manipulate directories)
import re #import regex module

# defines function that searches a given piece of text for a given regex and returns a count of how many times that keyword appears
def countkeys(regex, text): # this function requires two variables: a regular expression and a longer string
    keyword_list = re.findall(regex, text, flags=re.IGNORECASE) #find all keyword instances, regardless of capitalization, in text
    keywordcount = len(keyword_list) # count keyword instances found
    return keywordcount # output of the function is
    
keywords= [
    ['world war', r"world\swar"],
    ['political party', r"political\sparty"], 
    ['foreign policy', r"foreign\spolicy"], 
    ['united states', r"united/sstates"],
    ['russia', r"russia"],
    ['peace', r"peace"], 
    ['china', r"china"], 
    ['nations', r"nations"], 
    ['country', r"country"], 
    ['government', r"government"],
    ['american', r"american"]
    ]

os.chdir("/Users/Aanandi/Desktop/projects/") #use os.chdir to navigate to where College News issues are stored

inCorpus = "issues" #define inCorpus as issues
outCorpus = "50s-60s-tm" #define outCorpus as the decade you want 

if os.path.exists(outCorpus) == False: #checking to see if outCorpus directory exists
    os.mkdir(outCorpus) #creates outCorpus folder if it doesn't already exist 
for filename in os.listdir(directory): #for every file in the folder, do these steps:
    if filename.endswith(".txt"): #if file ends in .txt (which all should - to avoid processing hidden files)
         filepath =inCorpus + "/" + filename
         f = open(filepath, 'r', encoding='utf-8') #open and read the issue
         text = f.read() #set text equal to the issue that is read
         f.close() #close text file so it cannot be read or written. important to do to prevent data loss

   
for key in keywords:
            count =countkeys(key,text) # in the case that count = 5
            if count ==0:
                continue 
            elif count > 0:
                newfilename = outCorpus + "/" + filename #create new file name
                f = open(newfilename, "w") #open new file created on previous line
                f.write(text) #writes the chunk to the new file
                f.close() #closes text file
                break



    
# print(chunks)
# range(chunks)
    
