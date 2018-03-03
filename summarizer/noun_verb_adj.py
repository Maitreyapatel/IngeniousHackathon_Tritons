from collections import Counter
import nltk


def allCounter(document):
    tokens = nltk.word_tokenize(document.lower())
    document = nltk.Text(tokens)
    tags = nltk.pos_tag(document)
    return (Counter(tag for word,tag in tags))
    

