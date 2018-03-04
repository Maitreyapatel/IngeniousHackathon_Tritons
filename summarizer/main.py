from __future__ import division
from similarity_try3 import *
from review_processer import *
from textblob import TextBlob as tb
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import csv
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from autocorrect import spell
from noun_verb_adj_try1 import *
import requests
from bs4 import BeautifulSoup
import io
import codecs
from afinn import Afinn
from math import log, exp
from operator import mul
from collections import Counter
import os
import pylab
import pickle as cPickle



'''
sentiment analysis start
'''


class MyDict(dict):
    def __getitem__(self, key):
        if key in self:
            return self.get(key)
        return 0

pos = MyDict()
neg = MyDict()
features = set()
totals = [0, 0]
delchars = ''.join(c for c in map(chr, range(128)) if not c.isalnum())

CDATA_FILE = "countdata.pickle"
FDATA_FILE = "reduceddata.pickle"


def negate_sequence(text):
    """
    Detects negations and transforms negated words into "not_" form.
    """
    negation = False
    delims = "?.,!:;"
    result = []
    words = text.split()
    prev = None
    pprev = None
    for word in words:
        # stripped = word.strip(delchars)
        stripped = word.strip(delims).lower()
        negated = "not_" + stripped if negation else stripped
        result.append(negated)
        if prev:
            bigram = prev + " " + negated
            result.append(bigram)
            if pprev:
                trigram = pprev + " " + bigram
                result.append(trigram)
            pprev = prev
        prev = negated

        if any(neg in word for neg in ["not", "n't", "no"]):
            negation = not negation

        if any(c in word for c in delims):
            negation = False

    return result


def train():
    global pos, neg, totals
    retrain = False
    
    # Load counts if they already exist.
    if not retrain and os.path.isfile(CDATA_FILE):
        pos, neg, totals = cPickle.load(open(CDATA_FILE,'rb'))
        return

    limit = 12500
    for file in os.listdir("./aclImdb/train/pos")[:limit]:
        for word in set(negate_sequence(open("./aclImdb/train/pos/" + file).read())):
            pos[word] += 1
            neg['not_' + word] += 1
    for file in os.listdir("./aclImdb/train/neg")[:limit]:
        for word in set(negate_sequence(open("./aclImdb/train/neg/" + file).read())):
            neg[word] += 1
            pos['not_' + word] += 1
    
    prune_features()

    totals[0] = sum(pos.values())
    totals[1] = sum(neg.values())
    
    countdata = (pos, neg, totals)
    cPickle.dump(countdata, open(CDATA_FILE, 'wb'))

def classify(text):
    words = set(word for word in negate_sequence(text) if word in features)
    if (len(words) == 0): return True
    # Probability that word occurs in pos documents
    pos_prob = sum(log((pos[word] + 1) / (2 * totals[0])) for word in words)
    neg_prob = sum(log((neg[word] + 1) / (2 * totals[1])) for word in words)
    return pos_prob > neg_prob

def classify2(text):
    """
    For classification from pretrained data
    """
    words = set(word for word in negate_sequence(text) if word in pos or word in neg)
    if (len(words) == 0): return True
    # Probability that word occurs in pos documents
    pos_prob = sum(log((pos[word] + 1) / (2 * totals[0])) for word in words)
    neg_prob = sum(log((neg[word] + 1) / (2 * totals[1])) for word in words)
    return pos_prob > neg_prob

def classify_demo(text):
    words = set(word for word in negate_sequence(text) if word in pos or word in neg)
    if (len(words) == 0): 
        #print ("No features to compare on")
        return True

    pprob, nprob = 0, 0
    for word in words:
        pp = log((pos[word] + 1) / (2 * totals[0]))
        np = log((neg[word] + 1) / (2 * totals[1]))
        #print ("%15s %.9f %.9f" % (word, exp(pp), exp(np)))
        pprob += pp
        nprob += np
    if pprob>nprob:
        return True
    else:
        return False


def MI(word):
    """
    Compute the weighted mutual information of a term.
    """
    T = totals[0] + totals[1]
    W = pos[word] + neg[word]
    I = 0
    if W==0:
        return 0
    if neg[word] > 0:
        # doesn't occur in -ve
        I += (totals[1] - neg[word]) / T * log ((totals[1] - neg[word]) * T / (T - W) / totals[1])
        # occurs in -ve
        I += neg[word] / T * log (neg[word] * T / W / totals[1])
    if pos[word] > 0:
        # doesn't occur in +ve
        I += (totals[0] - pos[word]) / T * log ((totals[0] - pos[word]) * T / (T - W) / totals[0])
        # occurs in +ve
        I += pos[word] / T * log (pos[word] * T / W / totals[0])
    return I

