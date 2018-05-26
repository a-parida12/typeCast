# -*- coding: utf-8 -*-

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


def main():
    tagDict={}
    for i in range(25):
        tagDict=test_article(tagDict,i)

    testfile = "Similarity/workfile.txt"
    token_processor = TokenProcessor()
    er = EventRegistry(apiKey = 'ab40eb06-3900-4689-a369-b4098f4e49ef')
    # doc = datautils.get_test_document(testfile, token_processor)

    file1 = open(testfile,'r')
    text = file1.read()

    analytics = Analytics(er)
    ann = analytics.annotate(text)
    annotations = []
    parsed_json = json.loads(json.dumps(ann))
    for annotation in parsed_json[u'annotations']:
      annotations.append(annotation[u'title'])
    # print(annotations)
    my_list= list(itertools.chain(*tagDict.values()))
    my_list = my_list + annotations
    print dict(pd.value_counts(my_list))
    
if __name__ == "__main__":
    main()
