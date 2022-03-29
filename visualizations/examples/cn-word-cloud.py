"""
Basic word-cloud generator:
- separates all of the files by decade
- reads each decade's files into a string
- generates and displays word cloud of most frequent words from that string

"""
import os # used to get the names of the files
from wordcloud import WordCloud # generates the word clouds
from wordcloud import STOPWORDS # list of words to exclude
import matplotlib.pyplot as plt # used to display the word clouds


stop_words = STOPWORDS.copy() # create a copy of the stop words list
new_stop_words = ["ing", "bryn", "mawr", "college", "news"] # additional words for the stop words list
stop_words.update(new_stop_words) # add the custom words to stop words list

directory = "issues" # filepath for the folder containing each issue
filenames = os.listdir(directory) # get all of the names of files in the given directory
decades = ["1910s", "1920s", "1930s", "1940s", "1950s", "1960s"] # list of decades
decades_files = {} # dictionary of decades to files for that decade

for dec in decades: # for each decade: 
    decades_files[dec] = [] # make an empty list corresponding to that decade

for file in filenames: # for every file in our list of file names
    decade = file[2:5] + "0s" # get the decade from the file name and reformat it
    path = "issues/" + file # add the directory to the file path
    decades_files[decade].append(path) # add the file path to the list for the corresponding decade

# add all of the text for each decade to a string
for decade in decades_files.keys(): # for each decade 1910s-1960s:
    total_text = "" # set an empty string
    for name in decades_files[decade]: # for each file in the dictionary for that decade
        f = open(name) # open the file
        text = f.read() # read the text
        total_text += text.lower() # make the text all lowercase + add to the total_text
        f.close() # close the file

    # generate and display the word cloud
    wordcloud = WordCloud(max_words=50, min_word_length=3, stopwords=stop_words).generate(total_text)
    plt.figure() # create a figure
    plt.imshow(wordcloud, interpolation="bilinear") # display the wordcloud as an image
    plt.axis("off") # turn off axis labels & lines
    plt.title(decade) # add a title based on which decade is being displayed
    plt.show() # displays open figures
