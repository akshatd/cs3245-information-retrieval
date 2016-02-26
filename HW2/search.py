#HW2 by akshat dubey
#used reuters training data for this HW, found in NLTK toolkit
import nltk
import sys
import getopt

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

# t0 = time.time()
# LM = build_LM(input_file_b)
# test_LM(input_file_t, output_file, LM)
# t1 = time.time()

# print "this run with n=" + str(gram_size) + " took " + str(t1-t0)
