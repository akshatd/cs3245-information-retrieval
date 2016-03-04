#HW2 by akshat dubey
#used reuters training data for this HW, found in NLTK toolkit

import nltk
import sys
import os
import getopt
import time
from collections import OrderedDict
import math
# import csv
import cPickle as pickle

dictionary = {}
dictionary["!!!"] = 0
total_docs = set([])
postings_list = {}

def build_index(doc_id):
    total_docs.add(int(doc_id))
    full_filename = documents_dir_i[1:] + doc_id
    # print full_filename
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
                        postings_list[clean_token].add(int(doc_id))
                        # print str(postings_list[clean_token])
                    else:
                        dictionary[clean_token] = ""
                        tempset = set([int(doc_id)])
                        # print "NEW SET!!!" + str(tempset)
                        postings_list[clean_token] = tempset


def write_dictionary():
    dictionary["!!!"] = sorted(total_docs)
    sorted_dictionary = OrderedDict(sorted(dictionary.items(), key=lambda t: t[0]))
    dict_file = open(dictionary_file_d, 'wb')
    pickle.dump(sorted_dictionary, dict_file)
    # for word in sorted_dictionary:
    #     dict_file.write(word + "\n")
    dict_file.close()

def write_postings():
    sorted_postings = OrderedDict(sorted(postings_list.items(), key=lambda t: t[0]))
    temp_file = open(postings_file_p, 'wb')
    # postings_file = csv.writer(temp_file, delimiter = ':')
    for word_key in sorted_postings:
        sorted_doc_list = sorted(sorted_postings[word_key])
        # print str(sorted_doc_list)
        # insert skip pointers if length is > 2, otherwise no point
        doc_list_len = len(sorted_doc_list)
        # if (doc_list_len > 2):
        #     gap = int(math.sqrt(doc_list_len))
        #     for i in xrange(gap):
        #         if (i+1)*gap < doc_list_len:                        
        #             temp_list = (sorted_doc_list[i*gap], (i+1)*gap)
        #             # temp_list.append(sorted_doc_list[i*gap])
        #             # temp_list.append(sorted_doc_list[(i+1)*gap])
        #             # appending index itself
        #             # temp_list.append((i+1)*gap)
                    
        #             sorted_doc_list[i*gap] = temp_list
        # postings_file.write(str(sorted_doc_list) + "\n")
        # postings_file.writelines(':'.join(str(k) for k in i) + ',' for i in sorted_doc_list)
        # postings_file.writerow(sorted_doc_list)
        file_pointer = temp_file.tell()
        dictionary[word_key] = (doc_list_len, file_pointer)
        temp_file.write(str(sorted_doc_list) + '\n')
    temp_file.close()
    

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
# print os.listdir(documents_dir_i[1:])
for doc_filename in os.listdir(documents_dir_i[1:]):
    # print "building index for " + doc_filename + "\n"
    build_index(doc_filename)

# must do this first to get the byte offset for the dictionary file
print "writing postings\n"
write_postings()

print "writing dictionary\n"
write_dictionary()


t1 = time.time()

print "this run took " + str(t1-t0)
