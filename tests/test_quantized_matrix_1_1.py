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
from matrices.quantized_1_1 import quantized_matrix_1_1
from genam.utility_functions import convert_mesh, copy_solver_templates

lens_config = lens_configurator( quantized_matrix_1_1 )

lens_name = 'quantized_matrix_1_1' 

lens = Lens( lens_config, mesh_config_selector(3), name = lens_name  )

start = time.time()

lens.process_geometry()

print("Geometry computation time: {:.2f} sec".format(time.time() - start) )

start = time.time()

lens.process_mesh()

print("Mesh computation time: {:.2f} sec".format( time.time() - start) )

start = time.time()

path = str(Path('C:/Users/francisco/Documents/acoustic-brick/').joinpath( lens_name + '.unv'))

lens.export_mesh( path )

print("Mesh exported to Elmer format: {:.2f} sec".format( time.time() - start) )

start = time.time()

convert_mesh( path )

copy_solver_templates(  path, 
                        start_frequency = 40000, 
                        end_frequency = 41000, 
                        step = 1000 )

print("Elmer template copied: {:.2f} sec".format( time.time() - start) )


