# Cluster articles into groups representing different themes
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

from bs4 import BeautifulSoup

# Download all the urls each url will have 7 blog posts
def getAllDoxyDonkeyPosts(url,links):
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    soup = BeautifulSoup(response, features="lxml")
    # use a tag to find
    for a in soup.findAll('a'):
        try:
            url = a['href']
            title = a['title']
            # Find the link to the older posts and add it to the list
            if title == "Older Posts":
                print(title,url)
                links.append(url)
                # Find the next older posts link
                getAllDoxyDonkeyPosts(url,links)
        except:
            title = ""
    return

blogUrl = "http://doxydonkey.blogspot.com"
links = []
getAllDoxyDonkeyPosts(blogUrl,links)

# Once we got all the URLs we have to pass each article text to the URL
# We have to go to the browser and inspect the article text
# After we checked it we should find the classes which has div tag class 'post-body'

def getDoxyDonkeyText(testUrl):
    request = urllib2.Request(testUrl)
    response = urllib2.urlopen(request)
    soup = BeautifulSoup(response, features="lxml")
    # Find all posts within page
    myDivs = soup.findAll("div", {"class":'post-body'})
    posts = []
    for div in myDivs:
        posts += map(lambda p:p.text.encode('ascii',errors='replace').replace(b"?",b" "), div.findAll("li"))
        # div.findAll("li") :: find all articles within the post
    return posts

doxyDonkeyPosts = []
for link in links:
    doxyDonkeyPosts += getDoxyDonkeyText(link)

# So we set the articles and created a corpse of the Articles

# TfidVectorizer converts text to TF-IDF represntation
# Sklearn is a module with a lot of builtin pyhton functionality tasks fo ML
# which conrains feature_extraction module
from sklearn.feature_extraction.text import TfidfVectorizer

# we instantiate a vectorizer object which within a vectorizer we can specfy that
# we want to ignore stopwords by set its parameter to relevant language
vectorizer = TfidfVectorizer(max_df=0.5, min_df=2, stop_words='english')

# takes a list of strings and returens a 2-dimensional array inwhich each row
# represents 1 document. So if we try to print X, it is a matrix which has 2465
# rows each represents 1 article.
X = vectorizer.fit_transform(doxyDonkeyPosts)
print(X)

# the number of columns represents number of distinct words which are present in all articles
# we recall in TF-IDF representation each article is represented in n numbers and being total
# number of distinct words that can appear accross any text.
# each article is one row so x[0] is a tuple of 12428 numbers where each number represents TF*IDF
# of 1 word
print(X[0])
# it will print out the row: (0, 738)  0.0700267614388 .....
# TF-IDF numbers are the decimal number which all represent particular text of articles

# sk-learn also has a modulefor clustering calls in sklearn.cluster module
# It has a class for k-means clustering algorithm
# we import class and instantiate k-means object
from sklearn.cluster import KMeans

# n_cluster= number of clusters here we divide our article to 3 groups
# init specfies algorithm to help choose initial centroids such a way that find the relevant
# clusters with the minimum number of iterations. for other choices we should learn sklearn docs
# max_iter: maximum number of iterations (in case of no convergence)

km = KMeans(n_clusters = 3, init = 'k-means++', max_iter = 100, n_init = 1, verbose = True)
km.fit(X)
# after sum iterations there is convergence and clustering activity is complete

# each doc in our array X has now been assigned  to a number which represents the cluster which it belongs
# these numbers are stored in array as labels which is attributes of k-mean object
import numpy as np
# km.labels_: Array od cluster numbers assigned to each article
np.unique(km.labels_, return_counts=True)
# (array([0, 1, 2] -> distinct cluster numbers means every article assigned to one of these numbers
#  , dtype=int32), array([358, 1037, 1070]) -> how many articles is presented in each cluster means 0 has
# 358 number of articles in that cluster )

# Identify important keywords in each clusters
# we will setup dic text,  keys cluster numbers, values aggregated texts across all articles present
# in that cluster
text = {}
# we go to array of labels which have cluster numbers assigned to each document
# enumerate func converts array of labels to a list of tuples
for i,cluster in enumerate(km.labels_):
    # collect the text for each doc into corresponding cluster where the first element is the index of
    # an article, so using index we can get the corresponding article from the list of posts
    oneDocument = doxyDonkeyPosts[i]
    # then we aggregated this text for every article into the corresponding value in textDic
    if cluster not in text.keys():
        text[cluster] = oneDocument
    else:
        text[cluster] += oneDocument

