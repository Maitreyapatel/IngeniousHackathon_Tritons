from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
#from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import pickle

input_data = [
    'There is a house made of steel rods and cement across the road.',
    'I am wearing a beautiful dress made of cotton.',
    'Information technology is at its peak and I need consultancy for the same.',
    'The soil is dry and crops are cultivated and fertilizers are sprayed.'
]

count_vectorizer = CountVectorizer()
train_tc = count_vectorizer.fit_transform(training_data)
classifier = pickle.load(open("save_output.pkl","rb"))
# count_vectorizer = pickle.load(open("save_vectorizer.pkl","rb"))
tfidf = pickle.load(open("save_tfidf.pkl","rb"))
# Build a count vectorizer for test data
input_tc = count_vectoriz.transform(input_data)
# Create Term Frequency - Inverse Document Frequency (tf-idf) transformer for test data
input_tfidf = tfidf.transform(input_tc)
# Predict the categories
predictions = classifier.predict(input_tfidf)
print(predictions[0])
