#HW2 by akshat dubey
#used reuters training data for this HW, found in NLTK toolkit
import ast
import cPickle as pickle
import getopt
import math
import nltk
import sys
import time

stemmer = nltk.stem.porter.PorterStemmer()
all_list = []

def parse_query(query):
    '''
    parses the query using dijkstra's Shunting Yard algorithm to convert an infix notation to polish post fix notation.
    '''
    args = []
    ops = []
    tokens = nltk.word_tokenize(query)
    for token in tokens:
        if (token == 'NOT'):
            args.append(token)
        elif (token == 'AND'):
            if (len(args) > 0):
                while(args[len(args) - 1] == 'NOT'):
                    ops.append(args.pop())
            args.append(token)
        elif (token == 'OR'):
            while(True):
                if (len(args) <= 0):
                    break
                elif (args[len(args) - 1] == 'NOT' or args[len(args) - 1] == 'AND'):
                    ops.append(args.pop())
                else:
                    break
            args.append(token)
        elif (token == '('):
            args.append(token)
        elif (token == ')'):
            while (len(args) > 0):
                arg = args.pop()
                if (arg != '('):
                    ops.append(arg)
                else:
                    break
            if (len(args) == 0):
                print "Query is invalid. Brackets don't match."
                sys.exit(1)
        else:
            processed_token = stemmer.stem(token.lower())
            ops.append(processed_token)

    while(len(args) > 0):
        ops.append(args.pop())

    return ops

def get_postings_list(word):
    '''
    retrieves the posting list from the postings file based on the word offset in the dictionary file
    '''
    offset = words[word][1]
    postings.seek(offset)
    line = postings.readline()
    postings_list = ast.literal_eval(line)
    return postings_list

def not_list(xs):
    '''
    inverts the list by taking the difference between the universal list and this supplied list
    '''
    zs = []
    ys = all_list
    x_i, y_i = 0, 0
    while(x_i < len(xs)):
        x, y = xs[x_i], ys[y_i]

        if (x == y):
            x_i += 1
            y_i += 1
        else:
            zs.append(y)
            y_i += 1
    zs += ys[y_i:]
    return zs

def and_list(xs, ys):
    '''
    returns the intersection of the two lists supplied
    '''
    x_gap = int(math.sqrt(len(xs)))
    y_gap = int(math.sqrt(len(ys)))
    zs = []
    x_i, y_i = 0, 0
    while(x_i < len(xs) and y_i < len(ys)):
        x, y = xs[x_i], ys[y_i]

        if (x == y):
            zs.append(x)
            x_i += 1
            y_i += 1
        elif (x < y):
            if (x_i + x_gap < len(xs) and xs[x_i + x_gap] <= y):
                x_i += x_gap
            else:
                x_i += 1
        elif (x > y):
            if (y_i + y_gap < len(ys) and ys[y_i + y_gap] <= x):
                y_i += y_gap
            else:
                y_i += 1

    return zs

def or_list(xs, ys):
    '''
    returns the union of the two lists supplied.
    '''
    zs = []
    x_i, y_i = 0, 0
    while(x_i < len(xs) and y_i < len(ys)):
        x, y = xs[x_i], ys[y_i]

        if (x == y):
            zs.append(x)
            x_i += 1
            y_i += 1
        elif (x < y):
            zs.append(x)
            x_i += 1
        elif (x > y):
            zs.append(y)
            y_i += 1

    if (x_i < len(xs)):
        zs += xs[x_i:]
    elif (y_i < len(ys)):
        zs += ys[y_i:]

    return zs

def perform_operations(ops):
    '''
    executes the post fix stack and optimizes boolean operations in order.
    '''
    os = []
    for op_i in range(len(ops)):
        op = ops[op_i]
        if (op == 'NOT'):
            idxs = os.pop()
            os.append(not_list(idxs))
        elif (op == 'AND'):
            # reorder operand stack os for maximum efficiency
            and_count = 1
            for i in range(op_i + 1, len(ops)):
                if (ops[i] == 'AND'):
                    and_count += 1
                else:
                    break

            # reorder and_count + 1 top elements in the os
            if (and_count > 1):
                os_vals = os[(len(os) - (and_count + 1)):]
                os_vals.sort(key=len)
                os = os[:len(os) - (and_count + 1)]
                os_vals.reverse()
                os += os_vals

            idxs1 = os.pop()
            idxs2 = os.pop()
            os.append(and_list(idxs1, idxs2))
        elif (op == 'OR'):
            idxs1 = os.pop()
            idxs2 = os.pop()
            os.append(or_list(idxs1, idxs2))
        else:
           os.append(get_postings_list(op))

    return os.pop()

def answer_queries():
    queries_file = open(query_file_q, 'r')
    queries = queries_file.read().splitlines()
    output = open(output_file_o, 'w')
    for query in queries:
        ops = parse_query(query)
        output_list = perform_operations(ops)
        notFirst = False
        for id in output_list:
            if (notFirst):
                output.write(' ')
            output.write(str(id))
            notFirst = True
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
    dictionary_file_d = 'dictionary.txt'
    postings_file_p = 'postings.txt'
    query_file_q = 'queries.txt'
    output_file_o = 'output.txt'
    # usage()
    # sys.exit(2)

t0 = time.time()
print "reading dictionary"
words = pickle.load(open(dictionary_file_d, 'r'))
all_list = words.items()[0][1]
print "opening postings file"
postings = open(postings_file_p, 'r')
print ("answering queries...")
answer_queries()
t1 = time.time()
print "this run took " + str(t1-t0)
