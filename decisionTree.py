import csv
import os
import sys

playerClassArray = []
typeArray = []
costArray = []
healthArray = []
rarityArray = []
collectibleArray = []

simulatedCollectiblePlayerClassArray = []
simulatedCollectibleTypeArray = []
simulatedCollectibleCostArray = []
simulatedCollectibleHealthArray = []
simulatedCollectibleRarityArray = []
simulatedCollectibleArray = []

simulatedNormalPlayerClassArray = []
simulatedNormalTypeArray = []
simulatedNormalCostArray = []
simulatedNormalHealthArray = []
simulatedNormalRarityArray = []
simulatedNormalArray = []


def openFile(fileLocation):
	file = open(fileLocation)
	reader = csv.DictReader(file)
	return reader

def writeArrays():
	for row in csvFile:
		playerClassArray.append(row['playerClass'])
		typeArray.append(row['type'])
		costArray.append(row['cost'])
		healthArray.append(row['health'])
		rarityArray.append(row['rarity'])
		collectibleArray.append(row['collectible'])

def decisionTree():
	i = 0
	while(i < len(playerClassArray)):
		runThroughDecisionTree(i)
		i = i + 1

def runThroughDecisionTree(index):
	depth1(index)

def depth1(index):
	if(rarityArray[index] == 'RARE'):
		pushToCollectible(index)
	elif(rarityArray[index] == 'LEGENDARY'):
		depth2Legendary(index)
	else:
		depth2Common(index)

def depth2Legendary(index):
	if(healthArray[index] == '0' or healthArray[index] == '1...5'):
		pushToCollectible(index)
	else:
		pushToNormal(index)

def depth2Common(index):
	if(playerClassArray[index] == 'PHYSICAL'):
		pushToNormal(index)
	elif(playerClassArray[index] == 'MAGIC'):
		depth3Magic(index)
	else:
		depth3Neutral(index)

def depth3Magic(index):
	if(costArray[index] == '0'):
		pushToNormal(index)
	else:
		pushToCollectible(index)

def depth3Neutral(index):
	if(healthArray[index] == '0' or healthArray[index] == '1...5'):
		pushToNormal(index)
	else:
		pushToCollectible(index)

def confusionMatrix():
	truePositive = 0
	trueNegative = 0
	falsePositive = 0
	falseNegative = 0
	i = 0
	j = 0
	while(i < len(simulatedCollectibleArray)):
		if(simulatedCollectibleArray[i] == 'TRUE'):
			truePositive = truePositive + 1
		else:
			falsePositive = falsePositive + 1
		i = i + 1

	while(j < len(simulatedNormalArray)):
		if(simulatedNormalArray[j] == 'FALSE'):
			trueNegative = trueNegative + 1
		else:
			falseNegative = falseNegative + 1
		j = j + 1
	accuracy = (truePositive + trueNegative)/(trueNegative + truePositive + falseNegative + falsePositive)
	print("True Positive", truePositive)
	print("False Positive", falsePositive)
	print("True Negative", trueNegative)
	print("False Negative", falseNegative)
	print("Accuracy", accuracy)

def pushToCollectible(index):
	simulatedCollectiblePlayerClassArray.append(playerClassArray[index])
	simulatedCollectibleTypeArray.append(typeArray[index])
	simulatedCollectibleCostArray.append(costArray[index])
	simulatedCollectibleHealthArray.append(healthArray[index])
	simulatedCollectibleRarityArray.append(rarityArray[index])
	simulatedCollectibleArray.append(collectibleArray[index])

def pushToNormal(index):
	simulatedNormalPlayerClassArray.append(playerClassArray[index])
	simulatedNormalTypeArray.append(typeArray[index])
	simulatedNormalCostArray.append(costArray[index])
	simulatedNormalHealthArray.append(healthArray[index])
	simulatedNormalRarityArray.append(rarityArray[index])
	simulatedNormalArray.append(collectibleArray[index])


csvFile = openFile(os.path.join(sys.path[0], 'TrainingData.csv'))
writeArrays()
decisionTree()
confusionMatrix()