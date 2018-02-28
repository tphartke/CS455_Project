import csv
import os
import random
import sys
import numpy as np
import matplotlib.pyplot as plt
import main

outputFile = open(os.path.join(sys.path[0], 'Project2_Output.csv'), 'w')
writer = csv.writer(outputFile)

cluster1 = []
cluster2 = []

previousCentroid1 = []
previousCentroid2 = []


def openFile(fileLocation):
	file = open(fileLocation)
	reader = csv.DictReader(file)
	return reader

def kmeans(data):
	matrix = makeMatrix(data)
	centroid1 = matrix[getRandomNumber()]
	centroid2 = matrix[getRandomNumber()]
	run = 1

	i = 0
	while i < len(matrix):
		if getDistance(centroid1, matrix[i]) <= getDistance(centroid2, matrix[i]):
			cluster1.append(matrix[i])
		else:
			cluster2.append(matrix[i])
		i = i + 1
	#outputResults(centroid1, centroid2, run)
	showPlot(cluster1, cluster2, centroid1, centroid2, run)



	previousCentroid1 = centroid1
	previousCentroid2 = centroid2

	centroid1 = getAverageValue(cluster1)
	centroid2 = getAverageValue(cluster2)

	while(previousCentroid1 != centroid1 and previousCentroid2 != centroid2):
		run = run + 1
		cluster1.clear()
		cluster2.clear()
		i = 0
		while i < len(matrix):
			if getDistance(centroid1, matrix[i]) <= getDistance(centroid2, matrix[i]):
				cluster1.append(matrix[i])
			else:
				cluster2.append(matrix[i])
			i = i + 1
		previousCentroid1 = centroid1
		previousCentroid2 = centroid2

		centroid1 = getAverageValue(cluster1)
		centroid2 = getAverageValue(cluster2)
		showPlot(cluster1, cluster2, centroid1, centroid2, run)
		#outputResults(centroid1, centroid2, run)


def showPlot(cluster1, cluster2, centroid1, centroid2, run):
	c1xdata = []
	c1ydata = []
	c2xdata = []
	c2ydata = []
	inc = "run"
	inc += str(run)
	inc += ".png"
	print(inc)
	i = 0
	while i < len(cluster1):
		c1xdata.append(cluster1[i][1])
		c1ydata.append(cluster1[i][0])
		i = i + 1

	j = 0
	while j < len(cluster2):
		c2xdata.append(cluster2[j][1])
		c2ydata.append(cluster2[j][0])
		j = j + 1

	plt.scatter(c1xdata, c1ydata, c="green")
	plt.scatter(c2xdata, c2ydata, c="blue")
	plt.scatter(centroid1[1], centroid1[0], s=np.pi*25, c="red")
	plt.scatter(centroid2[1], centroid2[0], s=np.pi*25, c="red")
	plt.title('Health vs Cost')
	plt.xlabel('Health')
	plt.ylabel('Cost')
	#plt.savefig(inc)
	plt.show()


def makeMatrix(csvFile):
	healthArray = []
	costArray = []
	dataArray = [[0 for x in range(2)] for y in range(200)]

	for row in csvFile: #get values from csvFile
		if int(row['health']) > 1 and int(row['health']) < 80:
			healthArray.append(int(row['health']))
		if int(row['cost']) > 1 and int(row['cost']) < 80:
			costArray.append(int(row['cost']))

	healthArray = healthArray[:200]
	costArray = costArray[:200]

	i = 0
	while i < 200: #add first 200 values into dataArray
		dataArray[i][0] = costArray[i]
		dataArray[i][1] = healthArray[i]
		i = i + 1

	return dataArray

def normalizeData(data):
	normalizedData = [0 for x in range(len(data))]
	stddev = main.findstddev(data)
	mean = main.findMean(data)
	for datum in data:
		normalizedData[datum] = (data[datum] - mean)/stddev
	return normalizedData

def getDistance(point1, point2):
	#Euclidian Diatance
	xDistance = pow(abs(point1[0] - point2[0]), 2)
	yDistance = pow(abs(point1[1] - point2[1]), 2)
	return np.math.sqrt(xDistance + yDistance)


def getRandomNumber():
	return random.randint(0, 200)

def getAverageValue(cluster):
	xValues = []
	yValues = []
	xAverage = 0
	yAverage = 0
	i = 0
	while i < len(cluster):
		xValues.append(cluster[i][1])
		yValues.append(cluster[i][0])
		i = i + 1

	j = 0
	while j < len(xValues):
		xAverage = xAverage + xValues[j]
		yAverage = yAverage + yValues[j]
		j = j + 1

	xAverage = xAverage/len(xValues)
	yAverage = yAverage/len(yValues)

	return [yAverage, xAverage]

def sse(centroid, cluster):
	i = 0
	sse = 0
	while i < len(cluster):
		sse = sse + getDistance(cluster[i], centroid)
		i = i + 1
	return sse



def outputResults(centroid1, centroid2, run):
	writer.writerow(("run ", run))
	writer.writerow(("Total SSE: ", sse(centroid1, cluster1) + sse(centroid2, cluster2)))

	#write cluster1 results
	writer.writerow("cluster 1")
	writer.writerow(("SSE: ", sse(centroid1, cluster1)))
	writer.writerow(("centroid: ", centroid1))
	writer.writerow(["cost", "health"])
	i = 0
	while i < len(cluster1):
		writer.writerow([cluster1[i][0], cluster1[i][1]])
		i = i + 1

	#write cluster2 results
	writer.writerow("cluster 2")
	writer.writerow(("SSE: ", sse(centroid2, cluster2)))
	writer.writerow(("centroid: ", centroid2))
	writer.writerow(["cost", "health"])
	i = 0
	while i < len(cluster2):
		writer.writerow([cluster2[i][0], cluster2[i][1]])
		i = i + 1


csvFile = openFile(os.path.join(sys.path[0], 'hearthstoneCards.csv'))
clusters = kmeans(csvFile)