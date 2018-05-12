#!/usr/bin/python
import sys
from string import punctuation
import re, itertools
import codecs,operator
import matplotlib.pyplot as plt
import numpy as np
# import plotly.plotly as py

skiplist=[]
data=[]
skip=[1,8]
unigram_dict={}
bigram_dict={}
trigram_dict={}
quadgram_dict={}
pentagram_dict={}
hexagram_dict={}
sorted_tuple_dict={}
def create_regexp(): 
	regexp = {}
	smileys = """<3 :D :-D :) :-) :P :-P :-E >-) :( :-( :-< :P :-O :-* :-@ :'( :-$ :-\ :-# (((H))) :-X `:-) :^)
	 :-& E-:-) <:-) :-> (-}{-) :-Q $_$ @@ :-! :-D :*) :@ :-@ :-0 :-----) %-( :-.) :-($) (:I     |-O :@)
	  <(-_-)> d[-_-]b ~:0 -@--@- \VVV/ \%%%/ :-# :'-)
	{:-) ;) ;-) O:-) O*-) |-O (:-D @>--;-- @-}--- =^.^= O.o \_/) (o.o) (___)0 ~( 8^(I)"""

	regexp['email'] = re.compile( r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)" )
	regexp['url'] = re.compile( "(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)" )
	regexp['word'] = re.compile( "([A-Za-z0-9\-_]+(\'[A-Za-z][A-Za-z]?)?)\'?" )
	regexp['smileys'] = re.compile( "|".join( map(re.escape,smileys.split()) ) )
	regexp['emoji'] = re.compile(u'(['
									    u'\U0001F300-\U0001F64F'
									    u'\U0001F680-\U0001F6FF'
									    u'\u2600-\u26FF\u2700-\u27BF])', 
									    re.UNICODE)
	regexp['mentions'] = re.compile( r"(@\w+)" )
	regexp['tags'] = re.compile( r"(#[A-Za-z0-9]+)" )
	regexp['ellipses'] = re.compile( r"\.\.\.$" )
	regexp['punction'] = re.compile( "|".join( [re.escape(c) for c in punctuation] ) )
	regexp_list = [regexp['email'], regexp['url'], regexp['word'], regexp['smileys'], regexp['emoji'],
					regexp['mentions'], regexp['tags'], regexp['ellipses'], regexp['punction']]
	return regexp_list

def tokenizer(data,regexp_list):
	tokens=[]
	tokens.append('<s>')
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
	tokens.append('</s>')
	return tokens

def bigram_create():
	for i in range(len(data)):
		for j in range(len(data[i])-1):
			k=j+1
			temp=data[i][j]+" "+data[i][k]
			if bigram_dict.has_key(temp):
				bigram_dict[temp]=bigram_dict.get(temp)+1
			else:
				bigram_dict[temp]=1
def unigram_create():
	for i in range(len(data)):
		for j in range(len(data[i])):
			if(unigram_dict.has_key(data[i][j])):
				unigram_dict[data[i][j]]=unigram_dict.get(data[i][j])+1
			else:
				unigram_dict[data[i][j]]=1

def trigram_create():
	for i in range(len(data)):
		for j in range(len(data[i])-2):
			k=j+1
			l=j+2
			temp=data[i][j]+" "+data[i][k]+" "+data[i][l]
			if(trigram_dict.has_key(temp)):
				trigram_dict[temp]=trigram_dict.get(temp)+1
			else:
				trigram_dict[temp]=1

def quadgram_create():
	for i in range(len(data)):
		for j in range(len(data[i])-3):
			k=j+1
			l=j+2
			m=j+3
			temp=data[i][j]+" "+data[i][k]+" "+data[i][l]+" "+data[i][m]
			if(quadgram_dict.has_key(temp)):
				quadgram_dict[temp]=quadgram_dict.get(temp)+1
			else:
				quadgram_dict[temp]=1

def pentagram_create():
	for i in range(len(data)):
		for j in range(len(data[i])-4):
			k=j+1
			l=j+2
			m=j+3
			n=j+4
			temp=data[i][j]+" "+data[i][k]+" "+data[i][l]+" "+data[i][m]+" "+data[i][n]
			if(pentagram_dict.has_key(temp)):
				pentagram_dict[temp]=pentagram_dict.get(temp)+1
			else:
				pentagram_dict[temp]=1

