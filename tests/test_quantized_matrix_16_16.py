import sys
import time
from pathlib import Path

### Salome GEOM and SMESH components
import salome
salome.salome_init()

# Set file paths for library and tests  
# TODO: find a way to remove this into dependant classes as platform-dependent relative paths 
sys.path.insert(0, r'C:/Users/francisco/Documents/dev/pipeline')
sys.path.insert(0, r'C:/Users/francisco/Documents/dev/pipeline/genam')
sys.path.insert(0, r'C:/Users/francisco/Documents/dev/pipeline/tests')

# Genam Lens, mesh configurator
from genam.lens import Lens
from genam.lens_configuration import lens_configurator 
from genam.mesh_configuration import selector as mesh_config_selector
from matrices.quantized_16_16 import quantized_matrix_16_16



lens_config = lens_configurator( quantized_matrix_16_16 )

lens = Lens( lens_config, mesh_config_selector(3) )

start = time.time()

lens.process_geometry()

print("Geometry computation time: {:.2f} sec".format(time.time() - start))

start = time.time()

lens.process_mesh()

print("Mesh computation time: {:.2f} sec".format( time.time() - start))

start = time.time()

# end = lens.export_mesh( r'C:/Users/Francisco/Documents/acoustic-brick/Lens.unv')

print("Mesh exported to Elmer format: {:.2f} sec".format( time.time() - start))
