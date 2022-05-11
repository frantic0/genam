import sys
import time
import numpy as np
from pathlib import Path

### Salome GEOM and SMESH components
import salome
salome.salome_init()

# # Set file paths for library and tests  

sys.path.insert(0, r'C:/Users/francisco/Documents/dev/pipeline')
sys.path.insert(0, r'C:/Users/francisco/Documents/dev/pipeline/genam')
sys.path.insert(0, r'C:/Users/francisco/Documents/dev/pipeline/tests')

# sys.path.insert(0, r'/home/bernardo/genam/')
# sys.path.insert(0, r'/home/bernardo/genam/genam/')
# sys.path.insert(0, r'/home/bernardo/genam/tests/')


# Genam Lens, mesh configurator
from matrices.quantized_16_2 import quantized_matrix_16_2
from genam.lens import Lens
from genam.lens_configuration import lens_configurator 
from genam.mesh_configuration import selector as mesh_config_selector
from genam.utility_functions import convert_mesh, copy_solver_templates
from genam.run_elmer_solver import run_elmer_solver_parallel
from genam.analysis import Analysis



lens_config = lens_configurator( quantized_matrix_16_2 )

lens_name = 'quantized_matrix_16_2' 

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

# run elmergrid convert .unv mesh file to elmer format *.mesh files in a directory 
convert_mesh( path, "-partition 2 2 1" ) # the mesh will be partitioned in cartesian main directions
# convert_mesh( path, "-partdual -metisrec 4" ) # mesh will be partitioned with Metis using graph Kway routine
# convert_mesh( path, "-partdual -metiskway 4" ) # mesh will be partitioned with Metis using graph Recursive routine


# copy all the necessary templates to run elmer solver and copy SIF with 
copy_solver_templates( path, 
                       sif_path='./sif/test_parallel_quantized_matrix_16_2.sif'  )

print("Elmer template copied: {:.2f} sec".format( time.time() - start) )

run_elmer_solver_parallel( path, 4 )

# analysis_path = str( Path('/SAN/uclic/ammdgop/data').joinpath( lens_name ).joinpath( 'case-40000_t0001.vtu' ) )
analysis_path = str( Path('C:/Users/francisco/Documents/dev/pipeline/data').joinpath( 'lens-16-2' ).joinpath( 'case-40000_t0001.vtu' ) )

analysis = Analysis( analysis_path )



print(analysis.absolute_pressure)

# print("#values: {}".format( len( analysis.absolute_pressure ) ))
# min_absolute_pressure_wave = sorted( analysis.absolute_pressure )[0]
# max_absolute_pressure_wave = sorted( analysis.absolute_pressure ) [ len( analysis.absolute_pressure )-1]
# print("Value Range: {} {}".format( min_absolute_pressure_wave , max_absolute_pressure_wave ))
# print("Index of value {}: {}".format( min_absolute_pressure_wave, np.where( analysis.absolute_pressure == min_absolute_pressure_wave )[0] ))
# print("Index of value {}: {}".format( max_absolute_pressure_wave,  np.where( analysis.absolute_pressure == max_absolute_pressure_wave)[0] ))