def hexagram_create():
	for i in range(len(data)):
		for j in range(len(data[i])-5):
			k=j+1
			l=j+2
			m=j+3
			n=j+4
			p=j+5
			temp=data[i][j]+" "+data[i][k]+" "+data[i][l]+" "+data[i][m]+" "+data[i][n]+" "+data[i][p]
			if(hexagram_dict.has_key(temp)):
				hexagram_dict[temp]=hexagram_dict.get(temp)+1
			else:
				hexagram_dict[temp]=1

def funt(regexp_list):
	print "enter the text:"
	text=raw_input()
	tokenlist=tokenizer(text,regexp_list)
	tokenlist=tokenlist[::-1]
	print "probability for unigram:"
	temp=tokenlist[1]+" "+tokenlist[0]
	value=bigram_dict.get(temp,0)
	try:
		prob=float(value)/float(unigram_dict.get(tokenlist[1],0))
		print prob
	except ValueError:
		print "0"
	print "probability for bigram:"
	temp=tokenlist[1]+" "+tokenlist[0]
	value=bigram_dict.get(temp,0)
	prob=(float(value)+1.0)/(float(len(bigram_dict))+float(unigram_dict.get(tokenlist[1],0)))
	print prob
	print "probability for trigram:"
	temp=tokenlist[2]+" "+tokenlist[1]+" "+tokenlist[0]
	value=trigram_dict.get(temp,0)
	prob=(float(value)+1.0)/(float(len(trigram_dict))+float(bigram_dict.get(tokenlist[2]+tokenlist[1],0)))
	print prob
	print "probability for quadgram:"
	temp=tokenlist[3]+" "+tokenlist[2]+" "+tokenlist[1]+" "+tokenlist[0]
	temp2=tokenlist[3]+" "+tokenlist[2]+" "+tokenlist[1]
	value=quadgram_dict.get(temp,0)
	prob=(float(value)+1.0)/(float(len(quadgram_dict))+float(trigram_dict.get(temp2,0)))
	print prob
	print "probability for pentagram:"
	temp=tokenlist[4]+" "+tokenlist[3]+" "+tokenlist[2]+" "+tokenlist[1]+" "+tokenlist[0]
	temp2=tokenlist[4]+" "+tokenlist[3]+" "+tokenlist[2]+" "+tokenlist[1]
	value=pentagram_dict.get(temp,0)
	prob=(float(value)+1.0)/(float(len(pentagram_dict))+float(quadgram_dict.get(temp2,0)))
	print prob
	print "probability for hexagram:"
	temp=tokenlist[5]+" "+tokenlist[4]+" "+tokenlist[3]+" "+tokenlist[2]+" "+tokenlist[1]+" "+tokenlist[0]
	temp2=tokenlist[5]+" "+tokenlist[4]+" "+tokenlist[3]+" "+tokenlist[2]+" "+tokenlist[1]
	value=hexagram_dict.get(temp,0)
	prob=(float(value)+1.0)/(float(len(hexagram_dict))+float(pentagram_dict.get(temp2,0)))
	print prob

def create_graph(flag):
	if (flag==1):
		sorted_tuple=sorted(unigram_dict.items(),key=operator.itemgetter(1),reverse=True)
		sorted_tuple_dict[1]=sorted_tuple
	elif (flag==2):
		sorted_tuple=sorted(bigram_dict.items(),key=operator.itemgetter(1),reverse=True)
		sorted_tuple_dict[2]=sorted_tuple
	elif(flag==3):
		sorted_tuple=sorted(trigram_dict.items(),key=operator.itemgetter(1),reverse=True)
		sorted_tuple_dict[3]=sorted_tuple
	elif(flag==4):
		sorted_tuple=sorted(quadgram_dict.items(),key=operator.itemgetter(1),reverse=True)
		sorted_tuple_dict[4]=sorted_tuple
	elif(flag==5):
		sorted_tuple=sorted(pentagram_dict.items(),key=operator.itemgetter(1),reverse=True)
		sorted_tuple_dict[5]=sorted_tuple
	else:
		sorted_tuple=sorted(hexagram_dict.items(),key=operator.itemgetter(1),reverse=True)
		sorted_tuple_dict[6]=sorted_tuple
	# print sorted_tuple
	x_cord=[]
	y_cord=[]
	for i in range(len(sorted_tuple)):
		x_cord.append(i)
		y_cord.append(sorted_tuple[i][1])
	plt.plot(x_cord,y_cord);
	plt.show()

def sentence_generate_bia():
	st="<s>"
	curr="<s>"
	count=0
	while(count<=30):
		count+=1
		if (curr=="</s>"):
			break
		for i in sorted_tuple_dict[2]:
			l=i[0].split(" ")
			if(l[0]==curr):
				t=" "+l[1]
				curr=l[1]
				st=st+t
				break
	print st
	# print sorted_tuple_dict[2]
