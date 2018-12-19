# Classify texts base ontheir themes
# Feature extraction numeric models using the bag of words model
# Use K-means clustering to identify a set of topics

# k-means clustering aims to partition n observations into k clusters in which
# each observation belongs to the cluster with the nearest mean, serving as a
# prototype of the cluster.

# Using the K-Nearest Neighbors model for classifying text into topics

# In pattern recognition, the k-nearest neighbors algorithm (k-NN) is a non-parametric method
# used for classification and regression.[1] In both cases, the input consists of the k closest
# training examples in the feature space. The output depends on whether k-NN is used for classification
# or regression:
# In k-NN classification, the output is a class membership.
# An object is classified by a majority vote of its neighbors, with the object being assigned to the
# class most common among its k nearest neighbors (k is a positive integer, typically small).
# If k = 1, then the object is simply assigned to the class of that single nearest neighbor.
# In k-NN regression, the output is the property value for the object.
# This value is the average of the values of its k nearest neighbors.
# k-NN is a type of instance-based learning, or lazy learning, where the function is only approximated
# locally and all computation is deferred until classification. The k-NN algorithm is among the simplest
# of all machine learning algorithms.
# Both for classification and regression, a useful technique can be used to assign weight to the
# contributions of the neighbors, so that the nearer neighbors contribute more to the average than
# the more distant ones. For example, a common weighting scheme consists in giving each neighbor a weight
# of 1/d, where d is the distance to the neighbor.[2]
# The neighbors are taken from a set of objects for which the class (for k-NN classification) or the
# object property value (for k-NN regression) is known. This can be thought of as the training set
# for the algorithm, though no explicit training step is required.

# Classifying Articles
# Start with a corpus of articles. Identify underlying themes. Assign themes to the new article.
# Article100 -> Model -> theme

# Collect articles from a blog
# The page is sectiones to different pages each has 7 articles we can go forward or backward
# As usual
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
                print("Hi")
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
    mydivs = soup.findAll("div", {"class":'post-body'})

    posts = []
    for div in myDivs:
        posts += map(lambda p:p.text.encode('ascii',errors='replace').replace("?"," ")), div.findAll("li")
        # div.findAll("li") :: find all articles within the post
    return posts

doxyDonkeyPosts = []
for link in links:
    doxyDonkeyPosts += getDoxyDonkeyText(link)

# So we set the articles and created a corpse of the Articles
