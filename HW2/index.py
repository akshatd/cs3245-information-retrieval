#HW2 by akshat dubey
#used reuters training data for this HW, found in NLTK toolkit

import nltk
import sys
import os
import getopt
import time
from collections import OrderedDict

dictionary = set()
positngs_list = {}

def build_index(doc_id):
    full_filename = documents_dir_i[1:] + doc_id
    stemmer = nltk.stem.porter.PorterStemmer()
    doc_file = open(full_filename, 'r')
    for line in doc_file:
        sentence = nltk.sent_tokenize(line)
        for word in sentence:
            tokens = nltk.word_tokenize(word)
            for token in tokens:
                clean_token = stemmer.stem(token).lower()
                if clean_token.isalnum():
                    if clean_token in dictionary:
                        positngs_list[clean_token].add(doc_id)
                    else:
                        dictionary.add(clean_token)
                        tempset = set(doc_id)
                        positngs_list[clean_token] = tempset


def write_dictionary():
    sorted_dictionary = sorted(dictionary)
    dict_file = open(dictionary_file_d, 'w')
    for word in sorted_dictionary:
        dict_file.write(word + "\n")
    dict_file.close()

def write_postings():
    sorted_postings = OrderedDict(sorted(positngs_list.items(), key=lambda t: t[0]))
    postings_file = open(postings_file_p, 'w')
    for word_key in sorted_postings:
        sorted_doc_list = sorted(sorted_postings[word_key])
        # insert skip pointers
        # gap = int(math.sqrt(len(sorted_doc_list)))
        postings_file.write(str(sorted_doc_list) + "\n")
    postings_file.close()
    

def usage():
    print "usage: " + sys.argv[0] + " -i directory-of-documents -d dictionary-file -p postings-file"

documents_dir_i = dictionary_file_d = postings_file_p = None
try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:d:p:')
except getopt.GetoptError, err:
    usage()
    sys.exit(2)
for o, a in opts:
    if o == '-i':
        documents_dir_i = a
    elif o == '-d':
        dictionary_file_d = a
    elif o == '-p':
        postings_file_p = a
    else:
        assert False, "unhandled option"
if documents_dir_i == None or dictionary_file_d == None or postings_file_p == None:
    usage()
    sys.exit(2)

t0 = time.time()

# go file by file and create dictionary and postings
print "building index... \n"
for doc_filename in os.listdir("reuters/training"):
    # print "building index for " + doc_filename + "\n"
    build_index(doc_filename)

print "writing dictionary\n"
write_dictionary()

print "writing postings\n"
write_postings()

t1 = time.time()

print "this run took " + str(t1-t0)
