import sys
import time
from pathlib import Path

### Salome GEOM and SMESH components
import salome
salome.salome_init()

# Set file paths for library and tests  

# sys.path.insert(0, r'C:/Users/francisco/Documents/dev/pipeline')
# sys.path.insert(0, r'C:/Users/francisco/Documents/dev/pipeline/genam')
# sys.path.insert(0, r'C:/Users/francisco/Documents/dev/pipeline/tests')

sys.path.insert(0, r'/home/bernardo/genam/')
sys.path.insert(0, r'/home/bernardo/genam/genam/')
sys.path.insert(0, r'/home/bernardo/genam/tests/')


# Genam Lens, mesh configurator
from genam.lens import Lens
from genam.lens_configuration import lens_configurator 
from genam.mesh_configuration import selector as mesh_config_selector
from genam.utility_functions import convert_mesh, copy_solver_templates
from genam.run_elmer_solver import run_elmer_solver
from matrices.quantized_1_1 import quantized_matrix_1_1

lens_config = lens_configurator( quantized_matrix_1_1 )

lens_name = 'quantized_matrix_1_1' 

# Create lens with name, bricks ID and mesh configurations 

lens = Lens( lens_config, mesh_config_selector(3), name = lens_name  )

start = time.time()

lens.process_geometry() # Create the lens geometry 

print("Geometry computation time: {:.2f} sec".format(time.time() - start) )

start = time.time()

lens.process_mesh() # Create lens mesh 

print("Mesh computation time: {:.2f} sec".format( time.time() - start) )

start = time.time()

# define a path where all data will be stored (.unv mesh file, solver *.mesh files, sif. file )
# path = str(Path('C:/Users/francisco/Documents/acoustic-brick/').joinpath( lens_name + '.unv')) 
path = str(Path('/SAN/uclic/ammdgop/data').joinpath( lens_name + '.unv'))


lens.export_mesh( path ) # export .unv mesh file

print("Mesh exported to Elmer format: {:.2f} sec".format( time.time() - start) )

start = time.time()

convert_mesh( path ) # run elmergrid convert .unv mesh file to elmer format *.mesh files in a directory 

# copy all the necessary templates to run elmer solver
copy_solver_templates( path )

print("Elmer template copied: {:.2f} sec".format( time.time() - start) )

run_elmer_solver( path )