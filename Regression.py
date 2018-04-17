import csv
import os
import sys
import main
import math
import matplotlib.pyplot as plt
import numpy as np

def openFile(fileLocation):
	file = open(fileLocation)
	reader = csv.DictReader(file)
	return reader

def makeMatrix():
	healthArray = []
	costArray = []
	dataArray = [[0 for x in range(2)] for y in range(200)]
	for row in csvFile:
		healthArray.append(int(row['health']))
		costArray.append(int(row['cost']))

	healthArray = healthArray[:200]
	costArray = costArray[:200]

	i = 0
	while i < 200: #add first 200 values into dataArray
		dataArray[i][0] = costArray[i]
		dataArray[i][1] = healthArray[i]
		i = i + 1
	return dataArray



#Takes a matrix with two columns as input
#returns tuple with tuple[0] = w0 and tuple[1] = w1
def getSlopeValues(data):
	healthData = []
	costData = []
	i = 0
	while(i < len(data)):
		healthData.append(data[i][1])
		costData.append(data[i][0])
		i = i + 1
	averageHealth = main.findMean(healthData)
	averageCost = main.findMean(costData)

	j = 0
	top = 0
	bottom = 0
	while j < len(data):
		top = top + ((healthData[j] - averageHealth)*(costData[j] - averageCost))
		bottom = bottom + math.pow(healthData[j] - averageHealth, 2)
		j = j + 1
	w1 = top/bottom
	w0 = averageCost - (w1 * averageHealth)
	return (w0, w1)




def plotRegression(slopeValues, data):
	healthData = []
	costData = []
	i = 0
	while(i < len(data)):
		healthData.append(data[i][1])
		costData.append(data[i][0])
		i = i + 1
	plt.scatter(healthData, costData)
	plt.title('Health vs Cost')
	plt.xlabel('Health')
	plt.ylabel('Cost')
	x = np.arange(100)
	y = slopeValues[0] + slopeValues[1] * x
	plt.plot(x, y, c='red')
	plt.show()


csvFile = openFile(os.path.join(sys.path[0], 'hearthstoneCards.csv'))
data = makeMatrix()
slopeValues = getSlopeValues(data)
plotRegression(slopeValues, data)