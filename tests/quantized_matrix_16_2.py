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

sys.path.insert(0, r'C:/Users/francisco/Documents/dev/pipeline/tests')
# sys.path.insert(0, r'.')
print(sys.path)
# sys.path.append('.')
print (os.getcwd())

# from utility_functions import * 
# from parametric_shape import * 

# import genam.utility_functions as util 

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



# from genam.lens import Lens as l
# from genam import mesh_configuration  

quantized_matrix_16_2 = np.array([
                                  [ 10, 10 ],
                                  [ 13, 13 ],
                                  [  0,  0 ],
                                  [  3,  3 ],
                                  [  5,  5 ],
                                  [  6,  6 ],
                                  [  7,  7 ],
                                  [  8,  8 ],
                                  [  8,  8 ],
                                  [  7,  7 ],
                                  [  6,  6 ],
                                  [  5,  5 ],
                                  [  3,  3 ], 
                                  [  0,  0 ],
                                  [ 13, 13 ],
                                  [ 10, 10 ],  
                                ])

# lens_config = l.lens_configurator( quantized_matrix_16_2 )

# lens =  l.Lens( lens_config, mesh_configuration.mesh_config_selector(3) )

# start = time.time()

# end = lens.process_geometry()

# print("Geometry computation time: {:.2f} sec".format(end - start))

# start = time.time()

# end = lens.process_mesh()

# print("Mesh computation time: {:.2f} sec".format(end - start))

# start = time.time()

# end = lens.export_mesh( r'C:/Users/Francisco/Documents/acoustic-brick/Lens.unv')