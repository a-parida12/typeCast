from flask import Flask
from flask import request
from flask import redirect, url_for, render_template
import textract

# from werkzeug import secure_filename

app = Flask(__name__)

#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import re, math
from collections import Counter
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import glob
import os
import random
import cPickle

import utils as datautils
import operator
import cPickle
import itertools
import pandas as pd
import json

from eventregistry import *
from document_clean import Document
from pprint import pprint
from preprocess import TokenProcessor
from term_freq import TFIDF

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
import itertools

UPLOAD_FOLDER = '/Users/sricharanchiruvolu/hackathons/hackaburg/typeCast/tmp/'
ALLOWED_EXTENSIONS = set(['txt', 'docx', 'doc', 'pdf'])


LANG='german'
FOLDER='inputdocuments/Tagged_Documents_2018-05-25_215336'
WORD = re.compile(r'\w+')
BAGGING=100
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


def similarityTopic(text):

  listings=os.listdir(FOLDER)

  # file1 = open('workfile.txt','r')
  # text1=file1.read() 
  text1=text
  CosineScores={}

  for listing in listings:
      

      if listing != '.DS_Store':
          CosineScores[listing] =0.0

          files=glob.glob(FOLDER+'/'+listing+'/*.txt')
          #print len(files)
          #print listing
          for i in range(BAGGING):
              file2 = open(files[random.randint(0,len(files)-1)],'r')
              text2 = file2.read() 

              vector1 = text_to_vector(text1)
              vector2 = text_to_vector(text2)

              cosine = get_cosine(vector1, vector2)
              CosineScores[listing] = CosineScores[listing] + cosine
              file2.close()

  Result= {k:v/BAGGING for k, v in CosineScores.items() if v == max(CosineScores.values())}
  with open(r"Result.pickle", "wb") as output_file:
      cPickle.dump(Result, output_file)
  return Result.keys()[0]


class Tagger:
    def __init__(self):
        self.documents = {}
        self.tfidf = TFIDF()

    def add_document(self, document):
        self.documents[document.id] = document

    def display(self):
        for id in self.documents:
            self.documents[id].display()

    def get_terms_weighted_by_tfidf(self, document):
        documents = [ self.documents[key] for key in self.documents ]
        tfidf_list = self.tfidf.calculate_tfidf_document(documents, document)
        weighted_terms = {}
        for d in tfidf_list:
            term = d["term"]
            tf = d["tf"]
            idf = d["idf"]
            weighted_terms[term] = tf * idf
        return weighted_terms

    def get_tags_using_weighted_terms(self, weighted_terms, size=10):
        sorted_terms = sorted(weighted_terms.items(), key = operator.itemgetter(1), reverse=True)
        length = len(weighted_terms)
        size = length if size > length else size
        tags = []
        for i in range(size):
            tags.append(sorted_terms[i][0])
        return tags

    def __str__(self):
        return str(pprint(vars(self)))

def test_article(tagDict,i):
    token_processor = TokenProcessor()
    testfile = "Similarity/workfile.txt"

    with open(r"Similarity/Result.pickle", "rb") as input_file:
        typeDict = cPickle.load(input_file)
    tipe=typeDict.keys()[0]
    #print tipe
    documents = datautils.get_train_documents("inputdocuments/Tagged_Documents_2018-05-25_215336/"+tipe+"/*.txt", token_processor)

    doc = datautils.get_test_document(testfile, token_processor)

    tagger = Tagger()
    for document in documents:
        tagger.add_document(document)

    weighted_terms = tagger.get_terms_weighted_by_tfidf(doc)
    tags = tagger.get_tags_using_weighted_terms(weighted_terms)
    #print("Generated for the document are:\n{}".format(tags))
    tagDict[i]=tags
    return tagDict


@app.route("/")
def index():
    return render_template("base.html")
    # return "Welcome to typeCast!"


@app.route("/categoryfromtext")
def getCategoryFromText():
  text = request.args.get('text')
  if text is None:
    return "Please give a 'text' parameter to analyse."
  data = {}
  result_key = similarityTopic(text)
  data['text_type'] = str(result_key)
  json_data = json.dumps(data)
  return json_data