def get_relevant_features():
    pos_dump = MyDict({k: pos[k] for k in pos if k in features})
    neg_dump = MyDict({k: neg[k] for k in neg if k in features})
    totals_dump = [sum(pos_dump.values()), sum(neg_dump.values())]
    return (pos_dump, neg_dump, totals_dump)

def prune_features():
    """
    Remove features that appear only once.
    """
    global pos, neg
    for k in list(pos):
        if pos[k] <= 1 and neg[k] <= 1:
            del pos[k]

    for k in list(neg):
        if neg[k] <= 1 and pos[k] <= 1:
            del neg[k]

def feature_selection_trials():
    """
    Select top k features. Vary k and plot data
    """
    global pos, neg, totals, features
    retrain = True

    if os.path.isfile(FDATA_FILE):
        pos, neg, totals = cPickle.load(open(FDATA_FILE,'rb'))
        return

    words = list(set(list(pos) + list(neg)))
    print ("Total no of features:", len(words))
    words.sort(key=lambda w: -MI(w))
    num_features, accuracy = [], []
    bestk = 0
    limit = 500
    path = "./aclImdb/test/"
    step = 500
    start = 20000
    best_accuracy = 0.0
    for w in words[:start]:
        features.add(w)
    for k in range(start, 40000, step):
        for w in words[k:k+step]:
            features.add(w)
        correct = 0
        size = 0

        for file in os.listdir(path + "pos")[:limit]:
            correct += classify(open(path + "pos/" + file).read()) == True
            size += 1

        for file in os.listdir(path + "neg")[:limit]:
            correct += classify(open(path + "neg/" + file).read()) == False
            size += 1

        num_features.append(k+step)
        accuracy.append(correct / size)
        if (correct / size) > best_accuracy:
            bestk = k
        print (k+step, correct / size)

    features = set(words[:bestk])
    cPickle.dump(get_relevant_features(), open(FDATA_FILE, 'wb'))

    #pylab.plot(num_features, accuracy)
    #pylab.show()

def test_pang_lee():
    """
    Tests the Pang Lee dataset
    """
    total, correct = 0, 0
    for fname in os.listdir("txt_sentoken/pos"):
        correct += int(classify2(open("txt_sentoken/pos/" + fname).read()) == True)
        total += 1
    for fname in os.listdir("txt_sentoken/neg"):
        correct += int(classify2(open("txt_sentoken/neg/" + fname).read()) == False)
        total += 1
    print ("accuracy: %f" % (correct / total))


train()
feature_selection_trials()
# test_pang_lee()
#classify_demo("I love this product.")
# classify_demo(open("neg_example").read())

'''
Sentiment analysis over
'''



url=input("Enter amazon.com product url:")

good=0
bad=0
average=0
counting=0

def reviews(file,url):
    txt=""
    murl="http://www.amazon.com"
    headers = requests.utils.default_headers()
    headers.update({'User-Agent': 'Mozilla/5.0 (X11; Mint; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/51.0',})
    r=requests.get(url, headers=headers)
    soup=BeautifulSoup(r.content,"html.parser")
    print(soup)
    url=soup.find('a', {'id':'dp-summary-see-all-reviews'})['href']
    afinn = Afinn()
    url=str(murl+url)
    r=requests.get(url, headers=headers)
    soup=BeautifulSoup(r.content,"html.parser")
    link=soup.find('li',{'class':'a-last'})
    print(link)
    link=link.find('a')['href']
    url=str(murl+link[0:-31])
    print("Scrapping....!!")
    for i in range(11):
        url_main=url+str(i+1)
        r=requests.get(url_main, headers=headers)
        #print("Hello")
        soup=BeautifulSoup(r.content,"html.parser")
        g_data = soup.find_all("div",{"class":"a-section review"})
        #print(g_data)
        global counting
        global average
        global good
        global bad
        #g_data = soup.find_all("div",{"class":"a-row review-data"})
        for item in g_data:
            counting=counting+1
            review=item.find_all("div",{"class":"a-row review-data"})[0].text
            #print(review)
            txt = txt + review
            rate=item.find_all("span",{"class":"a-icon-alt"})[0].text
            rating=int(rate[0])            
            #print(rating)
            pol_blob = round(tb(review).sentiment.polarity, 3)
            
            if rating == 5 and pol_blob > 0.1:
                good=good+1
            elif rating == 4 and pol_blob > 0.45:
                good=good+1
            elif rating == 4 and pol_blob > 0.2:
                pol_afin = afinn.score(review)
                if pol_afin >= 4:
                    good=good+1
                else :
                    average=average+1
            elif rating == 3 and pol_blob > 0.7:
                good=good+1
            elif rating == 3 and pol_blob < 0:
                bad=bad+1
            elif rating == 2 and pol_blob < 0:
                bad=bad+1
            elif rating == 2 and pol_blob <= 0.175:
                pol_afin = afinn.score(review)
                if pol_afin < 0:
                    bad=bad+1
                else:
                    average=average+1
            elif rating == 1 and pol_blob < 0:
                bad=bad+1
            elif rating == 1 and pol_blob <= 0.2:
                pol_afin = afinn.score(review)
                if pol_afin < 0:
                    bad=bad+1
                else:
                    average=average+1
            else:
                average=average+1

    
    with codecs.open(file,'w', encoding='utf-8') as document:
        document.write(txt)


