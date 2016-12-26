import matplotlib.pyplot as plot
import numpy as np
import math

rawData = np.loadtxt(open("_ericdata/horizontal.txt","rb"),delimiter=",",skiprows=1)
# x = [1,2,3,4]
# y = [3,4,8,6]
time = np.array(rawData[:,1])
S1GX = np.array(rawData[:,3])
S1GY = np.array(rawData[:,4])
S1GZ = np.array(rawData[:,5])
S1AX = np.array(rawData[:,6])
S1AY = np.array(rawData[:,7])
S1AZ = np.array(rawData[:,8])
S2GX = np.array(rawData[:,9])
S2GY = np.array(rawData[:,10])
S2GZ = np.array(rawData[:,11])
S2AX = np.array(rawData[:,12])
S2AY = np.array(rawData[:,13])
S2AZ = np.array(rawData[:,14])
MX   = np.array(rawData[:,15])
MY   = np.array(rawData[:,16])

deltaTimes = []
deltaTimes.append(time[1] - time[0])
for i in range(1, time.size):
  deltaTimes.append(time[i] - time[i-1])

deltaTimes = np.array(deltaTimes)

S1AccAngleX = np.array([math.degrees(math.atan2(y, z) + math.pi) for y, z in zip(S1AY, S1AZ)])
S1AccAngleY = np.array([math.degrees(math.atan2(z, x) + math.pi) for z, x in zip(S1AZ, S1AX)])

S2AccAngleX = np.array([math.degrees(math.atan2(y, z) + math.pi) for y, z in zip(S2AY, S2AZ)])
S2AccAngleY = np.array([math.degrees(math.atan2(z, x) + math.pi) for z, x in zip(S2AZ, S2AX)])

AA = .98
currentAngleX1 = 0
currentAngleY1 = 0
currentAngleX2 = 0
currentAngleY2 = 0

CFangleX1 = np.array([AA*(currentAngleX1 + gx * dt) + (1 - AA) * ax for gx, ax, dt in zip(S1GX, S1AccAngleX, deltaTimes)])
CFangleY1 = np.array([AA*(currentAngleY1 + gy * dt) + (1 - AA) * ay for gy, ay, dt in zip(S1GY, S1AccAngleY, deltaTimes)])

CFangleX2 = np.array([AA*(currentAngleX2 + gx * dt) + (1 - AA) * ax for gx, ax, dt in zip(S2GX, S2AccAngleX, deltaTimes)])
CFangleY2 = np.array([AA*(currentAngleY2 + gy * dt) + (1 - AA) * ay for gy, ay, dt in zip(S2GY, S2AccAngleY, deltaTimes)])

# plot.plot(time, CFangleX1)
# plot.plot(time, CFangleY1)
# plot.plot(time, CFangleX2)
# plot.plot(time, CFangleY2)

# plot.show()

import csv
with open('data.csv', 'wb') as csvfile:
  writer = csv.writer(csvfile)
  writer.writerow(['time', 'x', 'y'])
  for t, x, y in zip(time, CFangleX1, CFangleY1):
    writer.writerow([t, x, y])
