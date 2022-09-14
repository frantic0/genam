import os, sys, time, math
import pandas as pd
from pathlib import Path

### Salome GEOM and SMESH components
import salome
salome.salome_init()

# Set file paths for library and tests  
sys.path.insert(0, r'C:/Users/Francisco/Documents/dev/pipeline')
sys.path.insert(0, r'C:/Users/Francisco/Documents/dev/pipeline/genam')
sys.path.insert(0, r'C:/Users/Francisco/Documents/dev/pipeline/tests')

# sys.path.insert(0, r'/home/bernardo/genam/')
# sys.path.insert(0, r'/home/bernardo/genam/genam/')
# sys.path.insert(0, r'/home/bernardo/genam/tests/')


# Genam Lens, mesh configurator
from matrices.quantized_2_2 import quantized_matrix_2_2_y, quantized_matrix_2_2_0    # [ [  0, -1 ], [ -1,  1 ] ]
from matrices.quantized_1_4 import quantized_matrix_1_4, quantized_matrix_1_4_0     # [ [  1 ], [ -1 ], [  0 ], [ -1 ] ]
from matrices.quantized_4_1 import quantized_matrix_4_1, quantized_matrix_4_1_0     # [ [ 1,  -1,  0,  -1] ]


from genam.lens import Lens
from genam.lens_hemisphere import Lens as Lens_hemi
from genam.configuration.lens import configurator as lens_configurator 
from genam.configuration.mesh import configurator as mesh_configurator
from genam.solver import convert_mesh, copy_solver_templates, copy_sif, run_elmer_solver
from genam.analysis import Analysis





# lens_config = lens_configurator( quantized_matrix_2_2_0 )

config_lens_hemi_2_2 = lens_configurator( quantized_matrix_2_2_y )
# config_lens_hemi_2_2 = lens_configurator( quantized_matrix_2_2_0 )

config_lens_hemi_1_4 = lens_configurator( quantized_matrix_1_4 )
# config_lens_hemi_1_4 = lens_configurator( quantized_matrix_1_4_0 )

config_lens_hemi_4_1 = lens_configurator( quantized_matrix_4_1 )
# config_lens_hemi_4_1 = lens_configurator( quantized_matrix_4_1_0 )

lens_hemi_2_2_name = 'quantized_matrix_2_2_y' 
lens_hemi_1_4_name = 'quantized_matrix_1_4' 
lens_hemi_4_1_name = 'quantized_matrix_4_1' 

# # # Create lens with name, bricks ID and mesh configurations 

lens_hemi_2_2 = Lens_hemi(  config_lens_hemi_2_2, 
              mesh_configurator(3), 
              name              = lens_hemi_2_2_name,
              inlet_offset      = 4.3,
              outlet_offset     = 17.3,
              wavelength        = 8.661,
              set_hemisphere    = True )

lens_hemi_1_4 = Lens_hemi(  config_lens_hemi_1_4, 
              mesh_configurator(3), 
              name              = lens_hemi_1_4_name,
              inlet_offset      = 4.3,
              outlet_offset     = 17.3,
              wavelength        = 8.661,
              set_hemisphere    = True )

lens_hemi_4_1 = Lens_hemi(  config_lens_hemi_4_1, 
              mesh_configurator(3), 
              name              = lens_hemi_4_1_name,
              inlet_offset      = 4.3,
              outlet_offset     = 17.3,
              wavelength        = 8.661,
              set_hemisphere    = True )



start = time.time()


lens_hemi_2_2.process_geometry() # Create the lens geometry 
lens_hemi_1_4.process_geometry() # Create the lens geometry 
lens_hemi_4_1.process_geometry() # Create the lens geometry 
 

print("Geometry computation time: {:.2f} sec".format(time.time() - start) )

start = time.time()

lens_hemi_2_2.process_mesh() # Create lens mesh 
lens_hemi_1_4.process_mesh() # Create lens mesh 
lens_hemi_4_1.process_mesh() # Create lens mesh 

print("Mesh computation time: {:.2f} sec".format( time.time() - start) )

# start = time.time()


# DATASET_PATH = Path('/SAN/uclic/ammdgop/data')              # Dataset path, where all data will be stored - .unv mesh files and solver directories
# UNV_PATH = DATASET_PATH.joinpath( lens_name + '.unv')       
# SIF_PATH = Path('test_quantised_matrix.sif')       
# SOLVER_DATA_PATH = DATASET_PATH.joinpath( lens_name )       #  solver *.mesh files, sif. file

# lens.export_mesh( str( UNV_PATH ) ) # export .unv mesh file, requires conversion to string
# print("Mesh exported to Elmer format: {:.2f} sec".format( time.time() - start) )

# start = time.time()

# convert_mesh( UNV_PATH ) # run elmergrid convert .unv mesh file to elmer format *.mesh files in a directory 
# copy_solver_templates( SOLVER_DATA_PATH )          # copy all the necessary templates to run elmer solver
# copy_sif( SOLVER_DATA_PATH, SIF_PATH )          # copy solver input file

# print("Elmer template copied: {:.2f} sec".format( time.time() - start) )

# run_elmer_solver( SOLVER_DATA_PATH )

# analysis = Analysis( str(SOLVER_DATA_PATH.joinpath( 'case-40000_t0001.vtu' )) )

# find_optimisation_target = lambda points, precision, value: sorted(list(filter( lambda x: x[2] == 0.1 and x[0] < 0 and x[1] < 0, points)))

# optimisation_targets = find_optimisation_target(analysis.points, 2, 0.1)
# optimisation_target = optimisation_targets[len(optimisation_targets)-1]
# optimisation_target_id = analysis.points.index(optimisation_targets[len(optimisation_targets)-1])
# optimisation_target_pressure = analysis._absolute_pressure.GetValue(optimisation_target_id)

# print("Optimisation target: {} {} {} ".format( optimisation_target_id, optimisation_target, optimisation_target_pressure ) )

