#HW2 by akshat dubey
#used reuters training data for this HW, found in NLTK toolkit
import ast
import nltk
import sys
import getopt
import cPickle as pickle

stemmer = nltk.stem.porter.PorterStemmer()
all_list = []

def parse_query(query):
    args = []
    ops = []
    tokens = nltk.word_tokenize(query)
    for token in tokens:
        print token
        if (token == 'NOT'):
            args.append(token)
        elif (token == 'AND'):
            if (len(args) > 0):
                while(args[len(args) - 1] == 'NOT'):
                    ops.append(args.pop)
            args.append(token)
        elif (token == 'OR'):
            if (len(args) > 0):
                while(args[len(args) - 1] == 'NOT' or args[len(args) - 1] == 'AND'):
                    ops.append(args.pop)
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
    offset = words[word][1] 
    postings.seek(offset)
    line = postings.readline()
    postings_list = ast.literal_eval(line)
    return postings_list

def not_list(xs):
    zs = []
    ys = all_list
    x_i, y_i = 0, 0
    while(x_i < len(xs)):
        x, y = xs[x_i], ys[y_i]
        if (type(x) == type((1, 2))):
            x = x[0]
        if (type(y) == type((1, 2))):
            y = y[0]

        if (x == y):
            x_i += 1
            y_i += 1
        else:
            zs.append(y)
            y_i += 1
    
    zs += ys[y_i:]
    return zs

def and_list(xs, ys):
    zs = []
    x_i, y_i = 0, 0
    while(x_i < len(xs) and y_i < len(ys)):
        x, y = xs[x_i], ys[y_i]
        if (type(x) == type((1, 2))):
            x = x[0]
        if (type(y) == type((1, 2))):
            y = y[0]

        if (x == y):
            zs.append(x)
            x_i += 1
            y_i += 1
        elif (x < y):
            x_i += 1
        elif (x > y):
            y_i += 1

    return zs

def or_list(xs, ys):
    zs = []
    x_i, y_i = 0, 0
    while(x_i < len(xs) and y_i < len(ys)):
        x, y = xs[x_i], ys[y_i]
        if (type(x) == type((1, 2))):
            x = x[0]
        if (type(y) == type((1, 2))):
            y = y[0]

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
    os = []
    for op in ops:
        if (op == 'NOT'):
            idxs = os.pop()
            os.append(not_list(idxs))
        elif (op == 'AND'):
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
    queries = open(query_file_q, 'r')
    output = open(output_file_o, 'w')
    for query in queries:
        print query
        ops = parse_query(query)
        print ops
        output_list = perform_operations(ops)
        notFirst = False
        for id in output_list:
            if (notFirst):
                output.write(' ')
            if (type(id) == type((1, 2))):
                id = id[0]
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
    usage()
    sys.exit(2)

print "reading dictionary"
words = pickle.load(open(dictionary_file_d, 'r'))
all_list = words.items()[0][1]
print "opening postings file"
postings = open(postings_file_p, 'r')
print ("answering queries...")
answer_queries()

# t0 = time.time()
# LM = build_LM(input_file_b)
# test_LM(input_file_t, output_file, LM)
# t1 = time.time()

# print "this run with n=" + str(gram_size) + " took " + str(t1-t0)
