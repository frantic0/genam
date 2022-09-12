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
from matrices.quantized_2_2 import quantized_matrix_2_2_0
from genam.lens import Lens
from genam.lens_hemisphere import Lens as Lens_hemi
from genam.configuration.lens import configurator as lens_configurator 
from genam.configuration.mesh import configurator as mesh_configurator
from genam.configuration.source import configurator as source_configurator
from genam.solver import convert_mesh, copy_solver_templates, copy_sif, compile_pressure_reader, run_elmer_solver
from genam.analysis import Analysis


def export_2_2_kernel( quantized_matrix ) -> None:

    lens_config = lens_configurator(quantized_matrix)

    lens_name = f"kernel_{ quantized_matrix.shape[0] }_{ quantized_matrix.shape[1] }_{quantized_matrix[0][0]}_{quantized_matrix[0][1]}_{quantized_matrix[1][0]}_{quantized_matrix[1][1]}"
    
    # # # Create lens with name, bricks ID and mesh configurations 
    lens = Lens_hemi(  lens_config, 
                        mesh_configurator(3), 
                        name              = lens_name,
                        inlet_offset      = 4.3,
                        outlet_offset     = 17.3,
                        wavelength        = 8.661,
                        set_hemisphere    = True )

    start = time.time()
    lens.process_geometry() # Create the lens geometry 
    print("Geometry computation time: {:.2f} sec".format(time.time() - start) )
    
    start = time.time()
    lens.process_mesh() # Create lens mesh 
    print("Mesh computation time: {:.2f} sec".format( time.time() - start) )
    
    start = time.time()
    DATASET_PATH = Path('/SAN/uclic/ammdgop/data')              # Dataset path, where all data will be stored - .unv mesh files and solver directories
    UNV_PATH = DATASET_PATH.joinpath( lens_name + '.unv')       
    SIF_PATH = Path('test_quantised_matrix.sif')       
    SOLVER_DATA_PATH = DATASET_PATH.joinpath( lens_name )       #  solver *.mesh files, sif. file
    lens.export_mesh( str( UNV_PATH ) ) # export .unv mesh file, requires conversion to string
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
    # return ( optimisation_target, optimisation_target_pressure )
    return




if sys.argv == ['']:
   print( 'args list is empty', sys.argv ) 
else: 
   print( 'args', sys.argv )
   PID =  int(sys.argv[2])
   kernel =  int(sys.argv[3])


min, max, step = 0, 16, 1

def nested_for_loop(min, max, step) -> None:
    space = np.array()
    for w in np.arange(min, max, step):  
        for x in np.arange(min, max, step): 
            for y in np.arange(min, max, step):
                for z in np.arange(min, max, step): 
                    space.append([w,x,y,z])
    return space


# Build space with 65536 combinations with cartesian product, equivalent to a nested for-loop of 16**4 
space = itertools.product( list(range(min, max)), repeat=4 )   

# Split space into list of 32 subspaces equally-sized, 2048 combinations (16**3/2) 
subspace = np.array_split( space, 32 ) 

# Select kernel from subspace and reshape it
quantized_matrix = np.reshape( subspace[PID][kernel], (2, 2) )




