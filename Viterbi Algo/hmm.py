#! /usr/bin/python
from __future__ import division
from nltk.corpus import brown
import numpy
import sys

TAG_SET = set()
TAG_LIST = []
V = set()

transition = {}
emission = {}
context = {}


def laplace(ngram, dictionary, type):
	k = 0.5
	wn_0 = ngram[0]
	wn_1 = ngram[1]	
	bgram = (wn_0, wn_1)		
	if type == 0:
		total = len(TAG_SET)		
	else:
		total = len(V)
	prob = 1.0*(dictionary.get(bgram, 0) + k)/(context.get(wn_0, 0) + k*total)
	return prob

def printdic(dicti):
	for key,value in dicti:
		print key,value

def viterbi(sentence):
	best_score = {}
	best_edge = {}
	best_score["0:<sen_BEG>"]=0
	best_edge["0:<sen_BEG>"]=None
	
	i=0
	for i in range(len(sentence)):
		for prev_tag in TAG_LIST:			
			for cur_tag in TAG_LIST:				
				if(best_score.get(str(i)+":"+prev_tag,-1)!=-1 and transition.get((prev_tag,cur_tag),-1)!=-1):					
					tag_gram = (prev_tag, cur_tag)
					trans = laplace(tag_gram,transition, 0)
					word_gram = (cur_tag,sentence[i][0])
					emit = laplace(word_gram,emission, 1)		
					score = best_score[str(i)+":"+prev_tag]+(-1*numpy.log10(trans))+(-1*numpy.log10(emit))										
					if(best_score.get(str(i+1)+":"+cur_tag,-1)==-1 or  best_score.get(str(i+1)+":"+cur_tag,-1)>score):
						best_score[str(i+1)+":"+cur_tag]=score
						best_edge[str(i+1)+":"+cur_tag]=str(i)+":"+prev_tag					
	cur_tag="<sen_END>"		
	for prev_tag in TAG_LIST:					
		if(best_score.get(str(i)+":"+prev_tag,-1)!=-1 and transition.get((prev_tag,cur_tag),-1)!=-1):					
			tag_gram = (prev_tag, cur_tag)			
			trans = laplace(tag_gram,transition, 0)			
			score = best_score[str(i)+":"+prev_tag]+(-1*numpy.log10(trans))			
			if(best_score.get(str(i+1)+":"+cur_tag,-1)==-1 or  best_score.get(str(i+1)+":"+cur_tag,-1)>score):				
				best_score[str(i+1)+":"+cur_tag]=score
				best_edge[str(i+1)+":"+cur_tag]=str(i)+":"+prev_tag								
				
	tags = []
	tags.append("<sen_END>")
	i=len(sentence)-1
	next_edge = best_edge[str(i)+":<sen_END>"]
	
	while(next_edge!="0:<sen_BEG>"):
		position= next_edge.split(":")[0]
		tag= next_edge.split(":")[1]
		
		
		tags.append(tag)
		next_edge=best_edge[next_edge]
	
	tags.reverse()	
	return tags	
	

def parse(data):
	sentences = data.split('\n')
	sentences = [ ' '.join(['<sen_BEG>/<sen_BEG>',each.strip(), '<sen_END>/<sen_END>']) for each in sentences if each.strip() != '' ]
	sentences = [ [every.split('/') for every in each.split(' ')] for each in sentences]
	for sentence in sentences:
		for wordtagpair in sentence:
			wordtagpair[0].lower()	
			wordtagpair[1].lower()	
	return sentences

def preprocess(data):
	global V, transition, context, emission
	sentences = parse(data)		
	for sentence in sentences:
		for word in sentence:
			V.add(word[0])
			TAG_SET.add(word[1])
	
	
	for sentence in sentences:
		tag_gram = ('<sen_BEG>', sentence[0][0])
		transition[tag_gram] = transition.get(tag_gram, 0) + 1		
		i = 1		
		while i < len(sentence):
			tag_gram = (sentence[i-1][1], sentence[i][1])		
			transition[tag_gram] = transition.get(tag_gram, 0) + 1
			i += 1
	
	for sentence in sentences:		
		context['<sen_BEG>'] = context.get('<sen_BEG>', 0) + 1
		for word in sentence:
			context[word[1]] = context.get(word[1], 0) + 1
	
	for sentence in sentences:
		for word in sentence:
			word_gram = (word[1], word[0])
			emission[word_gram] = emission.get(word_gram, 0) + 1
	
	return sentences

if __name__ == "__main__":
	# if len(sys.argv) != 3:
	# 	'Usage: python hmm.py train.data test.data'
	# 	sys.exit(0)
	
#TRAINING THE MODEL
	# f = open(sys.argv[1], 'r')
	f=open("training.data","r")
	data = f.read()
	sentences = preprocess(data)			
	
#TESTING THE MODEL
	TAG_LIST = list(TAG_SET)
	# f1 = open(sys.argv[2], 'r')
	f1=open("testing.data","r")
	test_data = f1.read()		
	test_sentences = parse(test_data)
	test_sentences = test_sentences
	
	for sent in test_sentences:
		for x,y in sent:
			print y,
		print 
		token_accuracy = 0					
		result = viterbi(sent)
		print ' '.join(result)
		print ('\n')
		match =0 
		total = len(sent)
		i=0

		for i in range(len(sent)-1):			
			if (sent[i][1]==result[i]):
			 	match=match+1

		print (match/total)*100
		



