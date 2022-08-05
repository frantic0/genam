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
from matrices.quantized_1_1 import quantized_matrix_1_1_x
from genam.lens import Lens
from genam.lens_hemisphere import Lens as Lens_hemi
from genam.configuration.lens import configurator as lens_configurator 
from genam.configuration.mesh import configurator as mesh_configurator
from genam.solver import convert_mesh, copy_solver_templates, copy_sif, run_elmer_solver
# from genam.analysis import Analysis


brick_ID = -1

if sys.argv == ['']:
   brick_ID = 15
else: 
   print( 'args', sys.argv )
   brick_ID =  int(sys.argv[2])
   


def compute_kernel_simulation( quantized_matrix_id ):

   config_lens_hemi_1_1 = lens_configurator( quantized_matrix_1_1_x( quantized_matrix_id ) )

   lens_hemi_1_1_name = 'hemi_quantized_matrix_1_1_{}'.format( quantized_matrix_id ) 

   # # # Create lens with name, bricks ID and mesh configurations 

   lens_hemi_1_1 = Lens_hemi(  config_lens_hemi_1_1, 
               mesh_configurator(3), 
               name              = lens_hemi_1_1_name,
               inlet_offset      = 4.3,
               outlet_offset     = 17.3,
               wavelength        = 8.661,
               set_hemisphere    = True )


   start = time.time()

   lens_hemi_1_1.process_geometry() # Create the lens geometry 


   print("Geometry computation time: {:.2f} sec".format(time.time() - start) )

   start = time.time()


   lens_hemi_1_1.process_mesh() # Create lens mesh 


   print("Mesh computation time: {:.2f} sec".format( time.time() - start) )

   start = time.time()


   DATASET_PATH = Path('/SAN/uclic/ammdgop/data')              # Dataset path, where all data will be stored - .unv mesh files and solver directories
   UNV_PATH = DATASET_PATH.joinpath( lens_hemi_1_1_name + '.unv')       
   SIF_PATH = Path('entitities.sif')       
   SOLVER_DATA_PATH = DATASET_PATH.joinpath( lens_hemi_1_1_name )       #  solver *.mesh files, sif. file

   lens_hemi_1_1.export_mesh( str( UNV_PATH ) ) # export .unv mesh file, requires conversion to string
   print("Mesh exported to Elmer format: {:.2f} sec".format( time.time() - start) )

   start = time.time()

   convert_mesh( UNV_PATH ) # run elmergrid convert .unv mesh file to elmer format *.mesh files in a directory 
   copy_solver_templates( SOLVER_DATA_PATH )          # copy all the necessary templates to run elmer solver
   copy_sif( SOLVER_DATA_PATH, SIF_PATH )          # copy solver input file

   print("Elmer template copied: {:.2f} sec".format( time.time() - start) )

   run_elmer_solver( SOLVER_DATA_PATH )

   # analysis = Analysis( str(SOLVER_DATA_PATH.joinpath( 'case-40000_t0001.vtu' )) )

   # find_optimisation_target = lambda points, precision, value: sorted(list(filter( lambda x: x[2] == 0.1 and x[0] < 0 and x[1] < 0, points)))

   # optimisation_targets = find_optimisation_target(analysis.points, 2, 0.1)
   # optimisation_target = optimisation_targets[len(optimisation_targets)-1]
   # optimisation_target_id = analysis.points.index(optimisation_targets[len(optimisation_targets)-1])
   # optimisation_target_pressure = analysis._absolute_pressure.GetValue(optimisation_target_id)

   # print("Optimisation target: {} {} {} ".format( optimisation_target_id, optimisation_target, optimisation_target_pressure ) )


for i in range( 0, 16, 1 ):
   compute_kernel_simulation(i)


