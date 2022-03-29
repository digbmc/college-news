"""
Functions for Text-Cleaning
- remove accents
- make lowercase
- remove symbols
- remove hyphens from the end of a line
- remove random strings of characters
- split into words
- lemmatize words 

"""
# import statements
import nltk # to lemmatize and tokenize by word
import re # to find patterns and make substitutions
import unidecode # to remove accents

word = re.compile(r'[a-zA-Z]{2}') # define a word as at least 2 letters in a row
endhyphen = re.compile(r'([a-zA-Z]+)-\s*$') # identify a hyphen at the end of a line
start_line = re.compile(r'^([^a-zA-Z]*)(([a-z]|[A-Z])+)') # identify the first word/fragment of a line
english_vocab = set(w.lower() for w in nltk.corpus.words.words()) # create a set of English words using NLTK
wordnet_lemmatizer = nltk.WordNetLemmatizer() # create a word net lemmatizer

def clean_words(text): # removes zeroes, accents and non-word strings
    no_accents = unidecode.unidecode(text) # remove accents from accented characters 
    no_decor = re.sub(r'\w*(e{3,}|c{3,})\w*', '', no_accents) #gets rid of misrecognized decorations
    no_zeroes = re.sub(r'([a-z]+)0([a-z]+)', r'\1o\2', no_decor) # if there is a zero in the middle of a word, replace it with an "o"
    return no_zeroes # return the string

def fix_hyphens(text): # for a given string, find hyphens at the end of a line and try to join together words that have been split
    lines = text.split("\n") # split into lines using the newline character
    linesclean = [] # create a list for lines with content
    for l in lines: # for every line in the text: 
        linesclean.append(l) # add the line to linesclean
    i = 0
    for c in linesclean: # for each line in our new list:
        if endhyphen.search(c) and i + 1 < len(linesclean): # if there is a hyphen at the end of the line and there is another line after:
            i = linesclean.index(c) # get the index of this line in the list
            target = endhyphen.search(c) # get the result of the search for an end-of-line hyphen
            to_search = linesclean[i+1].strip() # get the next line and remove extra whitespace
            result = start_line.search(to_search) # get the first word/fragment from the beginning of the next line
            if(result): # if there is a match to the previous search:
                fixed = target.group(1) + result.group(2) # combine the two parts 
                lower = fixed.lower() # make the word lowercase
                lem = wordnet_lemmatizer.lemmatize(lower) # lemmatize the word
                if(lem in english_vocab): # if this word is in the English vocabulary set:
                    newline = target.group(1) + to_search[to_search.index(result.group(2)):] # add the beginning of the word to the next line
                    linesclean[i+1] = newline # replace the new line in the list
                    linesclean[i] = c[:c.index(target.group(0))] # remove the beginning of the word from the current line
    output = "\n".join(linesclean) # make the list into a string separated by new line characters
    return output # return the string

def remove_symbols(text): # remove symbols and numbers from a string
    no_symbols = re.sub(r'[^a-z]', " ", text) # replace any non-alphabetical characters with a space
    return no_symbols

def lemmatize(tokens): # lemmatize each word in a list
    wordnet_lemmatizer = nltk.WordNetLemmatizer() # create a word net lemmatizer object
    lemmatized = [] # create a new list
    for t in tokens: # for every word in the input list:
        lemmatized.append(wordnet_lemmatizer.lemmatize(t)) # lemmatize the word and add it to the list
    return lemmatized # return the list of lemmatized words
    
def deep_clean_list(text): # clean the text by running the following steps:
    ocr_cleaner = clean_words(text) # remove zeros, non-word strings, accents
    no_hyphens = fix_hyphens(ocr_cleaner) # fix hyphens at the end of lines
    text_lower = no_hyphens.lower() # make the whole text lowercase 
    no_symbols = remove_symbols(text_lower) # remove symbols 
    words = nltk.word_tokenize(no_symbols) # split into words 
    lemmatized = lemmatize(words) # lemmatize
    return lemmatized # return the cleaned, lemmatized text as a list of words

def clean(text):
    ocr_cleaner = clean_words(text) # remove strings etc.
    no_hyphens = fix_hyphens(ocr_cleaner) # fix hyphens at the end of lines 
    return no_hyphens # return the cleaned version of the text

infile = 'issues/cn1959-10-07.txt' # filepath for input text
with open(infile, 'r', encoding='utf-8') as f: # open the file
    text = f.read() # read the file

clean_text = clean(text) # clean the text
print(clean_text) # print the cleaned text