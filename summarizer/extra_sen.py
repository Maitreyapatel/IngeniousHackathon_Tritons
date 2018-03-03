import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pickle
import csv
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

def create_word_features(words):
    useful_words = [word for word in words if word not in stopwords.words("english")]
    my_dict = dict([(word, True) for word in useful_words])
    return my_dict
'''
neg_reviews = []
for fileid in movie_reviews.fileids('neg'):
    words = movie_reviews.words(fileid)
    neg_reviews.append((create_word_features(words),"negative"))

pos_reviews = []
for fileid in movie_reviews.fileids('pos'):
    words = movie_reviews.words(fileid)
    pos_reviews.append((create_word_features(words), "positive"))

train_set = neg_reviews[:750] + pos_reviews[:750]
test_set =  neg_reviews[750:] + pos_reviews[750:]

classifier = NaiveBayesClassifier.train(train_set)
'''
'''
inputfile = 'amazon_cells_labelled.txt'
data = np.loadtxt(inputfile,delimiter=';', usecols=range(2))
X ,y = data[:,:-1], data[:,-1]
'''
data=[]
X=[]
y=[]
tfidf = TfidfTransformer()
#vect = TfidfVectorizer()
#print("Now game is start..!")
with open('allreviews.txt') as f:
   for l in f:
       data=l.strip().split(";")
       X.append(data[0])
       #print(X)
       y.append(data[1])
count_vectorizer = CountVectorizer()
X1=X
X1=count_vectorizer.fit_transform(X)
#print("\nDimensions of training data:",X1.shape)
#print(X1[0])
Xt=tfidf.fit_transform(X1)
#print(Xt)
#print("Transformation is done..!!")
classifier = RandomForestClassifier()

classifier.fit(Xt,y)

#print("Training is over...!!")
'''
accuracy = nltk.classify.util.accuracy(classifier, test_set)
print(accuracy * 100)
'''
with open('sentimenttry.pickle', 'wb') as handle:
    pickle.dump(classifier, handle, protocol=pickle.HIGHEST_PROTOCOL)

#print("File has been saved..!!")

def posnegfinal(sen):
    re=[]
    re.append(sen)
    rt=count_vectorizer.transform(re)
    rf=tfidf.transform(rt)
    return classifier.predict(rf)




'''
words = word_tokenize(review_spirit)
words = create_word_features(words)
print (classifier.classify(words))
'''