class Queue(object):
    def __init__(self, queue=None):
        if queue is None:
            self.queue = []
        else:
            self.queue = list(queue)
    def dequeue(self):
        return self.queue.pop(0)
    def enqueue(self, element):
        self.queue.append(element)



def importance(sen1,sen2):
	c1=allCounter(str(sen1))
	c2=allCounter(str(sen2))
	
	d1=0
	d2=0
		
	array=['JJ','JJR','JJS','VB','VBD','VBG','VBN','VBP','VBZ']
	for ar in array:
		d1=d1+c1[ar]
		d2=d2+c2[ar]
	
	if d1>d2:
		return True
	else:
		return False

def isHindi(sen):
	
	c=allCounter(str(sen))
	d=0
	array=['NN','NNS','NNP','NNPS']
	for ar in array:
		d=d+c[ar]
	if d > len(sen.words)/2:
		return True
	else:
		return False



reviews('review.txt',url)

count_vectorizer = CountVectorizer()
tfidf = TfidfTransformer()

def posneg(sen):
    
    #print("IN POSNEG")
    
    re=[]
    words=sen.words
    sentence=""
    for i in range(len(words)):
        sentence+=spell(words[i])
        if i+1!=len(words):
            sentence+=" "
        else:
            sentence+="."
    answer=posnegfinal(sentence)
    if answer[0] == '0':
        return False
    if answer[0] == '1':
        return True
    print("Return fail:)")


poss = Queue()
negs = Queue()
temp = Queue()



filepath = 'review.txt' 
with io.open(filepath, mode='r',encoding='utf-8') as myfile:
    document1=myfile.read()
    document2=u''
    char=""
    for character in document1:
        ordchar = ord(character)
        if character is '.' and char is '.':
            document2+=''
        if ordchar <= 0xFFFF:
            if character is '0' or character is '1' or character is '2' or character is '3' or character is '4' or character is '5' or character is '6' or character is '7' or character is '8' or character is '9':
                document2+=" � "
            else:
                document2+=character
        else:
            document2+=''
        if character is '.' and char is not '.':
            document2+=' '
        char=character

final1=tb(document2)
count = 0
countp = 0
countn = 0
counts = len(final1.sentences)
print("Summarizing..!!!")

for sentence in final1.sentences:
    check = sentence.words
    flag = False
	
    if len(check) <= 5 :
        continue
	
	
	
    for word in check:
        if word == '�':
            flag = True
            break
        for wordc in wordsForDelete:
            if word.lower() == wordc.lower():
                flag = True
    if flag == True:
        continue
    if isHindi(sentence) == True:
        continue
		
    if count is 0:
        temp.enqueue(sentence)
        count=count+1
    else:
        for i in range(count):
            sen=temp.dequeue()
            if checkSimilarity(sen,sentence) > 0.5:
                if importance(sen,sentence) == False:
                    sen=sentence
                temp.enqueue(sen)
                flag=False
                break
            else:
                temp.enqueue(sen)
                flag=True


        if flag:
            temp.enqueue(sentence)
            count=count+1
    

sentences=[]
   
for i in range(count):
    sen = temp.dequeue()
    sentences.append(str(sen))
    result=classify_demo(str(sen))
    #print(result)
    if result == True:
        poss.enqueue(sen)
        countp=countp+1
    elif result == False:
        negs.enqueue(sen)
        countn=countn+1


print("Positive:")
for i in range(countp):
    sen=poss.dequeue()
    print("sentence=",sen)

print("Negative:")
for i in range(countn):
    sen=negs.dequeue()
    print("sentence=",sen)


good=(good*100)/counting
bad=(bad*100)/counting
average=(average*100)/counting

print("Good:",good)
print("Bad:",bad)
print("Average:",average)
print("Total reviews scaned:",counting)
print("Total sentnces of all reviews:",counts)
print("Total sentences in summary:",count)
'''

summary={
    'sentence':sentences,
    'good':good,
    'bad':bad,
    'average':average,
    'counting':counting   
}

result=json.dumps(summary)
'''
