import csv
import numpy
from scipy import stats
import math
import os
import sys

playerClassArray = []
typeArray = []
costArray = []
healthArray = []
rarityArray = []
collectibleArray = []

def openFile(fileLocation):
	file = open(fileLocation)
	reader = csv.DictReader(file)
	return reader

def writeArrays():
	for row in csvFile:
		playerClassArray.append(row['playerClass'])
		typeArray.append(row['type'])
		costArray.append(int(row['cost']))
		healthArray.append(int(row['health']))
		rarityArray.append(row['rarity'])
		collectibleArray.append(row['collectible'])

def findMinimum(data):
	data.sort()
	return data[0]

def findMaximum(data):
	data.sort()
	return data[len(data)-1]

def findMedian(data):
	data.sort()
	if len(data) % 2 == 0:
		return (data[math.ceil(len(data)/2)] + data[math.ceil(len(data)/2 - 1)])/2
	else:
		return data[math.ceil(len(data)/2)]

def findMode(data):
	print(stats.mode(data))

def findMean(data):
	total = 0
	for datum in data:
		total = total + datum
	mean = total/(len(data))
	return mean

def findstddev(data):
	mean = findMean(data)
	toptotal = sum([(datum - mean)**2 for datum in data])
	bottomtotal = len(data)
	innertotal = toptotal/bottomtotal
	stddev = math.sqrt(innertotal)
	return stddev

def getCounts(data):
	unique, counts = numpy.unique(data, return_counts=True)
	return dict(zip(unique, counts))

csvFile = openFile(os.path.join(sys.path[0], 'hearthstoneCards.csv'))
writeArrays()
print('***********************************************************************')
print('PLAYERCLASS')
print("Count: ", getCounts(playerClassArray))
print('***********************************************************************')

print('COLLECTIBLE')
print("Count: ", getCounts(collectibleArray))
print('***********************************************************************')

print('RARITY')
print("Count: ", getCounts(rarityArray))
print('***********************************************************************')

print('TYPE')
print("Count: ", getCounts(typeArray))
print('***********************************************************************')

print('HEALTH')
print("Mean", findMean(healthArray))
print("Median: ", findMedian(healthArray))
print("Mode: ", findMode(healthArray))
print("Maximum Value: ", findMaximum(healthArray))
print("Minimum Value: ", findMinimum(healthArray))
print("Standard Deviation: ", findstddev(healthArray))
print('***********************************************************************')

print('COST')
print("Mean: ", findMean(costArray))
print("Median: ", findMedian(costArray))
print("Mode: ", findMode(costArray))
print("Maximum Value: ", findMaximum(costArray))
print("Minimum Value: ", findMinimum(costArray))
print("Standard Deviation: ", findstddev(costArray))
print('***********************************************************************')



