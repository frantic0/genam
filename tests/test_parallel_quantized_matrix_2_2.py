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
from genam.configuration.lens import configurator as lens_configurator 
from genam.configuration.mesh import configurator as mesh_configurator
from genam.solver import convert_mesh, copy_solver_templates, copy_sif, run_elmer_solver
from genam.analysis import Analysis



# lens_config = lens_configurator( quantized_matrix_2_2 )

lens_name = 'quantized_matrix_2_2' 

# # # Create lens with name, bricks ID and mesh configurations 

# lens = Lens( lens_config, mesh_configurator(3), name = lens_name  )

# # start = time.time()

# lens.process_geometry() # Create the lens geometry 

# # print("Geometry computation time: {:.2f} sec".format(time.time() - start) )

# # start = time.time()

# lens.process_mesh() # Create lens mesh 

# # print("Mesh computation time: {:.2f} sec".format( time.time() - start) )

# # start = time.time()


DATASET_PATH = Path('/SAN/uclic/ammdgop/data')              # Dataset path, where all data will be stored - .unv mesh files and solver directories
UNV_PATH = DATASET_PATH.joinpath( lens_name + '.unv')       
SIF_PATH = Path('test_parallel_quantized_matrix_16_2.sif')       
SOLVER_DATA_PATH = DATASET_PATH.joinpath( lens_name )       #  solver *.mesh files, sif. file

# lens.export_mesh( str( UNV_PATH ) ) # export .unv mesh file, requires conversion to string
# print("Mesh exported to Elmer format: {:.2f} sec".format( time.time() - start) )

# start = time.time()

# convert_mesh( UNV_PATH ) # run elmergrid convert .unv mesh file to elmer format *.mesh files in a directory 
# copy_solver_templates( SOLVER_DATA_PATH )          # copy all the necessary templates to run elmer solver
# copy_sif( SOLVER_DATA_PATH, SIF_PATH )          # copy solver input file

# print("Elmer template copied: {:.2f} sec".format( time.time() - start) )

# run_elmer_solver( SOLVER_DATA_PATH )

analysis = Analysis( str(SOLVER_DATA_PATH.joinpath( 'case.vtu' )) )

find_optimisation_target = lambda points, precision, value: list(filter( lambda x: round(x[0], precision) == 0 and round(x[1], precision) == 0 and x[2] == value, points ))

optimisation_target = find_optimisation_target(analysis.points, 2, 0.1) [0]
optimisation_target_id = analysis.points.index(optimisation_target)
optimisation_target_pressure = analysis._absolute_pressure.GetValue(optimisation_target_id)

print("Optimisation target: {} {} {} ".format( optimisation_target_id, optimisation_target, optimisation_target_pressure ) )

# print(points) 
# print()
