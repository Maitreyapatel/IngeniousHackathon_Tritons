from django.shortcuts import render
from textblob import TextBlob as tb
import numpy as np
import requests
from bs4 import BeautifulSoup
import codecs
from afinn import Afinn
from requests.auth import HTTPBasicAuth
import io
import json

# Create your views here.

good = 0
bad = 0
average = 0
counting = 0



def appsum(request):
    if request.method == 'POST':
        url = request.POST["desc"]


        #good,bad,average,counting,txt = reviews('scrap_review.txt', url)


        with io.open("review.txt", mode='r', encoding='utf-8') as myfile:
            document1 = myfile.read()
            document2 = u''
            char = ""
            for character in document1:
                ordchar = ord(character)
                if character is '.' and char is '.':
                    document2 += ''
                if ordchar <= 0xFFFF:
                    if character is '0' or character is '1' or character is '2' or character is '3' or character is '4' or character is '5' or character is '6' or character is '7' or character is '8' or character is '9':
                        document2 += " � "
                    else:
                        document2 += character
                else:
                    document2 += ''
                if character is '.' and char is not '.':
                    document2 += ' '
                char = character

        txt = str(tb(document2))


        data = {
            'code':txt,
        }

        r = requests.post(url="http://127.0.0.1:9000/snippets/", auth=HTTPBasicAuth('username', 'password'), data=data)

        print(type(r.json))
        datastore = json.loads(r.text)

        neg = []
        pos = []

        n = 0
        p = 0

        for sen in datastore['negative']:
            neg.append(str(sen))
            n+=1

        for sen in datastore['positive']:
            pos.append(str(sen))
            p+=1

        #,{'result':url,'good':good*100/counting,'bad':bad*100/counting,'average':average*100/counting}
        return render(request,'resultsum.html',{'positive':pos,'pl':p,'negative':neg,'nl':n})
    return render(request,'appsum.html')





def reviews(file, url):
    txt = ""
    murl = "http://www.amazon.com"
    headers = requests.utils.default_headers()
    headers.update({'User-Agent': 'Mozilla/5.0 (X11; Mint; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/51.0', })
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, "html.parser")
    # print(soup)
    url = soup.find('a', {'id': 'dp-summary-see-all-reviews'})['href']
    afinn = Afinn()
    url = str(murl + url)
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, "html.parser")
    link = soup.find('li', {'class': 'a-last'})
    # print(link)
    link = link.find('a')['href']
    url = str(murl + link[0:-31])
    print("Scrapping....!!")
    for i in range(11):
        url_main = url + str(i + 1)
        r = requests.get(url_main, headers=headers)
        # print("Hello")
        soup = BeautifulSoup(r.content, "html.parser")
        g_data = soup.find_all("div", {"class": "a-section review"})
        # print(g_data)
        global counting
        global average
        global good
        global bad
        # g_data = soup.find_all("div",{"class":"a-row review-data"})
        for item in g_data:
            counting = counting + 1
            review = item.find_all("div", {"class": "a-row review-data"})[0].text
            # print(review)
            txt = txt + review
            rate = item.find_all("span", {"class": "a-icon-alt"})[0].text
            rating = int(rate[0])
            # print(rating)
            pol_blob = round(tb(review).sentiment.polarity, 3)

            if rating == 5 and pol_blob > 0.1:
                good = good + 1
            elif rating == 4 and pol_blob > 0.45:
                good = good + 1
            elif rating == 4 and pol_blob > 0.2:
                pol_afin = afinn.score(review)
                if pol_afin >= 4:
                    good = good + 1
                else:
                    average = average + 1
            elif rating == 3 and pol_blob > 0.7:
                good = good + 1
            elif rating == 3 and pol_blob < 0:
                bad = bad + 1
            elif rating == 2 and pol_blob < 0:
                bad = bad + 1
            elif rating == 2 and pol_blob <= 0.175:
                pol_afin = afinn.score(review)
                if pol_afin < 0:
                    bad = bad + 1
                else:
                    average = average + 1
            elif rating == 1 and pol_blob < 0:
                bad = bad + 1
            elif rating == 1 and pol_blob <= 0.2:
                pol_afin = afinn.score(review)
                if pol_afin < 0:
                    bad = bad + 1
                else:
                    average = average + 1
            else:
                average = average + 1

    with codecs.open(file, 'w', encoding='utf-8') as document:
        document.write(txt)

    return good,bad,average,counting,txt
