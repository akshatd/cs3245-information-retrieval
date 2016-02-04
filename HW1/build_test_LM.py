#!/usr/bin/python
import re
import nltk
import sys
import getopt
import math

gram_size = 4
languages = {"indonesian": 0, "malaysian":1, "tamil":2}
inv_languages = {0:"indonesian", 1:"malaysian", 2:"tamil"}
lang_count = [0, 0, 0]
alien_threshold = 0.5 #set threshold here to see what happens :D

def cleanup(line):
	clean_line = ""
	clean_line.join(e for e in line if e.isalnum())
	return clean_line.lower()

def build_LM(in_file):
    """
    build language models for each label
    each line in in_file contains a label and an URL separated by a tab(\t)
    """
    print 'building language models...'
    # This is an empty method
    # Pls implement your code in below
    read_file = open(in_file, 'r')
    langModel = {}
    for line in read_file:
    	# line = cleanup(line)
        language = line.split(" ")[0]
        line = line[(len(language)+1):-1] #omit the language, extra space and endline
        line_size = len(line)
        for i in range(line_size + gram_size -1):
            lang_count[languages[language]] += 1
            gram = ""
            if((i+1)<gram_size):
            	#add padding
                for x in xrange(gram_size - (i+1)):
                	gram += ' '
                gram += line[:i+1]
            elif(i >= line_size):
            	gram += line[(i+1)-gram_size:]
            	#add padding
            	for x in xrange((i+1) - line_size):
                	gram += ' '
            else:
            	#normal case
            	gram = line[((i+1)-gram_size):i+1]

            if gram in langModel:
            	langModel[gram][languages[language]]+=1
            else:
            	langModel[gram] = [1, 1, 1]
            	for a in lang_count:
            		a +=1
            	langModel[gram][languages[language]]+=1
            # print language + " " + gram + ": " + str(langModel[gram])
    read_file.close()
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
    read_file = open(in_file)
    write_file = open(out_file, 'w')
    for line in read_file:
        line = line[:-1] #omit the endline
        line_size = len(line)
        total_prob = [0.0, 0.0, 0.0]
        final_lang = "other"
        total_grams = found_grams = 0.0
        for i in range(line_size + gram_size -1):
            total_grams += 1
            gram = ""
            if((i+1)<gram_size):
            	#add padding
                for x in xrange(gram_size - (i+1)):
                	gram += ' '
                gram += line[:i+1]
            elif(i >= line_size):
            	#add padding
            	gram += line[(i+1)-gram_size:]
            	for x in xrange((i+1) - line_size):
                	gram += ' '
            else:
            	#normal case
            	gram = line[((i+1)-gram_size):i+1]

            if gram in LM:
            	found_grams += 1
            	# print "found: " + gram
            	for l in languages:
            		total_prob[languages[l]] += math.log(float(LM[gram][languages[l]]) / float(lang_count[languages[l]]))
            # else:
            # 	print "not found: " + gram

        if (found_grams/total_grams) > alien_threshold:
        	final_lang = inv_languages[total_prob.index(max(total_prob))]
        # print "language is " + final_lang
        # print line + "\n"

        write_file.write(final_lang + " ")
        write_file.write(line + "\n")
	
    read_file.close()
    write_file.close()
            	

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
test_LM(input_file_t, output_file, LM)
