

# Given an article find the genuity of it.
from bs4 import BeautifulSoup
import requests, urllib2
from lxml.html import fromstring

import jellyfish
import re, math
from collections import Counter
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import glob
import os
import random
import pandas as pd

LANG='english'
# source = "http://abc7news.com/politics/former-pres-obama-spotted-in-san-francisco/3521667/"
source = "http://sricharn.net"
WORD = re.compile(r'\w+')

def get_cosine(vec1, vec2):
     intersection = set(vec1.keys()) & set(vec2.keys())
     numerator = sum([vec1[x] * vec2[x] for x in intersection])

     sum1 = sum([vec1[x]**2 for x in vec1.keys()])
     sum2 = sum([vec2[x]**2 for x in vec2.keys()])
     denominator = math.sqrt(sum1) * math.sqrt(sum2)

     if not denominator:
        return 0.0
     else:
        return float(numerator) / denominator


def text_to_vector(text):
     words = WORD.findall(text.lower())
     
     #remove stop words
     stop = set(stopwords.words(LANG))
     stopwordsRemoved=[i for i in words if i not in stop]
     
     #stemming
     stemmer = SnowballStemmer(LANG)
     stemWords=[stemmer.stem(i) for i in stopwordsRemoved ]
     
     #print stemWords
     #print Counter(stemWords)
     return Counter(stemWords)

def processText(webpage):
    proc_text = []

    try:
        news_open = urllib2.urlopen(webpage)
        news_soup = BeautifulSoup(news_open, "lxml")
        news_para = news_soup.find_all("p", text = True)
        for item in news_para:
            para_text = (' ').join((item.text).split())
            proc_text.append(para_text)

    except urllib2.HTTPError:
        pass
    return proc_text

def get_closest_match(x,list_strings):
    best_match=None
    highest_jw=0
    
    for current_string in list_strings:
        current_score=jellyfish.jaro_winkler(unicode(x),unicode(current_string))
        
        if current_score >highest_jw :
            highest_jw =current_score
            best_match=current_string
            
    return best_match

def get_reputation_score(url):
    Reputations=pd.read_csv("reputations.csv")
    matching=get_closest_match(url,list(Reputations['source'])) 
    
    return float(Reputations[Reputations['source']==matching]['ScaledRepo'].iloc[0])   


def set_reputation_score(url,score):
     Reputations=pd.read_csv("reputations.csv")
     matching=get_closest_match(url,list(Reputations['source']))     
     newScore=0.9*Reputations[Reputations['source']==matching]['ScaledRepo'].iloc[0]+0.1*score
     loci=Reputations.index[Reputations['source'] == matching].tolist()[0]
     Reputations.loc[loci,'ScaledRepo']=newScore
     Reputations.to_csv("reputations.csv",index=False)

url = requests.get(source)
tree = fromstring(url.content)
title = tree.findtext('.//title')

body = ''.join(BeautifulSoup(url.text, "html.parser").stripped_strings)


processed_text = processText(source)

# 
cosine_scores=[]

irrelavecy_index = 0
for text in processed_text:
  vector1 = text_to_vector(title)
  vector2 = text_to_vector(text)
  cosine = get_cosine(vector1, vector2)
  if cosine == 0.0:
    irrelavecy_index = (irrelavecy_index + 1)
  cosine_scores.append(cosine)
if len(processed_text) != 0:
    irrelavecy_index = irrelavecy_index / float(len(processed_text))
relavency_score = 1 - irrelavecy_index

rep_score = get_reputation_score(source)

relavency_score = (rep_score + relavency_score) / 2

set_reputation_score(source, relavency_score)

print(rep_score)
print(relavency_score)
