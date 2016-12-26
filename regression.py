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

def parseCSVaveraged(fileName):
    csvFile = open(fileName)
    dataReader = csv.reader(csvFile)
    dataReader.next()

    dataAveraged = []
    relevantIndices = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    for index, row in enumerate(dataReader):
        if index % 3 == 0:
            newRow = np.array([])
            for relevantIndex in relevantIndices:
                newRow = np.append(newRow, float(row[relevantIndex]))
            dataAveraged.append(newRow)
        else:
            for columnIndex, relevantIndex in enumerate(relevantIndices):
                dataAveraged[-1][columnIndex] += float(row[relevantIndex])/3.0
    dataAveraged = np.array(dataAveraged)

    csvFile.close()
    return dataAveraged

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



trainingScreenFiles = ['data/screen-data/csv/richard-test1.json.csv']#,
                       #'data/screen-data/csv/richard-test2.json.csv',
                       #'data/screen-data/csv/richard-test3.json.csv',
                       #'data/screen-data/csv/richard-test4.json.csv']

trainingSensorFiles = ['data/sensor-data/richard-test1-warped.csv']#,
                       #'data/sensor-data/richard-test2.csv',
                       #'data/sensor-data/richard-test3.csv',
                       #'data/sensor-data/richard-test4.csv']

screenData = []
sensorData = []
for i in range(0, len(trainingScreenFiles)):
    singleScreenData = parseCSV(trainingScreenFiles[i])
    singleSensorData = parseCSV(trainingSensorFiles[i])#[:len(singleScreenData)-1]

    for row in calculateDerivative(singleScreenData):
        screenData.append(row)
    for row in singleSensorData:
        sensorData.append(row)
    
screenData = np.array(screenData)
sensorData = np.array(sensorData)

#print (screenData)
#print ('=========')
#print (sensorData)


screenData = calculateDerivative(parseCSV('data/screen-data/csv/richard-test1.json.csv'))
sensorData = calculateDerivative(parseCSV('data/sensor-data/richard-test1-warped.csv'))
#screenData = calculateDerivative(screenData)

screenDataTest = parseCSV('data/screen-data/csv/richard-test5a.json.csv')
sensorDataTest = parseCSV('data/sensor-data/richard-test5a.csv')


#print '========='
#print screenData
#print '========='
#print calculateIntegral(calculateDerivative(screenData))
#print '========='

"""
matplot.figure(1)
matplot.plot(screenData[:, [1]], screenData[:, [2]])

rebuiltScreenData = calculateIntegral(calculateDerivative(screenData))
matplot.figure(2)
matplot.plot(rebuiltScreenData[:, [1]], rebuiltScreenData[:, [2]])

matplot.show()
"""

#regression = linear_model.LinearRegression()
regression = kernel_ridge.KernelRidge()
sensorDataReshaped = sensorData[:,range(1,len(sensorData[0]))]
screenDataReshaped = screenData[1:,range(1,len(screenData[0]))]
regression.fit(sensorDataReshaped, screenDataReshaped)
print (sensorDataReshaped.shape, screenDataReshaped.shape, sensorDataTest[:,range(3,15)].shape)
regressedScreenDataTest = calculateIntegral(regression.predict(sensorDataTest[:,range(3,15)]))
regressedScreenData = calculateIntegral(regression.predict(sensorDataReshaped))

matplot.figure(1)

matplot.subplot(221).set_title('Reconstructed ground truth')
matplot.plot(regressedScreenData[:, [0]], regressedScreenData[:, [1]])

matplot.subplot(222).set_title('Ground truth')
screenData = calculateIntegral(screenData)
matplot.plot(screenData[:, [1]], screenData[:, [2]])

matplot.subplot(223).set_title('Reconstructed test')
matplot.plot(regressedScreenDataTest[:, [0]], regressedScreenDataTest[:, [1]])

matplot.subplot(224).set_title('Test')
matplot.plot(screenDataTest[:, [1]], screenDataTest[:, [2]])

matplot.show()
