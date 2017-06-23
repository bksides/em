import sys
import re

def wordCount(filename):
	f = open(filename, 'r')
	contents = f.read().lower()
	words = re.split("[\W\d_]+", contents)
	wordcount = {}
	for word in words:
		if word in wordcount:
			wordcount[word] += 1
		else:
			wordcount[word] = 1
	return wordcount

def aggregateWordCounts(countdict):
	excludefile = open("exclusion.txt", 'r')
	excludeList = re.split("\s+", excludefile.read())
	wordSet = set()
	print(str(countdict.keys()) + "\n")
	for wordcount in countdict.values():
		for word in wordcount:
			wordSet.add(word)
	wordSet = wordSet.difference(excludeList)
	print("Wordset: " + str(wordSet) + "\n")
	fileCoords = {}
	for filename in countdict:
		fileCoords[filename] = []
		for word in wordSet:
			if word in countdict[filename]:
				fileCoords[filename].append(countdict[filename][word])
			else:
				fileCoords[filename].append(0)
	return fileCoords


def main(argv):
	countdict = {}
	for arg in argv[1:]:
		countdict[arg] = wordCount(arg)
		print(arg + ": " + str(wordCount(arg)) + "\n")
	print(str(countdict) + "\n")
	print(str(aggregateWordCounts(countdict)) + "\n")

if __name__ == "__main__":
	main(sys.argv)