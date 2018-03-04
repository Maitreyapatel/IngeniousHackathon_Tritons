from django.shortcuts import render
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
#from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import pickle
# Create your views here.
def index(request):
    return render(request,'index.html')

def app(request):
    # Load self-built dataset as dataframe object
    training_data = pd.read_csv('Dataset.csv')
    # Extract values of Y
    train_target = training_data.iloc[:,0]
    # Extract values of X
    training_data = training_data.iloc[:, 1]
    # Convert dataframe object X into numpy array
    training_data = training_data.values
    # Build a count vectorizer and extract unique word counts from all instances
    count_vectorizer = CountVectorizer()
    train_tc = count_vectorizer.fit_transform(training_data)
    print("\nDimensions of training data:", train_tc.shape)

    # Create Term Frequency - Inverse Document Frequency (tf-idf) transformer
    tfidf = TfidfTransformer()
    train_tfidf = tfidf.fit_transform(train_tc)

    classifier = MultinomialNB().fit(train_tfidf, train_target)



    if request.method == 'POST':
        #code here
        data = request.POST["desc"]
        input_data = [data]



        # classifier = pickle.load(open("save_output.pkl","rb"))
        # count_vectorizer = pickle.load(open("save_vectorizer.pkl","rb"))
        # tfidf = pickle.load(open("save_tfidf.pkl","rb"))
        # Build a count vectorizer for test data
        input_tc = count_vectorizer.transform(input_data)
        # Create Term Frequency - Inverse Document Frequency (tf-idf) transformer for test data
        input_tfidf = tfidf.transform(input_tc)
        # Predict the categories
        predictions = classifier.predict(input_tfidf)
        return render(request,'result.html',{ "val":predictions[0] })
    return render(request,'app.html')
