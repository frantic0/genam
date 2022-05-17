from re import S
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
# from operator import itemgetter
from collections import namedtuple
from vtkmodules.all import vtkXMLUnstructuredGridReader, vtkPoints, vtkCellArray, vtkPointLocator, vtkIdList, vtkQuad, vtkIntArray
import meshio

# Boundary Conditions
inletBC = 1
outletBC = 3

rho0 = 1.205
c0 = 343
flowDir = np.array([1, 0, 0])


calculate_absolute_pressure = lambda real, imag: 20*math.log10(((math.sqrt(real**2+imag**2))/math.sqrt(2)))
# 20*math.log(((math.sqrt(real**2+imag**2))/math.sqrt(2)))

calculate_absolute_pressure_pa = lambda real, imag: math.sqrt(real**2+imag**2)


class Analysis:

    def __init__( self, filename ):
        self.reader = vtkXMLUnstructuredGridReader()
        self.filename = filename
        self.__read()


    def __read(self):
       
        try:
            print('vtu: ' + self.filename)
            self.reader.SetFileName(self.filename)
            self.reader.Update()  # Needed because of GetScalarRange
            self._unstructuredGrid = self.reader.GetOutput() 
            
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
            
            self._geometryIds =          self._unstructuredGrid.GetCellData().GetArray("GeometryIds")

            self.points = [ self._unstructuredGrid.GetPoint(x) for x in range(self._unstructuredGrid.GetNumberOfPoints()) ]

            self.dataframe = pd.DataFrame({
                "x":  [ self._unstructuredGrid.GetPoint(x)[0] for x in range(self._unstructuredGrid.GetNumberOfPoints()) ],
                "y":  [ self._unstructuredGrid.GetPoint(x)[1] for x in range(self._unstructuredGrid.GetNumberOfPoints()) ],
                "z":  [ self._unstructuredGrid.GetPoint(x)[2] for x in range(self._unstructuredGrid.GetNumberOfPoints()) ], 
                "absolutePressure": pd.Series([self.pressure.absolute.GetValue(x) for x in range(self.pressure.absolute.GetNumberOfValues())] ),
                "realPressure": pd.Series([self.pressure.real.GetValue(x) for x in range(self.pressure.real.GetNumberOfValues())] ),
                "complexPressure": pd.Series([self.pressure.complex.GetValue(x) for x in range(self.pressure.complex.GetNumberOfValues())] ),
                "SPL": pd.Series([self._spl.GetValue(x) for x in range(self._spl.GetNumberOfValues())] ),
                "phase": pd.Series([self._phase.GetValue(x) for x in range(self._phase.GetNumberOfValues())] ),
                "phaseAtan2": pd.Series([self._phaseAtan2.GetValue(x) for x in range(self._phaseAtan2.GetNumberOfValues())] )

            })

            # self.quad = vtkQuad()
            # self.cells = vtkCellArray()
            
            self.pointLocator = vtkPointLocator()
            self.pointLocator.SetDataSet(self.reader.GetOutput())
            self.pointLocator.BuildLocator()

            self._data = meshio.read(self.filename)

        except Exception as e:
            print('exception' + str(e) )

    @property
    def real_pressure(self):
        return self._data.point_data["pressure wave 1"]
        
    @property
    def complex_pressure(self):
        return self._data.point_data["pressure wave 2"]

    @property
    def absolute_pressure(self):
        return self._data.point_data["pabs"]
        
    @property
    def spl(self):
        return self._data.point_data["spl"]

    @property
    def phase(self):
        return self._data.point_data["phase"]
        
    @property
    def phase_atan2(self):
        return self._data.point_data["phaseatan2"]
        
    @property
    def getGeometryId(self, index:int) -> vtkIntArray :
        return self._unstructuredGrid.GetCellData().GetArray("GeometryIds")

    @property
    def getNumberOfValues(self) -> int:
        return self._unstructuredGrid.GetCellData().GetArray("GeometryIds").GetNumberOfValues()

    @property
    def getNumberOfPoints(self) -> int:
        return self._unstructuredGrid.GetNumberOfPoints()

    @property
    def getPoint(self, id:int) -> tuple:
        return self._unstructuredGrid.GetPoint(id)

