import csv
import numpy
import math
import os
import sys

playerClassArray = []
typeArray = []
costArray = []
healthArray = []
rarityArray = []
collectibleArray = []

collectiblePlayerClassArray = []
collectibleTypeArray = []
collectibleCostArray = []
collectibleHealthArray = []
collectibleRarityArray = []


def openFile(fileLocation):
	file = open(fileLocation)
	reader = csv.DictReader(file)
	return reader

def writeArrays(csvFile):
	clearArrays()
	for row in csvFile:
		playerClassArray.append(row['playerClass'])
		typeArray.append(row['type'])
		costArray.append(row['cost'])
		healthArray.append(row['health'])
		rarityArray.append(row['rarity'])
		collectibleArray.append(row['collectible'])

def clearArrays():
	playerClassArray =  []
	typeArray = []
	costArray = []
	healthArray = []
	rarityArray = []
	collectibleArray = []

	collectiblePlayerClassArray = []
	collectibleTypeArray = []
	collectibleCostArray = []
	collectibleHealthArray = []
	collectibleRarityArray = []

def makeDecisionTree():
	getCollectible()
	#We now have our root; the attribute with the largest information gain is rarity
	#remove cards with rare rarity, as, from the data, we know they are all collectible
	getSpecific("RARE", rarityArray)
	#remove cards with common rarity so that we can focus soley on cards with legendary rarity
	getSpecific("COMMON", rarityArray)
	#We see that health has a large information gain, so we look at the data
	getCollectible()
	print(getCounts(healthArray))
	print(getCounts(collectibleHealthArray))
	#We see that all cards with 1...5 or 0 health are collectible, and all cards with >5 health are not collectible
	#We have now completed the decision tree for legendary and rare rarities, and now only need to focus on common cards
	csvFile = openFile(os.path.join(sys.path[0], 'TrainingData.csv'))
	writeArrays(csvFile)
	getSpecific("RARE", rarityArray)
	getSpecific("LEGENDARY", rarityArray)
	getCollectible()
	#we see that playerClass gives us our highest data gain
	print(getCounts(playerClassArray))
	print(getCounts(collectiblePlayerClassArray))
	#we see that all common cards with playerClass physical are not collectible
	#get rid of physical cards
	getSpecific("PHYSICAL", playerClassArray)
	#focus on magic cards for now, so get rid of neutral cards
	getSpecific("NEUTRAL", playerClassArray)
	getCollectible()
	#We see that cost gives us the biggest data gain
	print(getCounts(costArray))
	print(getCounts(collectibleCostArray))
	#we see that none of the cards with 0 cost are collectible, all cards with cost >5 are collectible, and the
	#overwhelming majority of cards with 1...5 health are collectible
	#now we look at neutral cards
	csvFile= openFile(os.path.join(sys.path[0], 'TrainingData.csv'))
	writeArrays(csvFile)
	getSpecific("RARE", rarityArray)
	getSpecific("LEGENDARY", rarityArray)
	getSpecific("MAGIC", playerClassArray)
	getSpecific("PHYSICAL", playerClassArray)
	getCollectible()
	#We see that health is our biggest information gain
	print(getCounts(healthArray))
	print(getCounts(collectibleHealthArray))
	#We see that the overwhelming majority of cards with 0 and 1...5 health are not collectible, and
	# the overwhelming majority of cards with >5 health are collectible
	#Thus, the tree is complete

def getSpecific(attribute, array):
	i = len(playerClassArray)-1
	while(i >= 0):
		if(array[i] == attribute):
			playerClassArray.pop(i)
			costArray.pop(i)
			healthArray.pop(i)
			typeArray.pop(i)
			collectibleArray.pop(i)
			rarityArray.pop(i)
		i = i - 1

def getCollectible():
	playerClassInfoGain = informationGain(collectiblePlayerClassArray, playerClassArray)
	typeInfoGain = informationGain(collectibleTypeArray, typeArray)
	costInfoGain = informationGain(collectibleCostArray, costArray)
	healthInfoGain = informationGain(collectibleHealthArray, healthArray)
	rarityInfoGain = informationGain(collectibleRarityArray, rarityArray)

	print("playerClass", playerClassInfoGain)
	print("Type", typeInfoGain)
	print("Cost", costInfoGain)
	print("Health", healthInfoGain)
	print("Rarity", rarityInfoGain)

def informationGain(collectible, total):
	i = 0
	collectible.clear()
	while(i < len(total)):
		if(collectibleArray[i] != 'FALSE'):
			collectible.append(total[i])
		i = i + 1
	return info(len(collectible), len(total) - len(collectible)) - informationNeeded(total, collectible)

def info(collectible, normal):
	collectibleProbability = collectible/(collectible + normal)
	normalProbability = 1 - collectibleProbability
	if(collectible == 0 or normal == 0):
		return 0
	else:
		return -collectibleProbability*math.log(collectibleProbability, 2) - normalProbability*math.log(normalProbability, 2)

def informationNeeded(total, collectible):
	collectibleCount = getCounts(collectible)
	totalCount = getCounts(total)
	infoa = 0
	i = 0
	for count in totalCount:
		if(count in collectible):
			infoa = infoa + int(totalCount[count])/len(collectibleArray) * info(int(collectibleCount[count]), int(totalCount[count]) - int(collectibleCount[count]))
		i = i + 1
	return infoa

def getCounts(data):
	unique, counts = numpy.unique(data, return_counts=True)
	return dict(zip(unique, counts))

csvFile = openFile(os.path.join(sys.path[0], 'TrainingData.csv'))
writeArrays(csvFile)
makeDecisionTree()
