# Now we want to Identify underlying themes
# Typical ML Workflow:
# 1. Pick your problem: Identify which type of problem we need to solve
# 2. Represent Data: Represent data using numeric attributes called features
# 3. Apply an Algorithm: Use a standard algorithm to find a model

# Pick your Problem:
# We are given a large group of articles, so we divide the articles in to groups
# based on same common attributes. This is a classic example of clustering.

# Clustering: Group items together based on some measure of similarity
# Items in a group must be "similar" to one another -> Maximize intracluster similarity
# Items in different groups must be "dissimilar" to one another. -> Minimize intracluster similarity

# Represent Data:
# Using meaningful numeric attributes (features) through the process of extracting
# numeric attributes from text (feature extraction).
# For instance there are 2 methods for feature extraction
# 1. Term Frequency:
# 2. TF-IDF:

# We can create a list representing the universe of all words that can appear in any text
# (w1, w2, w3, w4, ...., wN) -> N is number of such words each representing one word
# Any text can be represented (as tuple) using the frequencies of these words.
# Hello this is a test -> (Hello, this, is, the, universe, of, all, words, in, any, ...)
# (1,1,1,0,0,0,0,....,1,0,....) -> Term Frequency Represntation
# Information on the order of words is lost. It treats each text as "Bag of words" -> Bag of words model
# Some words characterize a document more than others. "The house was in Newyork" -> 'house', 'Newyork'
# Words which occure more rarely, clth early differentiate a document from other documents
# Words which are very common don't do much to differentiate a document.

# Term Frequency - Inverse Document Frequency
# Weight the term frequencies to take the rarity of a word in to account
# weight = 1/#(num) of documents the word appears in
# So we multiply TF in IDF which is this method calls TF-IDF

# Apply an algorithm
# k-means clustering (very common)
# Documents are represented using TF-IDF, each document is a tuple of N numbers.
# N is the total number of distinct words in all documents.
# Each Document <-> A tuple of N numbers <-> A point in N-Dimensional Hypercube

# N-Dimensional Hypercube
# A line: a one-Dimensional shape: Origin--------------------X----------->
# Any point on the line can be represented in one number which is the distance of that point from Origin
# A square is a 2-Dimensional shape: Any point in a square can be represented using 2 numbers: (x,y)
# A cube is a 3-Dimensional shape: any point can be represented with 3 numbers: (x,y,z)
# A N-Dimensional Hypercube: A set of N numbers represent a point in N-Dimensional Hypercube which
# N numbers are the coordinates in that space.
# Each Document <-> A tuple of N numbers <-> A point in N-Dimensional Hypercube
# we can measure the distance between 2 points.

# points within a cluster -> Minimize distance
# points in different clusters -> Maximize distance
# This is what exactly k-means clustering algorithm does
# 1. Initialize a set of points as the 'K' Means: (Centroid (or mean) of the clusters you want to find.)
# (How many clusters we want to divide into?)
# The algorithm starts with Initialize with set of points eaach point as k-meanns centroids
# 2. Assign each point to the cluster belonging to the nearest mean.
# 3. Find the new means/centroids of the clusters.
# once again we repeat steps 2 and 3 and recompute the values of centroids.
# Rinse and repeat steps 2,3 until the means don't change anymore -> convergance
# Sometimes we cannot reach convergence so we set a max number of iterations that k clustering algorithm
# wants to try. At the end we have set of groups which all articles are divided. 
