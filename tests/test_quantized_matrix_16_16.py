import configparser
import sys
import salome
import numpy as np
# import pandas as pd
import time, os
import random


salome.salome_init()
import salome_notebook
notebook = salome_notebook.NoteBook()

sys.path.insert(0, r'C:/Users/francisco/Documents/dev/genamm/genam')

from utility_functions import * 
from parametric_shape import * 

###
### Salome GEOM and SMESH components
###

import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS

import SMESH, SALOMEDS
from salome.smesh import smeshBuilder
from salome.GMSHPlugin import GMSHPluginBuilder



quantized_matrix_16_16 = np.array([
                                  [ 13,  0,  3,  5,  7,  8,  9, 10, 10,  9,  8,  7,  5,  3,  0, 13 ], #0
                                  [  0,  3,  6,  8, 10, 12, 13, 13, 13, 13, 12, 10,  8,  6,  3,  0 ], #1 
                                  [  3,  6,  9, 11, 13, 15,  0,  0,  0,  0, 15, 13, 11,  9,  6,  3 ], #2 
                                  [  5,  8, 11, 14,  0,  1,  2,  3,  3,  2,  1,  0, 14, 11,  8,  5 ], #3 
                                  [  7, 10, 13,  0,  2,  3,  4,  5,  5,  4,  3,  2,  0, 13, 10,  7 ], #4 
                                  [  8, 12, 15,  1,  3,  5,  6,  6,  6,  6,  5,  3,  1, 15, 12,  8 ], #5                                 
                                  [  9, 13,  1,  4,  5,  6,  7,  7,  7,  7,  6,  5,  4,  1, 13,  9 ], #6
                                  [ 10, 13,  0,  3,  5,  6,  7,  8,  8,  7,  6,  5,  3,  0, 13, 10 ], #7 
                                  [ 10, 13,  0,  3,  5,  6,  7,  8,  8,  7,  6,  5,  3,  0, 13, 10 ], #8
                                  [  9, 13,  1,  4,  5,  6,  7,  7,  7,  7,  6,  5,  4,  1, 13,  9 ], #9
                                  [  8, 12, 15,  1,  3,  5,  6,  6,  6,  6,  5,  3,  1, 15, 12,  8 ], #10
                                  [  7, 10, 13,  0,  2,  3,  4,  5,  5,  4,  3,  2,  0, 13, 10,  7 ], #11                                   
                                  [  5,  8, 11, 14,  0,  1,  2,  3,  3,  2,  1,  0, 14, 11,  8,  5 ], #12
                                  [  3,  6,  9, 11, 13, 15,  0,  0,  0,  0, 15, 13, 11,  9,  6,  3 ], #13 
                                  [  0,  3,  6,  8, 10, 12, 13, 13, 13, 13, 12, 10,  8,  6,  3,  0 ], #14
                                  [ 13,  0,  3,  5,  7,  8,  9, 10, 10,  9,  8,  7,  5,  3,  0, 13 ], #15
                                ])