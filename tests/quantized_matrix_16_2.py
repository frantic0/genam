
import configparser
import sys
import numpy as np
import time, os
import inspect


### Salome GEOM and SMESH components
import salome
salome.salome_init()
import salome_notebook
notebook = salome_notebook.NoteBook()

sys.path.insert(0, inspect.getfile(lambda: None))
# sys.path.insert(0, r'C:/Users/francisco/Documents/dev/pipeline')
print(sys.path)
# print (os.getcwd())

import GEOM
from salome.geom import geomBuilder
import SALOMEDS
import SMESH, SALOMEDS
from salome.smesh import smeshBuilder
from salome.GMSHPlugin import GMSHPluginBuilder

### Genam Lens, mesh configurator
from genam.lens import Lens, lens_configurator
from genam.mesh_configuration import mesh_config_selector 

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

lens_config = lens_configurator( quantized_matrix_16_2 )

lens = Lens( lens_config, mesh_config_selector(3) )

# start = time.time()

# end = lens.process_geometry()

# print("Geometry computation time: {:.2f} sec".format(end - start))

# start = time.time()

# end = lens.process_mesh()

# print("Mesh computation time: {:.2f} sec".format(end - start))

# start = time.time()

# end = lens.export_mesh( r'C:/Users/Francisco/Documents/acoustic-brick/Lens.unv')