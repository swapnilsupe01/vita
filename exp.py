# Python 3.12.1 (tags/v3.12.1:2305ca5, Dec  7 2023, 22:03:25) [MSC v.1937 64 bit (AMD64)] on win32
# Type "help", "copyright", "credits" or "license()" for more information.
import csv
import json, pickle
import sys
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from prettytable import PrettyTable
def readData(fileName):
data = []
file = open(fileName, "r")
data = file.read()
file.close()
return data
def preProcessData(data):
data = data.lower()
data = data.translate(str.maketrans("", "", string.punctuation.replace(".", "")))
data = data.replace(".", " eos ")
stop_words = set(stopwords.words("english"))
data = word_tokenize(data)
data = [word for word in data if word not in stop_words]
return data
def createBigram(data):
listOfBigrams = []
bigramCounts = {}
unigramCounts = {}
nbyn = {}
for i in range(len(data)):
if i < len(data) - 1:
listOfBigrams.append((data[i], data[i + 1]))
if (data[i], data[i + 1]) in bigramCounts:
bigramCounts[(data[i], data[i + 1])] += 1
else:
bigramCounts[(data[i], data[i + 1])] = 1
if data[i] in unigramCounts:
unigramCounts[data[i]] += 1
else:
unigramCounts[data[i]] = 1
return listOfBigrams, unigramCounts, bigramCounts
def calcBigramProb(listOfBigrams, unigramCounts, bigramCounts):
listOfProb = {}
for bigram in listOfBigrams:
word1 = bigram[0]
word2 = bigram[1]
listOfProb[bigram] = (bigramCounts.get(bigram)) / (unigramCounts.get(word1))
return listOfProb
def addOneSmothing(listOfBigrams, unigramCounts, bigramCounts):
listOfProb = {}
wordCounts = {}
for bigram in listOfBigrams:
word1 = bigram[0]
word2 = bigram[1]
listOfProb[bigram] = (bigramCounts.get(bigram) + 1) / (
unigramCounts.get(word1) + len(unigramCounts)
)
wordCounts[bigram] = (
(bigramCounts[bigram] + 1)
* unigramCounts[word1]
/ (unigramCounts[word1] + len(unigramCounts))
)
return listOfProb, wordCounts
if __name__ == "__main__":
data = readData("train_corpus.txt")
... data = preProcessData(data)
... listOfBigrams, unigramCounts, bigramCounts = createBigram(data)
... bigramProb = calcBigramProb(listOfBigrams, unigramCounts, bigramCounts)
... bigramAddOne, addOneCstar = addOneSmothing(
... listOfBigrams, unigramCounts, bigramCounts
... )
... input = input("Enter the sentence: ")
... inputList = []
... outputProb1 = 1
... outputProb2 = 1
... inputList.append("eos")
... for i in range(len(input.split())):
... inputList.append(input.split()[i])
... x = PrettyTable()
... field_names = [" "]
... field_names.extend(inputList)
... x.field_names = field_names
... for i in range(len(inputList)):
... list = []
... list.append(inputList[i])
... for j in range(len(inputList)):
... if (inputList[i], inputList[j]) in bigramProb:
... list.append(bigramProb.get((inputList[i], inputList[j])))
... outputProb1 *= bigramProb.get((inputList[i], inputList[j]))
... else:
... list.append(0)
... outputProb1 *= 0
... x.add_row(list)
... print("\nThe Probabilities of the Bigram Model are: ")
... print(x)
... print("The Probability of the Bigram Model is: ", outputProb1)
... y = PrettyTable()
... y.field_names = field_names
... for i in range(len(inputList)):
... list = []
... list.append(inputList[i])
... for j in range(len(inputList)):
... if (inputList[i], inputList[j]) in bigramAddOne:
... list.append(bigramAddOne.get((inputList[i], inputList[j])))
... outputProb2 *= bigramAddOne.get((inputList[i], inputList[j]))
else:
if inputList[i] not in unigramCounts:
unigramCounts[inputList[i]] = 1
prob = (1) / (unigramCounts[inputList[i]] + len(unigramCounts))
addOneCStar = (
1
* unigramCounts[inputList[i]]
/ (unigramCounts[inputList[i]] + len(unigramCounts))
)
outputProb2 *= prob
list.append(prob)
y.add_row(list)
print("\nThe Probabilities of the Add One Smoothing Model are: ")
print(y)
