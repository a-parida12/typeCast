#!/usr/bin/env python3

import glob

from document_clean import Document
from preprocess import TokenProcessor

import random

def get_train_documents(documents_path, token_processor):
    if not token_processor:
        token_processor = TokenProcessor()
    documents = []
    filenames = glob.glob(documents_path)
    
    bagWidth=int(0.2*len(filenames))
    docsInBag=random.sample(range(len(filenames)-1), bagWidth)
    
    for i in docsInBag:
        #print i 
        doc = Document(i)
        doc.load_from_file(filenames[i])
        doc.extract_terms(token_processor)
        doc.generate_frequency_map()
        documents.append(doc)
    return documents

def get_test_document(filename, token_processor):
    if not token_processor:
        token_processor = TokenProcessor()
    doc = Document(filename)
    doc.load_from_file(filename)
    doc.extract_terms(token_processor)
    doc.generate_frequency_map()
    return doc


def main():
    documents = get_train_documents("inputdocuments/Tagged_Documents_2018-05-25_215336/*")
    print(documents)

if __name__ == "__main__":
    main()

