# -*- coding: utf-8 -*-
# Computing transmission loss from 2-port simulation.
# 1st version: 11/09/2019 at Tuve, CWeng
import numpy as np
import matplotlib.pyplot as plt

#************ Parse *.dat.names  #************#************
# Should return res as a Str list which is used
# later for mapping the nemerical data in the .dat files...
def parseDatNames(filename):
    res = [] # Initialize
    if filename[-6:] != ".names":
        filename = filename + ".names"
    with open(filename, 'r') as f:
        isHeader = True
        for line in f:
            if 'Variables in columns' in line:
                isHeader = False
                continue
            if isHeader == True:
                continue
            # finally we can do some work here:
            # strParse1: get rid of 1: boundary mean, and split over "over"
            strParse1 = line.strip().split(':')[-1].strip().split('over')
            if len(strParse1) == 1:
                res.append(strParse1[0])
            else:
                if len(strParse1[0]) > 0:
                    itemName = strParse1[0]
                else:
                    strParse1[0] = itemName
                res.append(strParse1[0].strip() + '.' + strParse1[1].strip())
    return res
#************#************#************#************



## User input:
filename = 'BC0D.dat'
inletBCid = 1
outletBCid = 2
rho0 = 1.205
c0 = 343
flowDir = np.array([1, 0, 0]);

# Parse input names:
resNames = parseDatNames(filename)


with open(filename, 'r') as f:
    res = np.array([np.fromstring(line.strip(), dtype=float, sep=' ') for line in f])

#############################     Assign values #########################
## Get freq.
freqVec = res[:, resNames.index('frequency')]
omegaVec = 2*np.pi*freqVec
## Get pressure at inlet and outlet
pIn = res[:, resNames.index('pressure wave 1.bc ' + str(inletBCid))] \
     + 1j*res[:, resNames.index('pressure wave 2.bc ' + str(inletBCid))]
pOut = res[:, resNames.index('pressure wave 1.bc ' + str(outletBCid))] \
     + 1j*res[:, resNames.index('pressure wave 2.bc ' + str(outletBCid))]

## Get velocity at inlet. Note that uIn = 1j/rho0/omegaVec*dp/dn
# To decompose the p to p+ and p-, we notice that
#     p+ + p- = p
#     p+ - p- = uIn*rho0*c0
# so, p+ = (p + uIn*rho0*c0)/2

#  Check if it is 3D
dim = 3
if "pressure wave 1 grad 3.bc 1" not in resNames:
    dim = 2
    flowDir = flowDir[:-1]

pGradIn, pGradOut = np.zeros((freqVec.size, dim), dtype=np.complex_), np.zeros((freqVec.size, dim), dtype=np.complex_)
# Get pGradIn and pGradOut
fmt = 'pressure wave {0:d} grad {1:d}.bc {2:s}'
for ind in range(dim):
    # Inlet
    strReal = fmt.format(1, ind+1, str(inletBCid))
    strImag = fmt.format(2, ind+1, str(inletBCid))
    pGradIn[:, ind] = res[:, resNames.index(strReal)] \
     + 1j*res[:, resNames.index(strImag)]
    # outlet
    strReal = fmt.format(1, ind+1, str(outletBCid))
    strImag = fmt.format(2, ind+1, str(outletBCid))
    pGradOut[:, ind] = res[:, resNames.index(strReal)] \
     + 1j*res[:, resNames.index(strImag)]

# Decomposition at inlet
dpdnIn = pGradIn.dot(flowDir)
uIn = 1j/rho0/omegaVec*dpdnIn
pInPlus = (pIn + uIn*rho0*c0)/2
pInMinus = pIn - pInPlus


# Decomposition at outlet
dpdnOut = pGradOut.dot(flowDir)
uOut = 1j/rho0/omegaVec*dpdnOut
# %% TL, assuming same cross section area in inlet and outlet

TL = 20*np.log10(np.abs(pInPlus)/np.abs(pOut))

plt.close("all")
fig, ax = plt.subplots()
ax.minorticks_on()
#ax.grid(which='both')
ln = plt.plot(freqVec, TL, '-o', label='Simulation')
plt.xlabel('Frequncy, Hz'), plt.ylabel('TL, dB')
plt.title(filename)
plt.show()
