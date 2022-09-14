import itertools
import os, sys, time, math
import pandas as pd
import numpy as np
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

# sys.path.insert(0, r'/SAN/uclic/ammdgop/genam/')
# sys.path.insert(0, r'/SAN/uclic/ammdgop/genam/genam/')
# sys.path.insert(0, r'/SAN/uclic/ammdgop/genam/tests/')

# Genam Lens, mesh configurator
from matrices.quantized_1_1 import quantized_matrix_1_1_x
from genam.lens_hemisphere_PML import Lens as Lens_hemi
from genam.configuration.lens import configurator as lens_configurator 
from genam.configuration.mesh import configurator as mesh_configurator
from genam.configuration.source import configurator as source_configurator
from genam.solver import convert_mesh, copy_solver_templates, copy_sif, compile_pressure_reader, write_pressure_sif, run_elmer_solver
from genam.analysis import Analysis


def export_kernel_1_1_( kernel_id, process_id, PRESSURE_DATA_PATH ) -> None:

    lens_config = lens_configurator( quantized_matrix_1_1_x( kernel_id ))

    # lens_name = f"kernel_{ quantized_matrix.shape[0] }_{ quantized_matrix.shape[1] }_{quantized_matrix[0][0]}_{quantized_matrix[0][1]}_{quantized_matrix[1][0]}_{quantized_matrix[1][1]}"
    lens_name = f'K_1_1_{ kernel_id }_P_{ process_id }' 

    # # # Create lens with name, bricks ID and mesh configurations 
    lens = Lens_hemi(  lens_config, 
                        mesh_configurator(3),
                        name              = lens_name,
                        inlet_offset      = 0.001,
                        outlet_offset     = 17.3,
                        wavelength        = 8.661,
                        set_hemisphere    = True,
                        set_PML = False )
    start = time.time()
    lens.process_geometry() # Create the lens geometry 
    print("Geometry computation time: {:.2f} sec".format(time.time() - start) )
    
    start = time.time()
    lens.process_mesh() # Create lens mesh 
    print("Mesh computation time: {:.2f} sec".format( time.time() - start) )
    
    start = time.time()
    DATASET_PATH = Path('/SAN/uclic/ammdgop/data')              # Dataset path, where all data will be stored - .unv mesh files and solver directories
    UNV_PATH = DATASET_PATH.joinpath( lens_name + '.unv')       
    # SIF_PATH = Path('entities-1-1.sif')       
    SOLVER_DATA_PATH = DATASET_PATH.joinpath( lens_name )       #  solver *.mesh files, sif. file
    lens.export_mesh( str( UNV_PATH ) ) # export .unv mesh file, requires conversion to string
    print("Mesh exported to Elmer format: {:.2f} sec".format( time.time() - start) )
    
    start = time.time()
    convert_mesh( UNV_PATH ) # run elmergrid convert .unv mesh file to elmer format *.mesh files in a directory 
    copy_solver_templates( SOLVER_DATA_PATH )          # copy all the necessary templates to run elmer solver
    
    # copy_sif( SOLVER_DATA_PATH, SIF_PATH )          # copy solver input file

    write_pressure_sif( SOLVER_DATA_PATH, PRESSURE_DATA_PATH, process_id)
    
    print("Elmer template copied: {:.2f} sec".format( time.time() - start) )
    
    run_elmer_solver( SOLVER_DATA_PATH )
    
    return




if sys.argv == ['']:
   print( 'args list is empty', sys.argv ) 
   PID = 1
   file_complex_pressure_map = "p_8_8.out"
else: 
   print( 'args', sys.argv )
   PID =  int(sys.argv[2])
   file_complex_pressure_map = int(sys.argv[3])
   
#    kernel_id = int(sys.argv[3])





# for brick_ID in range(16):
for brick_ID in range(2):
    export_kernel_1_1_(brick_ID, PID, file_complex_pressure_map)