# def sentence_generate_bia1():
# 	# print sorted_tuple_dict[3]
# 	st=""
# 	curr="<s>"
# 	for i in sorted_tuple_dict[2]:
# 		l=i[0].split(" ")
# 		if(l[0]==curr):
# 			st=st+i[0]
# 			break
# 	curr=l[1]
# 	count=1
# 	while(count<20):
# 		count+=1
# 		cur=curr.split(" ")
# 		if (cur[0]=="</s>"):
# 			break
# 		for i in sorted_tuple_dict[2]:
# 			l=i[0].split(" ")
# 			if(l[0]==curr):
# 				t=" "+l[1]
# 				curr=l[1]
# 				st=st+t
# 				break
# 	print st

def sentence_generate_tri():
	# print sorted_tuple_dict[3]
	st=""
	curr="<s>"
	for i in sorted_tuple_dict[3]:
		l=i[0].split(" ")
		if(l[0]==curr):
			st=st+i[0]
			break
	curr=l[1]+" "+l[2]
	count=1
	while(count<=30):
		count+=1
		cur=curr.split(" ")
		if (cur[1]=="</s>"):
			break
		for i in sorted_tuple_dict[3]:
			l=i[0].split(" ")
			if(l[0]+" "+l[1]==curr):
				t=" "+l[2]
				curr=l[1]+" "+l[2]
				st=st+t
				break
	print st

def sentence_generate_quad():
	# print sorted_tuple_dict[3]
	st=""
	curr="<s>"
	for i in sorted_tuple_dict[4]:
		l=i[0].split(" ")
		if(l[0]==curr):
			st=st+i[0]
			break
	curr=l[1]+" "+l[2]+" "+l[3]
	count=1
	while(count<=30):
		count+=1
		cur=curr.split(" ")
		if (cur[2]=="</s>"):
			break
		for i in sorted_tuple_dict[4]:
			l=i[0].split(" ")
			if(l[0]+" "+l[1]+" "+l[2]==curr):
				t=" "+l[3]
				curr=l[1]+" "+l[2]+" "+l[3]
				st=st+t
				break
	print st

def sentence_generate_penta():
	# print sorted_tuple_dict[3]
	st=""
	curr="<s>"
	for i in sorted_tuple_dict[5]:
		l=i[0].split(" ")
		if(l[0]==curr):
			st=st+i[0]
			break
	curr=l[1]+" "+l[2]+" "+l[3]+" "+l[4]
	count=1
	while(count<=30):
		count+=1
		cur=curr.split(" ")
		if (cur[3]=="</s>"):
			break
		for i in sorted_tuple_dict[5]:
			l=i[0].split(" ")
			if(l[0]+" "+l[1]+" "+l[2]+" "+l[3]==curr):
				t=" "+l[4]
				curr=l[1]+" "+l[2]+" "+l[3]+" "+l[4]
				st=st+t
				break
	print st

def sentence_generate_hexa():
	# print sorted_tuple_dict[3]
	st=""
	curr="<s>"
	for i in sorted_tuple_dict[6]:
		l=i[0].split(" ")
		if(l[0]==curr):
			st=st+i[0]
			break
	curr=l[1]+" "+l[2]+" "+l[3]+" "+l[4]+" "+l[5]
	count=1
	while(count<=30):
		count+=1
		cur=curr.split(" ")
		if (cur[4]=="</s>"):
			break
		for i in sorted_tuple_dict[6]:
			l=i[0].split(" ")
			if(l[0]+" "+l[1]+" "+l[2]+" "+l[3]+" "+l[4]==curr):
				t=" "+l[5]
				curr=l[1]+" "+l[2]+" "+l[3]+" "+l[4]+" "+l[5]
				st=st+t
				break
	print st

def main():
	regexp_list=create_regexp()
	lines = codecs.open('tweeter_data.txt', encoding='utf-8')
	for line in lines:
		tokens =tokenizer(line,regexp_list)
		if len(tokens)!=0:
			data.append(tokens)
	unigram_create()
	bigram_create()
	trigram_create()
	quadgram_create()
	pentagram_create()
	hexagram_create()
	# funt(regexp_list)
	for i in range(1,7):
		create_graph(i)
	sentence_generate_bia()
	# sentence_generate_bia1()
	sentence_generate_tri()
	sentence_generate_quad()
	sentence_generate_penta()
	sentence_generate_hexa()

main()