import requests
from bs4 import BeautifulSoup
import io
import codecs
from afinn import Afinn
from textblob import TextBlob as tb

good=0
bad=0
average=0
counting=0

def reviews(file,url):
    txt=""
    afinn = Afinn()
    print("Scrapping....!!")
    for i in range(11):
        url_main=url+str(i+1)
        r=requests.get(url_main)
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

    

reviews('time.txt','https://www.amazon.com/Apple-iPhone-Unlocked-Phone-128/product-reviews/B01M1EXQY4/ref=cm_cr_arp_d_paging_btm_2?ie=UTF8&reviewerType=avp_only_reviews&pageNumber=')

print(counting,good,bad,average)

