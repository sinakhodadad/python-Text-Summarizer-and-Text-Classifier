try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

from bs4 import BeautifulSoup

def getTextWaPo(url):
    page = urllib2.urlopen(url).read().decode('utf8')
    soup = BeautifulSoup(page, "lxml")
    text = ' '.join(map(lambda p: p.text, soup.find_all('article')))
    return text.encode('ascii', errors='replace').replace(b"?",b" ")

articleURL = "https://www.washingtonpost.com/world/national-security/saudi-crown-prince-exchanged-messages-with-aide-alleged-to-have-overseen-khashoggi-killing/2018/12/01/faa43758-f5c3-11e8-9240-e8028a62c722_story.html?utm_term=.8ae87556badc"
text = getTextWaPo(articleURL)
text = text.decode("utf-8")

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from string import punctuation

sents = sent_tokenize(text)
word_sent = word_tokenize(text.lower())
_stopWords = set(stopwords.words('english') + list(punctuation))
word_sent = [word for word in word_sent if word not in _stopWords]

# FreqDist is a table that has words in one column and the number of times each
# word occurs in the 2nd column. FreqDist constructs a frequency distribution of words

from nltk.probability import FreqDist
freq = FreqDist(word_sent)
# The result is the dictionary which keys are the words and the values are the frequencies
# The higher the frequency, the more important the word is considered

# Lets find most frequent word in the article and find out if they are relevent to the theme
# nlargest is a function and can sort any collection whether it is Dict or List
from heapq import nlargest
# It has three inputs the number of elements we want to pick,
# The collection that we want to be sorted which in this case is the freq distribution of words,
# A function used to sort the elements in the collection
# This function find the corresponding value in Dict freq for a given key
# Values represent columns given a word will give us the column for specific words
nlargest(10, freq, key=freq.get)
# It will give us words such as space, telescope, etc. which are words related to the theme
# Now we have words and their corresponding frequencies
from collections import defaultdict
# we will create a dictionary which keys are the Sentences and
# Values are the Significance Scores we use defaultdict
# its difference is that if you try to look up a key which is not present in dictionary
# it will simply add new key in your dictionary
ranking = defaultdict(int)
# we will iterate through each sentence which is present in the list of Sentences
# enumarate function will take a list and return a list of tuples inwhich the first element
# of tuple is the index of the list element. so each time our loop is running i represents
# the index of the sentence we are currently looking at. enumarate converts [a,b,c] to
# [(0,a),(1,b),(2,c)]. Given each sentence, we first split it into list of words which are
# present in the sentence. and then use frequency distribution dictionary to lookup the importance
# of each word. we iterate through each word which is present in the sentence and add its frequency
# to the Significance score of the sentence and store this in the ranking dictionary.
for i,sent in enumerate(sents):
    for w in word_tokenize(sent.lower()):
        if w in freq:
            ranking[i]+=freq[w]

# ranking
# ranking dictionary which keys are the indexes of the different sentences in our article
# and the values are the significance scores which are sum of importance of all words in sentence

sents_idx = nlargest(4, ranking, key=ranking.get)
# sents_idx -> [27,6,17,19]
# for summary we put indexes in order
[sents[j] for j in sorted(sents_idx)]

# Encapsulate all the logic in function
def summarize(text, n):
    sents = sent_tokenize(text)
    # check whether the text has the required sentences
    assert n <= len(sents)
    word_sent = word_tokenize(text.lower())
    _stopwords = set(stopwords.words('english')+list(punctuation))
    word_sent = [word for word in word_sent if word not in _stopwords]
    freq = FreqDist(word_sent)
    ranking = defaultdict(int)
    for i,sent in enumerate(sents):
        for w in word_tokenize(sent.lower()):
            if w in freq:
                ranking[i] += freq[w]
    sents_idx = nlargest(n, ranking, key=ranking.get)
    return [sents[j] for j in sorted (sents_idx)]

print(summarize (text, 3))
# Not all tasks will be solved with rule based module. We need a machine learning approach
# to classify text
