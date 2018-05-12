#!/usr/bin/python
import sys
from string import punctuation
import re, itertools,math
import codecs,operator
import matplotlib.pyplot as plt
import numpy as np
# import plotly.plotly as py

skip=[0,1,6,10]
tokens=[]
dict_ngram={}
sorted_tuple={}

def create_regexp(): 
	regexp = {}
	smileys = """<3 :D :-D :) :-) :P :-P :-E >-) :( :-( :-< :P :-O :-* :-@ :'( :-$ :-\ :-# (((H))) :-X `:-) :^)
	 :-& E-:-) <:-) :-> (-}{-) :-Q $_$ @@ :-! :-D :*) :@ :-@ :-0 :-----) %-( :-.) :-($) (:I     |-O :@)
	  <(-_-)> d[-_-]b ~:0 -@--@- \VVV/ \%%%/ :-# :'-)
	{:-) ;) ;-) O:-) O*-) |-O (:-D @>--;-- @-}--- =^.^= O.o \_/) (o.o) (___)0 ~( 8^(I)"""
	regexp['abbv']=re.compile(r'(?:[A-Z]\.)+')
	regexp['web']=re.compile(r"(www.[a-zA-Z]+.[a-zA-Z]+)")
	regexp['email'] = re.compile( r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)" )
	regexp['url'] = re.compile( "(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)" )
	regexp['word'] = re.compile( "([A-Za-z0-9\-_]+(\'[A-Za-z][A-Za-z]?)?)\'?" )
	regexp['smileys'] = re.compile( "|".join( map(re.escape,smileys.split()) ) )
	regexp['emoji'] = re.compile(u'(['
									    u'\U0001F300-\U0001F64F'
									    u'\U0001F680-\U0001F6FF'
									    u'\u2600-\u26FF\u2700-\u27BF])', 
									    re.UNICODE)
	regexp['time'] = re.compile(r"\d{1,2}:\d{2}(?::\d{2})?\s*(?:AM|PM|am|pm)?")
	regexp['mentions'] = re.compile( r"(@\w+)" )
	regexp['tags'] = re.compile( r"(#[A-Za-z0-9]+)" )
	regexp['ellipses'] = re.compile( r"\.\.\.$" )
	regexp['punction'] = re.compile( "|".join( [re.escape(c) for c in punctuation] ) )
	regexp_list = [regexp['email'], regexp['url'], regexp['web'], regexp['abbv'], regexp['time'], regexp['word'],
					regexp['smileys'], regexp['emoji'],
					regexp['mentions'], regexp['tags'], regexp['ellipses'], regexp['punction']]
	return regexp_list

def tokenizer(data,regexp_list):
	lines=data.split("\n")
	for word in lines:
		word=word.strip()
		# print word
		while len(word)!=0:
			patternflag=0
			count=0
			for regexp in regexp_list:
				temp=regexp.match(word)
				if temp is not None:
					patternflag=1
					if count not in skip:
						tokens.append(temp.group())
					word=word[temp.end():].strip()
					break
				count+=1
			if patternflag==0:
				temp=re.match( r"^(.*?) ",word)
				if temp is None:
					tokens.append(word[0])
					word=word[1:].strip()
					break
				else:
					tokens.append(word[:temp.end()-1])
					word=word[temp.end():].strip()
	# tokens.append('</s>')
	# return tokens
def ngram():

	unigram={}
	bigram={}
	trigram={}
	quadgram={}
	pentagram={}
	hexagram={}

	for i in tokens:
		if(unigram.has_key(i)):
			unigram[i]=unigram.get(i)+1
		else:
			unigram[i]=1

	for i in range(len(tokens)-1):
		temp=tokens[i]+tokens[i+1]
		# bigram.append(temp)
		if(bigram.has_key(temp)):
			bigram[temp]=bigram.get(temp)+1
		else:
			bigram[temp]=1

	for i in range(len(tokens)-2):
		temp=tokens[i]+tokens[i+1]+tokens[i+2]
		# trigram.append(temp)
		if(trigram.has_key(temp)):
			trigram[temp]=trigram.get(temp)+1
		else:
			trigram[temp]=1

	for i in range(len(tokens)-3):
		temp=tokens[i]+tokens[i+1]+tokens[i+2]+tokens[i+3]
		# quadgram.append(temp)
		if(quadgram.has_key(temp)):
			quadgram[temp]=quadgram.get(temp)+1
		else:
			quadgram[temp]=1

	for i in range(len(tokens)-4):
		temp=tokens[i]+tokens[i+1]+tokens[i+2]+tokens[i+3]+tokens[i+4]
		# pentagram.append(temp)
		if(pentagram.has_key(temp)):
			pentagram[temp]=pentagram.get(temp)+1
		else:
			pentagram[temp]=1

	for i in range(len(tokens)-5):
		temp=tokens[i]+tokens[i+1]+tokens[i+2]+tokens[i+3]+tokens[i+4]+tokens[i+5]
		# hexagram.append(temp)
		if(hexagram.has_key(temp)):
			hexagram[temp]=hexagram.get(temp)+1
		else:
			hexagram[temp]=1
	dict_ngram[1]=unigram
	dict_ngram[2]=bigram
	dict_ngram[3]=trigram
	dict_ngram[4]=quadgram
	dict_ngram[5]=pentagram
	dict_ngram[6]=hexagram
	sorted_tuple[1]=sorted(dict_ngram[1].items(),key=operator.itemgetter(1),reverse=True)
	sorted_tuple[2]=sorted(dict_ngram[2].items(),key=operator.itemgetter(1),reverse=True)
	sorted_tuple[3]=sorted(dict_ngram[3].items(),key=operator.itemgetter(1),reverse=True)
	sorted_tuple[4]=sorted(dict_ngram[4].items(),key=operator.itemgetter(1),reverse=True)
	sorted_tuple[5]=sorted(dict_ngram[5].items(),key=operator.itemgetter(1),reverse=True)
	sorted_tuple[6]=sorted(dict_ngram[6].items(),key=operator.itemgetter(1),reverse=True)

def graph_create(i,n):
	xcord=[]
	ycord=[]
	if i==1:
		c='y'
		l='Author: Aristophanes'
	elif i==2:
		c='r'
		l='Author: Aristotle'
	elif i==3:
		c='b'
		l='Author: Caius Julius Caesar'
	elif i==4:
		c='g'
		l='Author: Marcus Tullius Cicero'
	else:
		c='black'
		l='Author: Horace'
	temp=sorted_tuple[n]
	for i in range(len(temp)):
		xcord.append(math.log(i+1))
		ycord.append(math.log(temp[i][1]))
	plt.plot(xcord,ycord,c,label=l)

def main():
	regexp_list=create_regexp()
	print "enter the n:"
	n=input()
	for j in range(1,6):
		lines = codecs.open('data'+str(j)+'.txt', encoding='utf-8')
		for line in lines:
			tokenizer(line,regexp_list)
		ngram()
		# print tokens
		# for i in range(1,7):
		graph_create(j,n)
		if (n==1):
			plt.title("UNIGRAM")
		elif (n==2):
			plt.title("BIGRAM")
		elif (n==3):
			plt.title("TRIGRAM")
		elif (n==4):
			plt.title("QUADGRAM")
		elif (n==5):
			plt.title("PENTAGRAM")
		else:
			plt.title("HEXAGRAM")
		
		del tokens[:]
	plt.legend()
	plt.show()
		# dict_ngram.clear()
		# sorted_tuple.clear()
main()