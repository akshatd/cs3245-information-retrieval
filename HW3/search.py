#HW3 by Varun Patro
from __future__ import division
import ast
import cPickle as pickle
import getopt
import math
import nltk
import sys
import time

DEBUG_MODE = False

stemmer = nltk.stem.porter.PorterStemmer()
all_list = []
all_dict = dict()
N = 1

def parse_query(query):
    '''
    Stems the lower case query using Porter's stemmer.
    :param query:
    :return: stemmed query
    '''
    return stemmer.stem(query.lower())

def cosine_score(query):
    '''
    Scores the documents using a cosine score based on the lnc.ltc ranking scheme.
    Does so by first, computing the query vector using ltc scheme. Then for each word in the query,
    the score of the document containg that word is updated. Finally, the score of each document is normalized,
    and returned.
    :param query:
    :return Scores:
    '''
    Scores = dict()
    q_terms = nltk.word_tokenize(query)
    q_vec = dict()
    total_wtq = 0

    for term in q_terms:
        tf = 1 + math.log(q_terms.count(term), 10)
        if term in words:
            postings_info = words[term]
            df = postings_info[0]
            idf = math.log(N / df, 10)
            wtq = tf * idf
            total_wtq += wtq ** 2
            q_vec[term] = dict()
            q_vec[term]['wtq'] = wtq

    for term in q_vec:
        q_vec[term]['norm'] = q_vec[term]['wtq'] / math.sqrt(total_wtq)

    for term in q_vec:
        postings_info = words[term]
        postings_offset = postings_info[1]
        postings.seek(postings_offset)
        line = postings.readline()
        p_list = ast.literal_eval(line)
        for pair in p_list:
            wtd = 1 + math.log(pair[1], 10)
            if pair[0] in Scores:
                Scores[pair[0]] += q_vec[term]['norm'] * wtd
            else:
                Scores[pair[0]] = q_vec[term]['norm'] * wtd

    for tid in Scores:
        Scores[tid] = Scores[tid] / all_dict[tid]

    return Scores

def answer_queries():
    '''
    Reads the queries from the file in order and for each query, writes the at most 10 docIds to the output file.
    :return None:
    '''
    queries_file = open(query_file_q, 'r')
    queries = queries_file.read().splitlines()
    output = open(output_file_o, 'w')
    for raw_query in queries:
        query = parse_query(raw_query)
        Scores = cosine_score(query)
        sorted_scores = sorted(Scores.items(), key=lambda x: (x[1], x[0]), reverse=True)
        output_list = []
        for i in range(min(len(sorted_scores), 10)):
            output_list.append(sorted_scores[i][0])
        output.write(' '.join([str(i) for i in output_list]))
        output.write('\n')

def usage():
    print "usage: " + sys.argv[0] + " -d dictionary-file -p postings-file -q file-of-queries -o output-file-of-results"

dictionary_file_d = postings_file_p = query_file_q = output_file_o = None
try:
    opts, args = getopt.getopt(sys.argv[1:], 'd:p:q:o:')
except getopt.GetoptError, err:
    usage()
    sys.exit(2)
for o, a in opts:
    if o == '-d':
        dictionary_file_d = a
    elif o == '-p':
        postings_file_p = a
    elif o == '-q':
        query_file_q = a
    elif o == '-o':
        output_file_o = a
    else:
        assert False, "unhandled option"
if dictionary_file_d == None or postings_file_p == None or query_file_q == None or output_file_o == None:
    if DEBUG_MODE:
        dictionary_file_d = 'dictionary.txt'
        postings_file_p = 'postings.txt'
        query_file_q = 'queries.txt'
        output_file_o = 'output.txt'
    else:
        usage()
        sys.exit(2)

t0 = time.time()
print "reading dictionary"
words = pickle.load(open(dictionary_file_d, 'r'))
all_list = words.items()[0][1]
all_dict = dict(all_list)
N = len(all_dict)
print "opening postings file"
postings = open(postings_file_p, 'r')
print ("answering queries...")
answer_queries()
t1 = time.time()
print "this run took " + str(t1-t0)
