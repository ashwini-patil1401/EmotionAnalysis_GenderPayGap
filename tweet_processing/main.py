import pandas
import preprocess
import topicmodel
import sys

def getTopics(data, modelName, numTopics, numWords, filename):
	'''
	:param data: the data, 
	:modelName: the topic modeling algorithm LDA
	:param numTopics: number of topics, 
	:param numWords: number of words to be returned for each topic
	:return: returns numWords number of words for each topic
	'''
	return topicmodel.runLDA(data, numTopics, numWords, filename)

def getEmotionPercentage(df, filename):
	result = df["emotion"].value_counts(sort=True, ascending=False, dropna=True)
	result = (result/sum(result))*100.0
	result.columns = ["Emotion", "Percentage"]
	
	with open(filename.split(".")[0] + "-emotions.csv", 'w') as nfh:
		result.to_csv(nfh)
	print("Emotion analysis stored in: "+filename.split(".")[0]+"-emotions.csv")
	

if __name__ == "__main__":

	#filename = "new_data/conservative.csv"
	#filename = "new_data/gap.csv"
	#filename = "new_data/impact.csv"
	#filename = "new_data/leader.csv"
	#filename = "new_data/marriage.csv"
	#filename = "new_data/maternity.csv"
	#filename = "new_data/politicians.csv"
	#filename = "new_data/talkpay.csv"
	filename = "new_data/merged.csv"
	df = preprocess.create_preprocessed_file(filename)

	getEmotionPercentage(df, filename)

	'''modelName = "LDA"
	numTopics = 3
	numWords = 10

	numTopics = raw_input("Choose number of topics K:")
	numWords = raw_input("Choose number of top words to display for each topic:")
	
	getTopics(df, modelName, int(numTopics), int(numWords), filename)
	'''
	
	