# now we have complete text of each cluster in one place, we can use some nltk funcs to find out the
# most frequent words wihtin each cluster
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from collections import defaultdict
from string import punctuation
from heapq import nlargest
import nltk
# when we find MFW we don't want to include stopwords
# so we will setup a variable to represent stopwords that we want to ignore + some irrelevent words
_stopwords = set(stopwords.words('english') + list(punctuation) + ["million", "billion", "year", "millions", "billions", "y/y", "'s'", "''"])

keywords = {}
counts = {}
# this code will take text from each cluster and findout top 100 words that occur within that text
# we iterate through each cluster
for cluster in range(3):
    # we take corresponding text and tokenize it to words
    word_sent = word_tokenize(text[cluster].decode('utf-8').lower())
    # we filter out all the stopwords and keep only relevant words
    word_sent = [word for word in word_sent if word not in _stopwords]
    # compute frequency distribution of the words
    freq = FreqDist(word_sent)
    # pick top 100 words from distribution
    keywords[cluster] = nlargest(100, freq, key=freq.get)
    # we will store complete set of word distribution which will keep words along their counts in dictionary

unique_keys = {}
for cluster in range(3):
    # top keywords unique to each cluster
    other_clusters = list(set(range(3))-set([cluster]))
    # as we iterate and find list of other clusters and collect all keywords present in other clusters
    keys_other_clusters = set(keywords[other_clusters[0]]).union(set(keywords[other_clusters[1]]))
    # rm those kys from list of keywords in our cluster
    unique = set(keywords[cluster])-keys_other_clusters
    # pick 10 top
    unique_keys[cluster]=nlargest(10, unique, key=counts[cluster].get)


# Assign themes to new Articles
# Typical classification setup
# Problem statement: Define the problem statement
# Features: represent the training data and test data using numerical attributes
# Training: "Train a model" using training data
# Test: "Test a model" using test data

# Problem statement: article(Problem instance) -> classifier -> one of three themes we classified (label)
# classifier is like a blackbox
# ML Objective: Build this blackbox
# Use TF-IDF representation for historical data
# There are several standard algorithms: k-nearest algorithm
# From the clustering step we have articles grouped in different themes
# A new article to be classified (tuple of n numbers)
# find k "nearest" Neighbors, Take a majority vote ( which cluster majority nearest neighbors belong to)

# we can select an article from doxydonkey

article = "Facebook Inc. has been giving advertisers an inflated metric for the average time users spent watching a video, a measurement that may have helped boost marketer spending on one of Facebook’s most popular ad products. The company, owner of the world’s largest social network, only counts a video as viewed if it has been seen for more than 3 seconds. The metric it gave advertisers for their average video view time incorporated only the people who had watched the video long enough to count as a view in the first place, inflating the metric because it didn’t count anyone who didn’t watch, or watched for a shorter time. Facebook’s stock fell more than 1.5 percent in extended trading after the miscalculation was earlier reported in the Wall Street Journal. Facebook had disclosed the mistake in a posting on its advertiser help center web page several weeks ago. Big advertising buyers and marketers are upset about the inflated metric, and asked the company for more details, according to the report in the Journal, citing unidentified people familiar with the situation. The Menlo Park, California-based company has kept revenue surging in part because of enthusiasm for its video ads, which advertisers compare in performance to those on Twitter, YouTube and around the web.\""

# K-Nearest Neighbors Classifier
from sklearn.neighbors import KNeighborsClassifier
classifier = KNeighborsClassifier() # (n_neighbors = 10)
# Training Phase: use fit method to setup training phase, a complete set of articles where labels already
# known. X has articles as TF-IDF tuples. km_labels_ as array cluster numbers assigned to those Articles
classifier.fit(X,km.labels_)
# Out// KNeighborsClassifier(algorithm='auto', leaf_size = 30, metric = 'minkowski', metric_params
# =None, n_jobs=1, n_neighbors(bydefault)=5, p=2, weights='uniform')
# after TS, classifier is ready to be given any new instance

# represent the test article as TF-IDF
test = vectorizer.transform([article.decode('utf-8').encode('ascii', errors='ignore')])
# <1x12428 sparse matrix of type '<type 'numpy.float 64'>' with 85 stored elements in compressed Sparse row format

classifier.predict(test)
# array([0], dtype = int32)
