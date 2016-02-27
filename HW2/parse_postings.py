import os
import itertools

dictionary_file = open("dictionary.txt", 'r')
posting_file = open("postings.txt", 'r')
dictionary = []
posting_list = {}

for dict_word, posting in itertools.izip(dictionary_file, posting_file):
	dictionary.append(dict_word[:-1])
	doc_list = posting.split(":")
	for doc in doc_list:
		skip_pointer_check = doc.split(",")
		if len(skip_pointer_check) > 1:
			skip_doc = []
			skip_doc.append(int(skip_pointer_check[0][1:]))
			skip_doc.append(int(skip_pointer_check[1][:-2]))
			doc = skip_doc
		else:
			# print "HELLOWTF"
			temp = ''.join([i for i in doc if i.isdigit()])
			doc = int(temp)
			# print doc
	posting_list[dict_word[:-1]] = doc_list

# print dictionary
print posting_list