import csv
import numpy as np
import sklearn.linear_model as linear_model
import sklearn.kernel_ridge as kernel_ridge
import matplotlib.pyplot as matplot

np.set_printoptions(threshold='nan')

def parseCSV(fileName):
    csvFile = open(fileName)
    dataReader = csv.reader(csvFile)
    next(dataReader)

    data = []
    for row in dataReader:
        data.append(np.array([float(column) for column in row]))
    data = np.array(data)

    csvFile.close()
    return data



def calculateDerivative(data):
    result = []
    for rowIndex in range(1, len(data)):
        derivativeRow = []
        for columnIndex in range(0, len(data[rowIndex])):
            derivativeRow.append(data[rowIndex][columnIndex]-data[rowIndex-1][columnIndex])
        result.append(derivativeRow)
    result = np.array(result)

    return result

def calculateIntegral(data):
    result = []
    result.append(np.array([0 for i in data[0]]))
    for row in data:
        result.append(np.array([column+result[-1][columnIndex] for columnIndex, column in enumerate(row)]))

    return np.array(result)

screenData = parseCSV('data/screen-data/csv/richard-test1.json.csv')
sensorData = parseCSV('data/sensor-data/richard-test1.csv')
warpedSensorData = []

sensorDataIndex = 0
for screenRow in screenData:
    while sensorData[sensorDataIndex][1] < screenRow[0]:
        sensorDataIndex += 1

    sensorMinusOne = sensorData[sensorDataIndex-1]
    sensorPlusOne = sensorData[sensorDataIndex]

    minusWeight = abs(sensorPlusOne[1]-screenRow[0]) # flip weight associations
    plusWeight = abs(sensorMinusOne[1]-screenRow[0])

    warpedSensorDataRow = []
    warpedSensorDataRow.append(screenRow[0])
    for column in range(3, 15):
        warpedSensorDataValue = (minusWeight*sensorMinusOne[column]+plusWeight*sensorPlusOne[column])/(minusWeight+plusWeight)
        warpedSensorDataRow.append(warpedSensorDataValue)
    warpedSensorData.append(np.array(warpedSensorDataRow))
warpedSensorData = np.array(warpedSensorData)

for row in warpedSensorData:
    printedRow = ''
    for col in row:
        printedRow += str(col) + ','
    print (printedRow[:-1])
