#HW2 by akshat dubey
#used reuters training data for this HW, found in NLTK toolkit
import nltk
import sys
import getopt

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
            ops.append(token)

    while(len(args) > 0):
        ops.append(args.pop())

    return ops

def answer_queries():
    queries = open(query_file_q, 'r')
    for query in queries:
        print query
        ops = parse_query(query)

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


print ("answering queries...")
answer_queries()

# t0 = time.time()
# LM = build_LM(input_file_b)
# test_LM(input_file_t, output_file, LM)
# t1 = time.time()

# print "this run with n=" + str(gram_size) + " took " + str(t1-t0)
