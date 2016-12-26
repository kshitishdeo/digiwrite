import sys
import serial
import time
import matplotlib.pyplot as plot
import numpy as np
import math

serial = serial.Serial(
    port='/dev/cu.usbmodem797521',\
    baudrate=115200,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=0)

num_lines_to_remove = 10

dataTime = []
S1AccAngleXList = []
S1AccAngleYList = []
S2AccAngleXList = []
S2AccAngleYList = []

CFangleX1List = []
CFangleY1List = []
CFangleX2List = []
CFangleY2List = []

currentAngleX1 = 0
currentAngleY1 = 0
currentAngleX2 = 0
currentAngleY2 = 0

current_line = 0
start_time = -1
while serial:
    line = serial.readline()
    if line:
        line_split = line.split(" ")
        if len(line_split) == 16:
            if current_line < num_lines_to_remove:
                current_line += 1
            else:
                # print line_split
                (line_split[0]) # Teensy time

                if start_time == -1:
                    start_time = time.time()


                currentTime = (time.time()-start_time)
                dataTime.append(currentTime) # Python system time
                S1GX = float(line_split[2]) # sensor 1 gyroscope X
                S1GY = float(line_split[3]) # sensor 1 gyroscope Y
                S1GZ = float(line_split[4]) # sensor 1 gyroscope Z
                S1AX = float(line_split[5]) # sensor 1 accelerometer X
                S1AY = float(line_split[6]) # sensor 1 accelerometer Y
                S1AZ = float(line_split[7]) # sensor 1 accelerometer X
                S2GX = float(line_split[8]) # sensor 2 gyroscope X
                S2GY = float(line_split[9]) # sensor 2 gyroscope Y
                S2GZ = float(line_split[10]) # sensor 2 gyroscope Z
                S2AX = float(line_split[11]) # sensor 2 accelerometer X
                S2AY = float(line_split[12]) # sensor 2 accelerometer Y
                S2AZ = float(line_split[13]) # sensor 2 accelerometer Z
                MX   = float(line_split[14]) # mouse X
                MY   = float(line_split[15]) # mouse Y


                S1AccAngleX = math.degrees(math.atan2(S1AY, S1AZ) + math.pi)
                S1AccAngleY = math.degrees(math.atan2(S1AZ, S1AX) + math.pi)

                S2AccAngleX = math.degrees(math.atan2(S2AY, S2AZ) + math.pi)
                S2AccAngleY = math.degrees(math.atan2(S2AZ, S2AX) + math.pi)

                S1AccAngleXList.append(S1AccAngleX)
                S1AccAngleYList.append(S1AccAngleY)
                S2AccAngleXList.append(S2AccAngleX)
                S2AccAngleYList.append(S2AccAngleY)

                AA = .98

                CFangleX1 = AA*(currentAngleX1 + S1GX * currentTime) + (1 - AA) * S1AccAngleX
                CFangleY1 = AA*(currentAngleY1 + S1GY * currentTime) + (1 - AA) * S1AccAngleY
                CFangleX2 = AA*(currentAngleX2 + S2GX * currentTime) + (1 - AA) * S2AccAngleX
                CFangleY2 = AA*(currentAngleY2 + S2GY * currentTime) + (1 - AA) * S2AccAngleY

                print CFangleX1
                print CFangleY1
                print CFangleX2
                print CFangleY2
                currentAngleX1 = CFangleX1
                currentAngleY1 = CFangleY1
                currentAngleX2 = CFangleX2
                currentAngleY2 = CFangleY2

                CFangleX1List.append(CFangleX1)
                CFangleY1List.append(CFangleY1)
                CFangleX2List.append(CFangleX2)
                CFangleY2List.append(CFangleY2)

                plot.plot(dataTime, CFangleX1List)
                plot.plot(dataTime, CFangleY1List)
                plot.plot(dataTime, CFangleX2List)
                plot.plot(dataTime, CFangleY2List)

                plot.draw()
                plot.pause(0.01)
