import math #import math module to get access to mathematical functions
import os #import operating system (allows you to navigate or manipulate directories)
import re #import regex module

os.chdir("/Users/averymatteo/Desktop/projects/") #use os.chdir to navigate to where College News issues are stored

inCorpus = "issues" #define inCorpus as issues
outCorpus = "60s-tm" #define outCorpus as the decade you want 

if os.path.exists(outCorpus) == False: #checking to see if outCorpus directory exists
    os.mkdir(outCorpus) #creates outCorpus folder if it doesn't already exist 

filenames = [] #create a list
for root, dirs, files, in os.walk(inCorpus, topdown=False): # os.walk generates the file names from a given directory 
# root: main directory (this case root is inCorpus)
# dirs:  sub-directories from root
# files:  all files from root and directories

    for name in files: #create for loop iterating through files
        if '196' in name: #pulls files that start with 196 (1960s)
            filenames.append(os.path.join(root, name)) #add issues and 196 to list of files

for issue in filenames: #create for loop iterating through every issue
    f = open(issue, 'r', encoding='utf-8') #open and read the issue
    text = f.read() #set text equal to the issue that is read
    f.close() #close text file so it cannot be read or written. important to do to prevent data loss
    characters = len(text) #define characters as the entire length of the text
    chunks = math.floor(characters/500) 
  #chunks: the number of 500 character chunks
  #math.floor: rounds the number down
    
# print(chunks)
# range(chunks)
    issue_name = issue[7:19] #issue_name defined as characters 7 through 19 in the file name, extracting the date "cnYYYY-MM-DD" (not including .txt)
    start=0 #start specfies the beginning of the chunk (character 0)
    stop=500 #stop specfies the end of the chunk (character 500)

    for i in range(chunks): # loop that is specifying the number of chunks and going through them in that order
        # i represents the number of the chunk you are on
        slice = text[start:stop] # extracting the chunk 
        start +=500 #iterates through each successive set of 500 character chunks (index)
        stop +=500 # moves to the next set of 500 characters (index) 
        # start and stop are pointers telling you where you are in the file. each time you are adding 500 
        newfile = outCorpus + "/" + issue_name + '-chunk' + str(i) + '.txt' #create new file name

        f = open(newfile, "w") #open new file created on previous line
        f.write(slice) #writes the chunk to the new file
        f.close() #closes text file




