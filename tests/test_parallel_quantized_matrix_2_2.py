import os, sys, time
from pathlib import Path

### Salome GEOM and SMESH components
import salome
salome.salome_init()


# Set file paths for library and tests  
sys.path.insert(0, r'C:/Users/francisco/Documents/dev/pipeline')
sys.path.insert(0, r'C:/Users/francisco/Documents/dev/pipeline/genam')
sys.path.insert(0, r'C:/Users/francisco/Documents/dev/pipeline/tests')

# sys.path.insert(0, r'/home/bernardo/genam/')
# sys.path.insert(0, r'/home/bernardo/genam/genam/')
# sys.path.insert(0, r'/home/bernardo/genam/tests/')


# Genam Lens, mesh configurator
from matrices.quantized_2_2 import quantized_matrix_2_2
from genam.lens import Lens
from genam.lens_configuration import lens_configurator 
from genam.mesh_configuration import selector as mesh_config_selector
from genam.utility_functions import convert_mesh, copy_solver_templates, copy_sif
from genam.run_elmer_solver import run_elmer_solver
from genam.analysis.analysis import Analysis



lens_config = lens_configurator( quantized_matrix_2_2 )

lens_name = 'quantized_matrix_2_2' 

# Create lens with name, bricks ID and mesh configurations 

lens = Lens( lens_config, mesh_config_selector(3), name = lens_name  )

start = time.time()

lens.process_geometry() # Create the lens geometry 

print("Geometry computation time: {:.2f} sec".format(time.time() - start) )

start = time.time()

lens.process_mesh() # Create lens mesh 

print("Mesh computation time: {:.2f} sec".format( time.time() - start) )

start = time.time()


DATASET_PATH = Path('/SAN/uclic/ammdgop/data')              # Dataset path, where all data will be stored - .unv mesh files and solver directories
UNV_PATH = DATASET_PATH.joinpath( lens_name + '.unv')       
SIF_PATH = Path('test_parallel_quantized_matrix_16_2.sif')       
SOLVER_DATA_PATH = DATASET_PATH.joinpath( lens_name )       #  solver *.mesh files, sif. file

lens.export_mesh( str( UNV_PATH ) ) # export .unv mesh file, requires conversion to string
print("Mesh exported to Elmer format: {:.2f} sec".format( time.time() - start) )

start = time.time()

convert_mesh( UNV_PATH ) # run elmergrid convert .unv mesh file to elmer format *.mesh files in a directory 

copy_solver_templates( SOLVER_DATA_PATH )          # copy all the necessary templates to run elmer solver
copy_sif( SOLVER_DATA_PATH, SIF_PATH )          # copy all the necessary templates to run elmer solver

print("Elmer template copied: {:.2f} sec".format( time.time() - start) )

run_elmer_solver( SOLVER_DATA_PATH )

analysis = Analysis( SOLVER_DATA_PATH.joinpath( 'case-40000_t0001.vtu' ))


# print(analysis.absolute_pressure())
print(analysis)