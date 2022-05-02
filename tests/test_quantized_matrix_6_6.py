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


quantized_matrix_6_6 = np.array([ 
                                  [ 10, 13,  3,  3, 13, 10 ], #1
                                  [ 13,  4,  6,  6,  4, 13 ], #2
                                  [  3,  6,  7,  7,  6,  3 ], #3
                                  [  3,  6,  7,  7,  6,  3 ], #4
                                  [ 13,  4,  6,  6,  4, 13 ], #5
                                  [ 10, 13,  3,  3, 13, 10 ], #6
                                ])