def analyseText(input_text):
  if input_text is None:
    return "Please give a 'text' parameter to analyse."
  data = {}
  result_category = similarityTopic(input_text)

  tagDict={}
  for i in range(25):
      tagDict=test_article(tagDict,i)

  # testfile = "Similarity/workfile.txt"
  token_processor = TokenProcessor()
  er = EventRegistry(apiKey = 'ab40eb06-3900-4689-a369-b4098f4e49ef')
  # doc = datautils.get_test_document(testfile, token_processor)

  # file1 = open(testfile,'r')
  text = input_text

  analytics = Analytics(er)
  ann = analytics.annotate(text)
  annotations = []
  parsed_json = json.loads(json.dumps(ann))
  for annotation in parsed_json[u'annotations']:
    annotations.append(annotation[u'title'])
  # print(annotations)

  my_list = []
  for i in tagDict.keys():
    my_list.append(tagDict[i])
  my_list= list(itertools.chain(*tagDict.values()))
  my_list = my_list + annotations


  data['text_category'] = str(result_category)
  data['encoding'] = 'utf-8'
  data['tags'] = dict(pd.value_counts(my_list))
  json_data = json.dumps(data)
  return json_data



@app.route("/tagsfromtext")
def getTagsFromText():
  input_text = request.args.get('text')
  if input_text is None:
    return "Please give a 'text' parameter to analyse."
  data = {}
  result_category = similarityTopic(input_text)

  tagDict={}
  for i in range(25):
      tagDict=test_article(tagDict,i)

  # testfile = "Similarity/workfile.txt"
  token_processor = TokenProcessor()
  er = EventRegistry(apiKey = 'ab40eb06-3900-4689-a369-b4098f4e49ef')
  # doc = datautils.get_test_document(testfile, token_processor)

  # file1 = open(testfile,'r')
  text = input_text

  analytics = Analytics(er)
  ann = analytics.annotate(text)
  annotations = []
  parsed_json = json.loads(json.dumps(ann))
  for annotation in parsed_json[u'annotations']:
    annotations.append(annotation[u'title'])
  my_list= list(itertools.chain(*tagDict.values()))
  my_list = my_list + annotations

  data['text_category'] = str(result_category)
  data['encoding'] = 'utf-8'
  data['tags'] = dict(pd.value_counts(my_list))
  json_data = json.dumps(data)
  return json_data


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


cwd = os.getcwd()
llist = []
def getFileName( path ):

  for subdir, dirs, files in os.walk(path):
    for file in files:
        #print os.path.join(subdir, file)
        filepath = subdir + os.sep + file
        hidden_file = filepath
        if file != '.DS_Store':
          llist.append(filepath)
  return llist

@app.route("/documentAnalyser", methods=['GET', 'POST'])
def analyseDocument():
  if request.method == 'POST':
      file = request.files['file']
      if file and allowed_file(file.filename):
          filename = file.filename
          file.save(os.path.join(UPLOAD_FOLDER, filename))

          current_file = os.path.join(UPLOAD_FOLDER, filename)
          current_filename = os.path.splitext(filename)[0]
          current_fileext = os.path.splitext(filename)[1] 

          if current_fileext == '.txt':
            current_file2 = open(current_file, 'r')
            text = current_file2.read()
            return analyseText(text)


          else:
            print("input is saved as " + current_file)
            parsed_text = textract.process(current_file, encoding='utf-8')
            doc_path = UPLOAD_FOLDER
            try: 
              os.makedirs(doc_path)
            except OSError:
                if not os.path.isdir(doc_path):
                    raise
            print("analysing " + current_filename +  '.txt')
            file = open(current_filename + '.txt', 'w+')
            file.write(parsed_text)
            file.close()

            current_file2 = open(current_filename + '.txt', 'r')
            text = current_file2.read()
            return analyseText(text)
          # return redirect(url_for('index'))
  return """
  <!doctype html>
  <title>TypeCast --- Text Annotation and Tagging tool</title>
  <h1>Upload new File</h1>
  <form action="" method=post enctype=multipart/form-data>
    <p><input type=file name=file>
       <input type=submit value=Upload>
  </form>
  <p>%s</p>
  """ % "<br>".join(os.listdir(UPLOAD_FOLDER),)


# Fake news

