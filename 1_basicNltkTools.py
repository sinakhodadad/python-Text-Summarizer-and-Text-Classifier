import nltk

# Tokenization
from nltk.tokenize import word_tokenize, sent_tokenize
text = "Mary had a little lamb. Her fleece was white as snow"
sents = sent_tokenize(text)
print (sents)
words = [word_tokenize(sent) for sent in sents]
print (words)

#Stopwords Removal
from nltk.corpus import stopwords
from string import punctuation
customStopWords = set(stopwords('english')+list(punctuation))
wordsNotStopWords = [for word in word_tokenize(text) if word not in customStopWords]
print(customStopWords)

#N_Grams
from nltk.collocations import *
bigramMeasures = nltk.collocations.BigramAssocMeasures()
finder = BigramCollocationFinder.from_words(wordsNotStopWords)
print(sorted(finder.ngram_fd.items()))

#Stemming
text2 = "Mary closed on closing night when she was in the mood to close"
from nltk.stem.lancaster import LancasterStemmer
st = LancasterStemmer()
stemmedWords = [st.stem(word) for word in word_tokenize(text2)]
stemmedNotStopWords = [word for word in word_tokenize(text2) if word not in customStopWords]
print(stemmedWords)
print(stemmedWords)
nltk.pos_tag(word_tokenize(text2))
#print(nltk.pos_tag(word_tokenize(text2))) it has error also search for acronyms abbreviation in nltk docs

#Disambiguating Word Meanings
text3 = "Sing in a lower tone, along with the bass."
text4 = "This sea bass was really hard to catch."
from nltk.corpus import wordnet as wn #wordnet is a lexicon (a little like a thesaurus)
for ss in wn.synsets('bass'): #sysnset represents one single definition of the word
    print(ss,ss.definition())
from nltk.wsd import lesk #an algorithm for word sense Disambiguating
sense1 = lesk(word_tokenize(text3,'bass')) #one singleton
print(sense1, sense1.difinition())
sense2 = lesk(word_tokenize(text4,'bass')) #one singleton
print(sense2, sense2.difinition())

#Contrasting Rule Based and Machine Learning Approach
#NLP Application: Spam detection. Emails->Static Rules(Contain specific words)->Spam/Ham
