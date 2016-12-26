import matplotlib.pyplot
import numpy as np
# import pylab

test = np.loadtxt(open("_ericdata/horizontal.txt","rb"),delimiter=",",skiprows=1)
# x = [1,2,3,4]
# y = [3,4,8,6]
S1GX = test[:,3]
S1GY = test[:,4]
S1GZ = test[:,5]
S1AX = test[:,6]
S1AY = test[:,7]
S1AZ = test[:,8]
S2GX = test[:,9]
S2GY = test[:,10]
S2GZ = test[:,11]
S2AX = test[:,12]
S2AY = test[:,13]
S2AZ = test[:,14]
MX = test[:,15]
MY = test[:,16]


matplotlib.pyplot.scatter(S1GX,S1GY)
# matplotlib.pyplot.scatter(S1AX,S1AY)
# matplotlib.pyplot.scatter(S2GX,S2GY)
# matplotlib.pyplot.scatter(S2AX,S2AY)
# matplotlib.pyplot.scatter(MX,MY)

matplotlib.pyplot.show()