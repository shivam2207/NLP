#!/usr/bin/python
import sys
from string import punctuation
import re, itertools
import codecs

def create_regexp(): 
	regexp = {}
	smileys = """<3 :D :-D :) :-) :P :-P :-E >-) :( :-( :-< :P :-O :-* :-@ :'( :-$ :-\ :-# (((H))) :-X `:-) :^)
	 :-& E-:-) <:-) :-> (-}{-) :-Q $_$ @@ :-! :-D :*) :@ :-@ :-0 :-----) %-( :-.) :-($) (:I     |-O :@)
	  <(-_-)> d[-_-]b ~:0 -@--@- \VVV/ \%%%/ :-# :'-)
	{:-) ;) ;-) O:-) O*-) |-O (:-D @>--;-- @-}--- =^.^= O.o \_/) (o.o) (___)0 ~( 8^(I)"""
		
	regexp['email'] = re.compile( r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)" )
	regexp['url'] = re.compile( "(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)" )
	regexp['word'] = re.compile( "([A-Za-z0-9\-_]+(\'[A-Za-z][A-Za-z]?)?)\'?" );
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

	regexp_list = [ regexp['email'], regexp['url'], regexp['word'], 
					regexp['smileys'], regexp['emoji'],
					regexp['mentions'], regexp['tags'], regexp['ellipses'], 
					regexp['punction']]
	return regexp_list

def tokenizer(data,regexp_list):
	tokens=[]
	lines=data.split("\n")
	for word in lines:
		word=word.strip()
		while len(word)!=0:
			patternflag=0
			for regexp in regexp_list:
				temp=regexp.match(word)
				if temp is not None:
					patternflag=1
					tokens.append(temp.group())
					word=word[temp.end():].strip()
					break
			if patternflag==0:
				temp=re.match( r"^(.*?) ",word)
				if temp is None:
					tokens.append(word[0])
					word=word[1:].strip()
					break
				else:
					tokens.append(word[:temp.end()-1])
					word=word[temp.end():].strip()
	return tokens

def main():
	regexp_list=create_regexp()
	lines = codecs.open('tweeter_data.txt', encoding='utf-8')
	fp=open("tokens.txt","w")
	for line in lines:
		tokens =str(tokenizer(line,regexp_list)).strip()
		tokens =str(tokens).strip('[]')
		if len(tokens)!=0:
			# print str(tokens)
			fp.write(str(tokens))
			fp.write("\n")
main()