import numpy as np
# import pandas as pd
import math
import matplotlib.pyplot as plt
from collections import namedtuple
import vtk
import meshio

# Boundary Conditions
inletBC = 1
outletBC = 3

rho0 = 1.205
c0 = 343
flowDir = np.array([1, 0, 0])



# datFileName = lambda a: '../../ammgdop-20220221/brick-{}/SPLmean.dat'.format(a)
# vtu_filename = '../ammgdop-ds-20220208/brick-15/case-40000_t0001.vtu'

# datFileNames = [ datFileName(fn) for fn in range(1,16) ]

# Parse input names, this list is shared across all bricks 
# column_names = parseDatNames(datFileNames[14])

def calculate_absolute_pressure(real, imag): 
    return 20*math.log10(((math.sqrt(real**2+imag**2))/math.sqrt(2)))
    # return 20*math.log(((math.sqrt(real**2+imag**2))/math.sqrt(2)))

def calculate_absolute_pressure_pa(real, imag): 
    return math.sqrt(real**2+imag**2)


class Analysis:

    def __init__( self, filename ):
        self.reader = vtk.vtkXMLUnstructuredGridReader()
        self.filename = filename
        self.__read()


    def __read(self):
       
        try: 
            self.reader.SetFileName(self.filename)
            self.reader.Update()  # Needed because of GetScalarRange
            self._unstructuredGrid =     self.reader.GetOutput() 
            
            Pressure = namedtuple('Pressure', 'real complex absolute')
            self.pressure = Pressure(
                self._unstructuredGrid.GetPointData().GetArray("pressure wave 1"),
                self._unstructuredGrid.GetPointData().GetArray("pressure wave 2"),
                self._unstructuredGrid.GetPointData().GetArray("pabs")
            )

            self._real_pressure =        self._unstructuredGrid.GetPointData().GetArray("pressure wave 1")
            self._complex_pressure =     self._unstructuredGrid.GetPointData().GetArray("pressure wave 2")
            self._absolute_pressure =    self._unstructuredGrid.GetPointData().GetArray("pabs")
            
            self._spl =                  self._unstructuredGrid.GetPointData().GetArray("spl")
            self._phase =                self._unstructuredGrid.GetPointData().GetArray("phase")
            self._phaseAtan2 =           self._unstructuredGrid.GetPointData().GetArray("phaseatan2")

            self.data = meshio.read(self.filename)
            self.field_data = self.data.point_data
            self.coordinates = self.data.points
                
        except Exception as e:
            print(e)

    @property
    def real_pressure(self):
        return self._real_pressure

    @property
    def complex_pressure(self):
        return self._complex_pressure

    @property
    def absolute_pressure(self):
        return self._absolute_pressure

    @property
    def spl(self):
        return self._spl

    @property
    def phase(self):
        return self._phase

    @property
    def phase_atan2(self):
        return self._phaseAtan2

    @property
    def field_data(self):
        return self.field_data

    @property
    def coordinates(self):
        return self.coordinates        


    # @property
    # def real_pressure(self):
    #     return self._pressure_wave_2_flux

    # @property
    # def real_pressure(self):
    #     return self._pressure_wave_1_flux

    # def __parseDatNames__(filename):
    #     res = [] # Initialize
    #     if filename[-6:] != ".names":
    #         filename = filename + ".names"
    #     with open(filename, 'r') as f:
    #         isHeader = True
    #         for line in f:
    #             if 'Variables in columns' in line:
    #                 isHeader = False
    #                 continue
    #             if isHeader == True:
    #                 continue
    #             # strParse1: get rid of 1: boundary mean, and split over "over"
    #             strParse1 = line.strip().split(':')[-1].strip().split('over')
    #             if len(strParse1) == 1:
    #                 res.append(strParse1[0])
    #             else:
    #                 if len(strParse1[0]) > 0:
    #                     itemName = strParse1[0]
    #                 else:
    #                     strParse1[0] = itemName
    #                 res.append(strParse1[0].strip() + '.' + strParse1[1].strip())
    #     return res

    # def calculateTransmissionLoss(self, res, frequency_column_index, flowDir):

    # #     frequency_columns_index = column_names.index('frequency')
    #     freqVec = res[:, frequency_column_index]
    #     omegaVec = 2 * np.pi * freqVec

    #     ## Get pressure at inlet and outlet

    #     pIn = res[:, column_names.index('pressure wave 1.bc ' + str(inletBC))] \
    #     + 1j * res[:, column_names.index('pressure wave 2.bc ' + str(inletBC))]

    #     pOut = res[:, column_names.index('pressure wave 1.bc ' + str(outletBC))] \
    #     + 1j * res[:, column_names.index('pressure wave 2.bc ' + str(outletBC))]

    #     # print(pIn)
    #     # print(pOut)

    #     #  Check if it is 3D
    #     dim = 3
    #     if "pressure wave 1 grad 3.bc 1" not in column_names:
    #         dim = 2
    #         flowDir = flowDir[:-1]

    #     pGradIn, pGradOut = np.zeros((freqVec.size, dim), dtype=np.complex_), np.zeros((freqVec.size, dim), dtype=np.complex_)

    #     # Get pGradIn and pGradOut
    #     fmt = 'pressure wave {0:d} grad {1:d}.bc {2:s}'
    #     for ind in range(dim):
    #         # Inlet
    #         strReal = fmt.format(1, ind+1, str(inletBC))
    #         strImag = fmt.format(2, ind+1, str(inletBC))
    #         pGradIn[:, ind] = res[:, column_names.index(strReal)] + 1j * res[:, column_names.index(strImag)]
    #         # outlet
    #         strReal = fmt.format(1, ind+1, str(outletBC))
    #         strImag = fmt.format(2, ind+1, str(outletBC))
    #         pGradOut[:, ind] = res[:, column_names.index(strReal)] + 1j * res[:, column_names.index(strImag)]

    #     # Decomposition at inlet
    #     dpdnIn = pGradIn.dot(flowDir)
    #     uIn = 1j/rho0/omegaVec*dpdnIn
    #     pInPlus = (pIn + uIn*rho0*c0)/2
    #     pInMinus = pIn - pInPlus

    #     # Decomposition at outlet
    #     dpdnOut = pGradOut.dot(flowDir)
    #     uOut = 1j/rho0/omegaVec*dpdnOut

    #     # Transmission Loss
    #     TL = 20*np.log10(np.abs(pInPlus)/np.abs(pOut))
        
    #     return freqVec, TL


