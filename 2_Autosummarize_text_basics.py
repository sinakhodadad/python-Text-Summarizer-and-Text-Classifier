try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

from bs4 import BeautifulSoup

articleURL = "https://www.washingtonpost.com/world/national-security/saudi-crown-prince-exchanged-messages-with-aide-alleged-to-have-overseen-khashoggi-killing/2018/12/01/faa43758-f5c3-11e8-9240-e8028a62c722_story.html?utm_term=.8ae87556badc"

page = urllib2.urlopen(articleURL).read().decode('utf','ignore')
soup = BeautifulSoup(page, "lxml")

# print(soup.find('article'))
# soup.find('article').text

#page might have multiple articles, we have to collect all of them
#soup.find will give only the first article so we have to use find_all
#find_all will give us a list of all elements which have the tag of article
#we can combine text from all of them to a single string
text = ' '.join(map(lambda p: p.text, soup.find_all('article')))
#text

#some special chars such as \x0 or \u201
#there are different paradigms such as unicode and ascii
#remove special chars
text.encode('ascii', errors='replace').replace("?"," ")
#now we have clean piece of text

#Encapsulate all the logic in the one function
#Encapsulating all the parsing logic
def getTextWaPo(url):
    page = urllib2.urlopen(url).read().decode('utf8')
    soup = BeautifulSoup(page, "lxml")
    text = ' '.join(map(lambda p: p.text, soup.find_all('article')))
    return text.encode('ascii', errors='replace').replace("?"," ")
