from textblob import TextBlob
from random import randint
from PyDictionary import PyDictionary
import requests
from bs4 import BeautifulSoup
import io
from nltk.corpus import brown
import nltk

freqs=nltk.FreqDist(w.lower() for w in brown.words())

dictionary=PyDictionary()

def penn_to_wn(tag):
    if tag.startswith('N'):
        return 'n'
    if tag.startswith('V'):
        return 'v'
    if tag.startswith('J'):
        return 'a'
    if tag.startswith('R'):
        return 'r'
    return None



def tagged_to_synset(word,tag):
    wn_tag = penn_to_wn(tag)
    if wn_tag is None:
        return None

    try:
        return wn.synsets(word, wn_tag)[0]
    except:
        return None



def sentence_similarity(sentence1, sentence2):
    """ compute the sentence similarity using Wordnet """
    sentence1 = sentence1.tags
    sentence2 = sentence2.tags
    
    synsets1 = [tagged_to_synset(*tagged_word) for tagged_word in sentence1]
    synsets2 = [tagged_to_synset(*tagged_word) for tagged_word in sentence2]
    
    synsets1 = [ss for ss in synsets1 if ss]
    synsets2 = [ss for ss in synsets2 if ss]
    
    score, count = 0.0, 0
    
    for synset in synsets1:
        
        li=[synset.path_similarity(ss) for ss in synsets2]
        m=0
        for i in range(len(li)):
            if li[i] is not None and m<li[i]:
                m=li[i]
        if m != 0:
            score += m
            count += 1

    if count is 0:
        score = 0
    else:
        score /= count
    return score

def checkSimilarity(sentence,focus_sentence):
    a1=sentence_similarity(focus_sentence, sentence)
    a2=sentence_similarity( sentence,focus_sentence)

    return max(a1,a2)

def rewriter(sentence):
    sentence=TextBlob(sentence)
    sen=sentence.tags
    #print(sen)
    temp=sentence;
    q1=[]
    black_list=['is','are','be','b','–',"-","'","!","."]
    q2=[]
    words=sentence.words
    #print(sen)
    max=0
    for c in range(1):
        temp=""
        for i in range(len(words)):
            #print(words[i])
            if sen[i][0] not in black_list and (sen[i][1]=='VB' or sen[i][1]=='VBG' or sen[i][1]=='VBN' or sen[i][1]=='VBP'):
                print("sen:",sen[i][0])
                maxi=-1
                stri=""
                strm=""
                msen=""
                lists=list(dictionary.synonym(sen[i][0]))
                flag=True
                for syn in lists:
                    if i<len(words):
                        stri+=words[i-2]+" "+words[i-1]+" "+syn
                        strm+=words[i-2]+" "+words[i-1]+" "+sen[i][0]
                    elif i==1 and len(words)>=2:
                        stri+=words[i-1]+" "+syn+" "+words[i+1]
                        strm+=words[i-1]+" "+sen[i][0]+" "+words[i+1]
                    elif i==0 and len(words)>=2:
                        stri+=syn+" "+words[i+1]+" "+words[i+2]
                        strm+=sen[i][0]+" "+words[i+1]+" "+words[i+2]
                    else:
                        flag=False
                        break
                    simi=checkSimilarity(TextBlob(stri),TextBlob(strm))
                    if simi>maxi:
                        msen=syn
                        maxi=simi
                
                if flag==True:
                    temp+=msen+" "
                    continue
                if flag==False:
                    temp+=sen[i][0]+" "
                    continue
            else:
                temp+=sen[i][0]+" "
            
            
        temp+=sentence[-1]
        #print(temp)
        return temp

'''
sentences=""
with io.open('artical.txt',mode='r',encoding='utf-8') as myfile:
    document1=myfile.read()
    
    char=""
    for character in document1:
        sentences+=character

sentences=TextBlob(sentences)
for sentence in sentences.sentences:
    #print("jasdjdb:",str(sentence))
    rewriter(str(sentence))

#print(checkSimilarity(TextBlob("nice"),TextBlob("good")))
'''
def result(murl):
    r=requests.get(murl)
    soup=BeautifulSoup(r.content,"html.parser")
    old_text=''
    old_header=soup.find_all('h1', {'class':'entry-title'})
    if old_header==None:
        return render(request,'scrap/index.html')
    t=old_header
    old_header=old_header[0].text
    old_text=soup.find('div',{'class':'pf-content'})
    
    if old_text=='':
        return render(request,'scrap/index.html')
    
    old_text=old_text.text
    
    sentences=TextBlob(str(old_text))
    final_txt=""
    for sentence in sentences.sentences:
        #print("jasdjdb:",str(sentence))
        final_txt+=rewriter(str(sentence))
    '''
    final_header=rewriter(str(old_header))
    new_entry=article(url=murl,old_name=old_header,old_txt=old_text,new_name=final_header,new_txt=final_txt)
    try:
        new_entry.save()
    except IntegrityError as e:
        return render_to_response("scrap/template.html", {"message": t})
    return render(request,'scrap/end.html')
    '''
    print(final_txt)

result('http://www.thetravelmagazine.net/brighton-ba-i360-observation-tower.html')