LANGUAGE_FAKENEWS='english'
WORD = re.compile(r'\w+')

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
    #print (float(Reputations[Reputations['source']==matching]['ScaledRepo'].iloc[0]))
    return float(Reputations[Reputations['source']==matching]['ScaledRepo'].iloc[0])   

def set_reputation_score(url,score):
     Reputations=pd.read_csv("reputations.csv")
     matching=get_closest_match(url,list(Reputations['source']))     
     newScore=0.9*Reputations[Reputations['source']==matching]['ScaledRepo'].iloc[0]+0.1*score
     loci=Reputations.index[Reputations['source'] == matching].tolist()[0]
     Reputations.loc[loci,'ScaledRepo']=newScore
     Reputations.to_csv("reputations.csv",index=False)



@app.route("/munichnews")
def LocalNews():
  # input_url = request.args.get('url')
  # if input_url is None:
  #   return "Give an Article, find the genuity of it. Please give an article 'url' parameter to analyse."
  TweetLink=pd.read_csv("geotweets.csv")
  linkArray=list(set(TweetLink.dropna()['longitude'].values))

  df_ = pd.DataFrame(columns=['source','Headline','Body','Relevancy'])
  for source in linkArray[0:10]:
      url = requests.get(source)
      #print source
      tree = fromstring(url.content)
      if tree is not None:
        title = tree.findtext('.//title')

        body = ''.join(BeautifulSoup(url.text, "html.parser").stripped_strings)
        processed_text = processText(source)

        cosine_scores=[]
        irrelavecy_index = 0
        score=0
        
        #print processed_text
        for text in processed_text:
            vector1 = text_to_vector(title)
            vector2 = text_to_vector(text)
            cosine = get_cosine(vector1, vector2)
            if cosine != 0.0:
                irrelavecy_index = (irrelavecy_index + 1)
                cosine_scores.append(cosine)
                if len(processed_text) != 0:
                    irrelavecy_index = irrelavecy_index / float(len(processed_text))
                    relavency_score =irrelavecy_index

                    rep_score = get_reputation_score(source)
                    #print(relavency_score)
                    relavency_score = (rep_score + relavency_score) / 2
                    score= relavency_score
                    set_reputation_score(source, relavency_score)

                    #print(rep_score)
                    #print "Relavancy(%)=",100-100*relavency_score
        
        if len(processed_text)>1:
            data = {'source': source, 'Headline': title,'Body':' '.join(processed_text) ,'Relevancy':100-100*score}
            dataframeing=pd.DataFrame(data=data, index=[0])
            listdf=[df_,dataframeing]
            print(score)
            df_ = pd.concat(listdf,sort=False,ignore_index=True)
  d = [ 
    dict([
        (colname, row[i]) 
        for i,colname in enumerate(df_.columns)
    ])
    for row in df_.values
  ]
  return json.dumps(d)          

  # return json.dumps(df_.to_json())
  # df_.to_csv('truaidnas.csv',index=False,encoding='utf-8')


@app.route("/relavencycheck")
def relavencyCheck():
  input_url = request.args.get('url')
  if input_url is None:
    return "Check the relavency score of an Article. Please give a 'url' parameter to analyse."
  url = requests.get(input_url)
  tree = fromstring(url.content)
  title = tree.findtext('.//title')

  body = ''.join(BeautifulSoup(url.text, "html.parser").stripped_strings)


  processed_text = processText(input_url)

  # 
  cosine_scores=[]

  irrelavecy_index = 0
  for text in processed_text:
    vector1 = text_to_vector(title)
    vector2 = text_to_vector(text)
    cosine = get_cosine(vector1, vector2)
    if cosine != 0.0:
      irrelavecy_index = (irrelavecy_index + 1)
    cosine_scores.append(cosine)
  if len(processed_text) != 0:
      irrelavecy_index = irrelavecy_index / float(len(processed_text))
  relavency_score =irrelavecy_index

  rep_score = get_reputation_score(input_url)
  relavency_score = (rep_score + relavency_score) / 2

  set_reputation_score(input_url, relavency_score)

  data = {}
  data['Relavancy(%)'] = 100-100*relavency_score
  json_data = json.dumps(data)
  return json_data
  # return "Relavancy(%) = ",100-100*relavency_score

















