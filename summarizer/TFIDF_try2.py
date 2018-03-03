import math
from textblob import TextBlob as tb
import io
import codecs
from similarity_try3 import *

def tf(word, blob):
    return blob.words.count(word) / len(blob.words)

def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob.words)

def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))

def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)


def TF(file):
    filepath = file
    with io.open(filepath, mode='r',encoding='utf-8') as myfile:
        document1=myfile.read() #.replace('\n', '')
        document2=u''
        char=""
        #print("hi")
        for character in document1:
            ordchar = ord(character)
            if character is '.' and char is '.':
                document2+=''
            if ordchar <= 0xFFFF:
                # debugging # print( 'U+%.4X' % ordchar, character)
                if character is '0' or character is '1' or character is '2' or character is '3' or character is '4' or character is '5' or character is '6' or character is '7' or character is '8' or character is '9':
                    document2+=' '
                    document2+='�'
                    document2+=' '
                    
                else:
                    document2+=character
            else:
                # debugging # print( 'U+%.6X' % ordchar, '�')
                ###         �=Replacement Character; codepoint=U+FFFD; utf8=0xEFBFBD
                document2+=''
            if character is '.' and char is not '.':
                #document2+='.'
                document2+=' '
            char=character
        final1=document2
        #print(document2)
    
    with io.open("reviews2.txt", mode='r',encoding='utf-8') as myfile:
        document1=myfile.read() #.replace('\n', '')
        document2=u''
        #print("hi")
        char=""
        for character in document1:
            ordchar = ord(character)
            if character is '.' and char is '.':
                document2+=''
            if ordchar <= 0xFFFF:
                # debugging # print( 'U+%.4X' % ordchar, character)
                if character is '0' or character is '1' or character is '2' or character is '3' or character is '4' or character is '5' or character is '6' or character is '7' or character is '8' or character is '9':
                    document2+=" � "
                else:
                    document2+=character
            else:
                # debugging # print( 'U+%.6X' % ordchar, '�')
                ###         �=Replacement Character; codepoint=U+FFFD; utf8=0xEFBFBD
                document2+=''
            if character is '.' and char is not '.':
                #document2+='.'
                document2+=' '
            char=character
        final2=document2
        #print(document2)

    with io.open("reviews3.txt", mode='r',encoding='utf-8') as myfile:
        document1=myfile.read() #.replace('\n', '')
        document2=u''
        #print("hi")
        char=""
        for character in document1:
            ordchar = ord(character)
            if character is '.' and char is '.':
                document2+=''
            if ordchar <= 0xFFFF:
                # debugging # print( 'U+%.4X' % ordchar, character)
                if character is '0' or character is '1' or character is '2' or character is '3' or character is '4' or character is '5' or character is '6' or character is '7' or character is '8' or character is '9':
                    document2+=" � "
                else:
                    document2+=character
            else:
                # debugging # print( 'U+%.6X' % ordchar, '�')
                ###         �=Replacement Character; codepoint=U+FFFD; utf8=0xEFBFBD
                document2+=''
            if character is '.' and char is not '.':
                #document2+='.'
                document2+=' '
            char=character
        final3=document2
        #print(document2)
    
    final1=tb(final1)
    final2=tb(final2)
    final3=tb(final3)
    
    bloblist = [final1, final2, final3]
    scores=[]
    blob=final1
    scores = {word: tfidf(word, blob, bloblist) for word in blob.words}

    return(scores)

#TF('reviews3.txt')






