import os, sys, time, math
import pandas as pd
from pathlib import Path


# Genam Lens, mesh configurator
from genam.lens import Lens
from genam.configuration.lens import configurator as lens_configurator 
from genam.configuration.mesh import configurator as mesh_configurator
from genam.solver import convert_mesh, copy_solver_templates, copy_sif, run_elmer_solver
from genam.analysis import Analysis

def compute_lens_optimisation_objective( quantized_matrix, iteration ):
    lens_config = lens_configurator(quantized_matrix)
    print(quantized_matrix)
    print(lens_config)
    lens_name = f"quantized_matrix_{ quantized_matrix.shape[0] }_{ quantized_matrix.shape[1] }_{iteration}"
    print(lens_name)
    # # # Create lens with name, bricks ID and mesh configurations 
    lens = Lens( lens_config, mesh_configurator(3), name = lens_name  )
    # # start = time.time()
    lens.process_geometry() # Create the lens geometry 
    # # print("Geometry computation time: {:.2f} sec".format(time.time() - start) )
    # # start = time.time()
    lens.process_mesh() # Create lens mesh 
    # # print("Mesh computation time: {:.2f} sec".format( time.time() - start) )
    # # start = time.time()
    DATASET_PATH = Path('/SAN/uclic/ammdgop/data')              # Dataset path, where all data will be stored - .unv mesh files and solver directories
    UNV_PATH = DATASET_PATH.joinpath( lens_name + '.unv')       
    SIF_PATH = Path('test_quantised_matrix.sif')       
    SOLVER_DATA_PATH = DATASET_PATH.joinpath( lens_name )       #  solver *.mesh files, sif. file
    lens.export_mesh( str( UNV_PATH ) ) # export .unv mesh file, requires conversion to string
    # print("Mesh exported to Elmer format: {:.2f} sec".format( time.time() - start) )
    # start = time.time()
    convert_mesh( UNV_PATH ) # run elmergrid convert .unv mesh file to elmer format *.mesh files in a directory 
    copy_solver_templates( SOLVER_DATA_PATH )          # copy all the necessary templates to run elmer solver
    copy_sif( SOLVER_DATA_PATH, SIF_PATH )          # copy solver input file
    # print("Elmer template copied: {:.2f} sec".format( time.time() - start) )
    run_elmer_solver( SOLVER_DATA_PATH )
    analysis = Analysis( str(SOLVER_DATA_PATH.joinpath( 'case-40000_t0001.vtu' )) )
    find_optimisation_target = lambda points, precision, value: sorted(list(filter( lambda x: x[2] == 0.1 and x[0] < 0 and x[1] < 0, points)))
    optimisation_targets = find_optimisation_target(analysis.points, 2, 0.1)
    optimisation_target = optimisation_targets[len(optimisation_targets)-1]
    optimisation_target_id = analysis.points.index(optimisation_targets[len(optimisation_targets)-1])
    optimisation_target_pressure = analysis._absolute_pressure.GetValue(optimisation_target_id)
    return ( optimisation_target, optimisation_target_pressure )
