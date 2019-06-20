# -*- coding: utf-8 -*-

import re
import codecs
import os
import pandas
import sys
import operator
from nltk.corpus import stopwords
from word2vec_cosine import Word2vecExtractor
from sklearn.metrics.pairwise import cosine_similarity

W2vecextractor=Word2vecExtractor("/home/geet/dialogue_systems/data/GoogleNews-vectors-negative300.bin") 

def getdict1():
	'''
	:return: returns a dictionary for text normalization
	'''
	dict_file1 = os.path.join('resources', 'emnlp2012-lexnorm', 'emnlp_dict.txt')
	dict1 = {}
	with open(dict_file1, "r") as fh:
		for line in fh:
			line = line.split("\t")
			dict1[line[0]] = line[1]
	return dict1

def getdict2():
	'''
	:return: returns a dictionary for text normalization
	'''
	dict_file2 = os.path.join('resources', 'Test_Set_3802_Pairs.txt')
	dict2 = {}
	with open(dict_file2, "r") as fh:
		for line in fh:
			line = line.split("\t")
			new_line = line[1].split(" | ")
			dict2[new_line[0]] = new_line[1]
	return dict2

dict1 = getdict1()
dict2 = getdict2()
en_stop = set(stopwords.words('english'))

def normalize_text(text):
	'''
	:param text: the tweet text to be normalized
	:return: normalized version of the tweet after stopword removal
	 '''
	normalized_text = []
	
	for i in range(0, len(text)):
		text[i] = text[i].lower()
		if text[i] not in en_stop:
			if(text[i] in dict1):
				normalized_text.append(dict1[text[i]])
			elif(text[i] in dict2):
				normalized_text.append(dict2[text[i]])
			else:
				normalized_text.append(text[i])
	return " ".join(normalized_text)
	
def preprocess(text):
	'''
	:param text: the tweet text to be preprocessed
	:return: preprocessed version of the tweet; removes all URLs and html tags, removes @ from mentions, gets rid of trailing hashtags. It also normalizes the tokens based on two dictionaries, and removes stopwords
	 '''
	text = str(text)
	text = re.sub(r'<[^>]+>', "", text) # regex for html
	regex_url = regex = "(?:https?)(:\/\/)?[\n\S]+" # regex for URLs
	text = re.sub(regex_url, "", text) # regex for URLs
	text = re.sub(r"^@| @|.@", " ", text) # remove @ from mentions
	
	text = text.split()
	
	i = len(text)-1
	
	while(i > 0):		#remove trailing hashtags
		if(text[i][0] == "#"):
			i = i-1
			continue
		else:
			break
	preprocessed_text = text[:i]
	return (normalize_text(preprocessed_text))

def get_emotion(text):
	'''
	:param text: the tweet text
	:return: a sorted dictionary of 6 emotions and the cosine distance of the tweet from each emotion
	 '''
	vec_rep=W2vecextractor.sent2vec(text)
	scores_dict = {}

	for item in W2vecextractor.emotions_dict.keys():
		scores_dict.update({item:cosine_similarity(vec_rep, W2vecextractor.emotions_dict[item])})

	sorted_dict = sorted(scores_dict.items(), key=operator.itemgetter(1))
	return(sorted_dict[0][0])


def create_preprocessed_file(filename):
	'''
	:param filename: the input file containing tweets in a csv file with column named "Tweet_text" containing tweets. A file containing the preprocessed tweets is created, with same filename as input filename, but appended with -preprocessed
	'''

	print(filename)

	if(filename in {"data/merged.csv"}):
		print("Merged condition true")
		df1 = pandas.read_csv("data/conservative-preprocessed.csv")
		df2 = pandas.read_csv("data/gap-preprocessed.csv")
		df3 = pandas.read_csv("data/impact-preprocessed.csv")
		df4 = pandas.read_csv("data/leader-preprocessed.csv")
		df5 = pandas.read_csv("data/marriage-preprocessed.csv")
		df6 = pandas.read_csv("data/maternity-preprocessed.csv")
		df7 = pandas.read_csv("data/politicians-preprocessed.csv")
		df8 = pandas.read_csv("data/talkpay-preprocessed.csv")
		frames = [df1, df2, df3, df4, df5, df6, df7, df8]
		df = pandas.concat(frames)
		#df['Tweet_text'] = df['Tweet_text'].apply(preprocess)

	else:
		with open(filename, "r") as fh:
		#with codecs.open(filename, 'r', decoding='UTF-8') as fh:
			df = pandas.read_csv(fh)
			df['emotion'] = df['Tweet_text'].apply(get_emotion)
			df['Tweet_text'] = df['Tweet_text'].apply(preprocess)
			
	
	with open(filename.split(".")[0] + "-preprocessed.csv", 'w') as nfh:
		df.to_csv(nfh)
	print("Preprocessed file created in: "+filename.split(".")[0]+"-preprocessed.csv")
	return df


if __name__=='__main__':
	
	filename = "data/conservative.csv"
	create_preprocessed_file(filename)
