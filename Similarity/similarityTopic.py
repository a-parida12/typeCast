#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import re, math
from collections import Counter
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import glob
import os
import random


LANG='english'
FOLDER='./ReferenceDocs'
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

listings=os.listdir(FOLDER)

file1 = open('workfile.txt','r')
text1=file1.read() 

CosineScores={}

for listing in listings:
    files=glob.glob(FOLDER+'/'+listing+'/*.txt')
    #print FOLDER+'/'+listing+'/*.txt'
    file2 = open(files[random.randint(0,len(files))],'r')
    text2 = file2.read() 

    vector1 = text_to_vector(text1)
    vector2 = text_to_vector(text2)

    cosine = get_cosine(vector1, vector2)
    CosineScores[listing] = cosine
    file2.close()

print CosineScores