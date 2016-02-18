#!/usr/bin/python
import re
import nltk
import sys
import getopt

            	

def usage():
    print "usage: " + sys.argv[0] + " -i directory-of-documents -d dictionary-file -p postings-file"

input_file_b = input_file_t = output_file = None
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
        postings_file = a
    else:
        assert False, "unhandled option"
if documents_dir_i == None or dictionary_file_d == None or postings_file == None:
    usage()
    sys.exit(2)

# t0 = time.time()
# LM = build_LM(input_file_b)
# test_LM(input_file_t, output_file, LM)
# t1 = time.time()

# print "this run with n=" + str(gram_size) + " took " + str(t1-t0)
