"""
Multiple Keywords Context Search
- read every file in the corpus
- clean the file using the code from the text-cleaning.py file in the corpus-cleaning folder
- search for a list of different religion keywords
- write the instance and its context to a csv

"""
# import statements 
import re # regular expressions, checks if a string matches a regular expression
import os # operating system, accesses its information
import csv # provides classes for reading and writing data to a csv file
import nltk # to lemmatize and tokenize by word
import unidecode # to remove accents
word = re.compile(r'[a-zA-Z]{2}') # define a word as at least 2 letters in a row
endhyphen = re.compile(r'([a-zA-Z]+)-\s*$') # identify a hyphen at the end of a line
start_line = re.compile(r'^([^a-zA-Z]*)(([a-z]|[A-Z])+)') # identify the first word/fragment of a line
english_vocab = set(w.lower() for w in nltk.corpus.words.words()) # create a set of English words using NLTK

def fix_hyphens(text): # for a given string, find hyphens at the end of a line and try to join together words that have been split
    lines = text.split("\n") # split into lines using the newline character
    linesclean = [] # create a list for lines with content
    for l in lines: # for every line in the text: 
            if word.search(l): # if there are at least 2 alphabetical characters in a row:
                linesclean.append(l) # add the line to linesclean
    for c in linesclean: # for each line in our new list:
        if endhyphen.search(c): # if there is a hyphen at the end of the line and there is another line after:
            i = linesclean.index(c) # get the index of this line in the list
            if i + 1 < len(linesclean):
                target = endhyphen.search(c) # get the result of the search for an end-of-line hyphen
                to_search = linesclean[i+1].strip() # get the next line and remove extra whitespace
                result = start_line.search(to_search) # get the first word/fragment from the beginning of the next line
                if(result): # if there is a match to the previous search:
                    fixed = target.group(1) + result.group(2) # combine the two parts 
                    lower = fixed.lower() # make the word lowercase
                    wordnet_lemmatizer = nltk.WordNetLemmatizer() # create a word net lemmatizer
                    lem = wordnet_lemmatizer.lemmatize(lower) # lemmatize the word
                    if(lem in english_vocab): # if this word is in the English vocabulary set:
                        newline = target.group(1) + to_search[to_search.index(result.group(2)):] # add the beginning of the word to the next line
                        linesclean[i+1] = newline # replace the new line in the list
                        linesclean[i] = c[:c.index(target.group(0))] # remove the beginning of the word from the current line
    output = "\n".join(linesclean) # make the list into a string separated by new line characters
    return output # return the string
                    
def remove_symbols(text): # remove symbols from a string
    no_zeroes = re.sub(r'([a-z]+)0([a-z]+)', r'\1o\2', text) # if there is a zero in the middle of a word, replace it with an "o"
    no_symbols = re.sub(r'[^a-z]', " ", no_zeroes) # replace any non-alphabetical characters with a space
    return no_symbols # return the string

def lemmatize(tokens): # lemmatize each word in a list
    wordnet_lemmatizer = nltk.WordNetLemmatizer() # create a word net lemmatizer object
    lemmatized = [] # create a new list
    for t in tokens: # for every word in the input list:
        lemmatized.append(wordnet_lemmatizer.lemmatize(t)) # lemmatize the word and add it to the list
    return lemmatized # return the list of lemmatized words
    
def clean(text): # clean the text by running the following steps:
    text_unaccented = unidecode.unidecode(text) # remove accents from accented characters
    no_hyphens = fix_hyphens(text_unaccented) # fix hyphens at the end of lines
    text_lower = no_hyphens.lower() # make the whole text lowercase 
    no_symbols = remove_symbols(text_lower) # remove symbols 
    words = nltk.word_tokenize(no_symbols) # split into words 
    lemmatized = lemmatize(words) # lemmatize
    return lemmatized # return the cleaned version of the text

# search for all instances of a keyword in each CN issue
rows = [] # create list
directory = "/Users/alyssanash/Desktop/DSSF/collegenews/issues/" # directory path to all college news issues 
# dictionary of keywords
keyword_dict = {"Baha'i": [r"bahai.{0,2}\s"], "Buddhism": [r"buddhi.{2,4}\s"], "Catholicism": [r"cathol.{2,6}\s"], "Confucianism": [r"confuciani.{2,5}\s"], "Druze": [r"druze.{0,2}\s"], "Hinduism": [r"hindu\s", r"hindus", r"hinduis.{1,4}\s"], "Interfaith": [r"interfaith"], "Islam": [r"muslim.{0,2}\s", r"moslem.{0,2}\s", r"islam[^e]{0,4}\s"], "Jainism": [r"jainism"], "Judaism": [r"\sjew[^a-z]", r"jews", r"jewish", r"juda[e|i].{2,5}\s"], "Mormonism": [r"mormon.{0,4"], "Shinto": [r"shinto."], "Sikhism": [r"\ssikh.{0,4}\s"], "Taoism": [r"taois.{1,3}\s"], "Zoroastrianism": [r"zoroastr.{3,6}\s"]}

for filename in os.listdir(directory): # for every file in the folder, do these steps:
    if filename.endswith(".txt"): # if file ends in .txt (which all issue files should):
        newfilename = directory + filename # add folder name to file name
        f = open(newfilename, "r", encoding = "utf-8") # open file
        cn_text = f.read() # read file
        cleaned_text = " ".join(clean(cn_text)) # clean the text and turn the list back into a string
        len_text = len(cleaned_text) # counts characters in file
        chars = 250 # number of desired characters before and after keyword
        for keyword in keyword_dict.keys(): # for every religion name:
            for key_regex in keyword_dict[keyword]: # for each keyword associated with that religion
                for instance in re.finditer(key_regex, cleaned_text, flags=re.IGNORECASE): #find keyword, regardless of capitalization, and for each instance do these steps:
                    startindex, endindex = instance.span() # get the starting and ending indices for the match
                    if startindex > chars: # if the starting character is more than 250 characters
                        startcontext = startindex - chars # start the context chunk 250 characters before the match
                    else: # otherwise, start at the beginning of the string
                        startcontext = 0
                    if startindex + chars > len_text: # if there are less than 250 characters after the starting character:
                        endcontext = len_text # go up to the end of the string
                    else: # otherwise, go up to 250 chars after
                        endcontext = startindex + chars
                    context = cleaned_text[startcontext:endcontext] # extract the context chunk
                    date = filename[2:12] # extract the date from the file name
                    data = [filename, date, keyword, key_regex, context] #group file name, keyword, and context in a list
                    rows.append(data) # add the data into the list of rows
        f.close() # close the file

#write csv file to store keyword information
header = ["file name", "date", "religion", "keyword", "context"] #name header cells
with open("religions-context.csv", "w", encoding = "utf-8", newline = '') as outfile: #open and write to csv file
    writer = csv.writer(outfile) #create csv writer
    writer.writerow(header) #write header row
    writer.writerows(rows) #write information rows
