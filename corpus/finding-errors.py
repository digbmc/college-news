"""
Preliminary cleaning:
- Line filter (at least 2 consecutive letter characters)
- Get rid of hyphens
- Basic nltk lemmas and stems
- Identifies words not in nltk corpus words

"""



import nltk
from nltk.stem.porter import *
import re

porter_stemmer = PorterStemmer()
wordnet_lemmatizer = nltk.WordNetLemmatizer()
 	
def unusual_words(text):
    text_vocab = set(w.lower() for w in text if w.isalpha())
    english_vocab = set(w.lower() for w in nltk.corpus.words.words())
    unusual = text_vocab - english_vocab
    return sorted(unusual)


infile = '1940s-short.txt'
with open(infile, 'r', encoding='utf-8') as f:
    text = f.read()

nohyphens = re.sub('\w(-\n)', '', text)


tokens = nltk.word_tokenize(nohyphens)

word = re.compile(r'[a-zA-Z]{2}')

endhyphen = re.compile(r'[a-zA-Z]+.*-\s*$')
# maybe remove period?


# Determining if there are other syllable hyphens
# across lines: need to get better regex

lines = nohyphens.split('\n')
linesclean=[]
for l in lines:
    if word.search(l):
        linesclean.append(l)
for c in linesclean:
    if endhyphen.search(c):
        print(c)
        i = linesclean.index(c)
        print(linesclean[i+1])



cleanTokens = []
for t in tokens:
    if word.search(t):
        cleanTokens.append(t.lower())
# problem: isalpha gets rid of hyphenated words - use word search instead
# len(set(cleanTokens)) is 64082

lemmatized = []
for t in cleanTokens:
    lemmatized.append(wordnet_lemmatizer.lemmatize(t))

# len(set(lemmatized)) is 60309

stemmed = []
for t in lemmatized:
    t_stemmed = porter_stemmer.stem(t)
    stemmed.append(t_stemmed)

# len(set(stemmed)) is 49959

unusual = unusual_words(stemmed)
# 27813 unusual words

#outfile = 'weird_words_1940s.txt'

# with open(outfile, 'w', encoding='utf-8') as f:
#     for item in unusual:
#         f.write(item)
#         f.write('\n')



# stemmed = [porter_stemmer.stem(t) for t in lemmatized]
