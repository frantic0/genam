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