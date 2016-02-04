#!/usr/bin/python
import re
import nltk
import sys
import getopt

gram_size = 4
languages = {"indonesian": 0, "malaysian":1, "tamil":2}

def build_LM(in_file):
    """
    build language models for each label
    each line in in_file contains a label and an URL separated by a tab(\t)
    """
    print 'building language models...'
    # This is an empty method
    # Pls implement your code in below
    f = open(in_file, 'r')
    langModel = {}
    for line in f:
        language = line.split(" ")[0]
        line = line[(len(language)+1):-1] #omit the language, extra space and endline
        # print "printing end of line: "
        # print line[len(line)-1]
        line_size = len(line)
        for i in range(line_size + gram_size -1):
            gram = ""
            if((i+1)<gram_size):
                for x in xrange(gram_size - (i+1)):
                	gram += ' '
                gram += line[:i+1]
            elif(i >= line_size):
            	gram += line[(i+1)-gram_size:]
            	for x in xrange((i+1) - line_size):
                	gram += ' '
            else:
            	gram = line[((i+1)-gram_size):i+1]

            if gram in langModel:
            	langModel[gram][languages[language]]+=1
            else:
            	langModel[gram] = [1, 1, 1]
            	langModel[gram][languages[language]]+=1
            print language + " " + gram + ": " + str(langModel[gram])


    return langModel
    
def test_LM(in_file, out_file, LM):
    """
    test the language models on new URLs
    each line of in_file contains an URL
    you should print the most probable label for each URL into out_file
    """
    print "testing language models..."
    # This is an empty method
    # Pls implement your code in below
    f = open(in_file)
    for line in f:
    	line_size = len(line)
        for i in range(line_size + gram_size):
            gram = ""
            if(i+1<gram_size):
                for x in xrange(gram_size - i-1):
                	gram += ' '
                gram += line[:i]
            elif(i >= line_size):
            	gram += line[i-gram_size+1:]
            	for x in xrange(line_size - i-1):
                	gram += ' '
            else:
            	gram = line[(i-4):i]
            # if gram in LM:




def usage():
    print "usage: " + sys.argv[0] + " -b input-file-for-building-LM -t input-file-for-testing-LM -o output-file"

input_file_b = input_file_t = output_file = None
try:
    opts, args = getopt.getopt(sys.argv[1:], 'b:t:o:')
except getopt.GetoptError, err:
    usage()
    sys.exit(2)
for o, a in opts:
    if o == '-b':
        input_file_b = a
    elif o == '-t':
        input_file_t = a
    elif o == '-o':
        output_file = a
    else:
        assert False, "unhandled option"
if input_file_b == None or input_file_t == None or output_file == None:
    usage()
    sys.exit(2)

LM = build_LM(input_file_b)
# print LM
# test_LM(input_file_t, output_file, LM)
