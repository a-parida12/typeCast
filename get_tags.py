#!/usr/bin/env python3

import utils as datautils
import operator

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

def test_article():
    token_processor = TokenProcessor()
    testfile = "Similarity/workfile.txt"

    # FIXME
    documents = datautils.get_train_documents("inputdocuments/Tagged_Documents_2018-05-25_215336/Geschichte/*.txt", token_processor)

    doc = datautils.get_test_document(testfile, token_processor)

    tagger = Tagger()
    for document in documents:
        tagger.add_document(document)

    weighted_terms = tagger.get_terms_weighted_by_tfidf(doc)
    tags = tagger.get_tags_using_weighted_terms(weighted_terms)
    print("Generated for the document are:\n{}".format(tags))


def main():
    test_article()

if __name__ == "__main__":
    main()
