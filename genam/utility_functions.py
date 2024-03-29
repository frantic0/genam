import sys
import salome
import numpy as np
import time, os, shutil
from pathlib import Path
# import export_solver_input_file
# from export_solver_input_file import export_parameterisable_solver_input_file

import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS

def sketch_to_volume(geom_builder, sketch_obj, thickness, rotation=None, translation=None):
  """
  Inputs
  
    sketch: 2d sketch of the object
    thickness: thickness of volume in z axis
    rotation: provide a list of tuples with (axis, angle) as a tuple i.e. (x, 90), in the order you want to rotate in x axis
  
  Returns
     
   sketch_rotation: sketch to 3d object
  
  """
  try:

    sketch_face = geom_builder.MakeFaceWires( [sketch_obj], 1) # make sketch object

    sketch_volume = geom_builder.MakePrismDXDYDZ(sketch_face, 0, 0, thickness) # extrude
    
    temp = sketch_volume
    
    if rotation is not None:
      for (axis, angle) in rotation:
        sketch_rotation = geom_builder.MakeRotation(temp, axis, angle * math.pi / 180.0) # rotate
        temp = sketch_rotation

    if translation is not None:
      sketch_rotation = geom_builder.MakeTranslation(sketch_rotation, translation[0], translation[1], translation[2])
      
    return sketch_rotation

  except:
    print("Error extruding in sketch_to_volume: {} {} {}".format( sketch_obj, thickness ) )

    return None


def copy_solver_templates(  path,
                            start_frequency=40000,  
                            end_frequency=0, 
                            step=0 ): 

  # TODO validate input and that solver directory is on the right place 
  # Get path to '../../solver/' 
  solver_templates_path = str( Path( os.path.dirname(os.path.realpath(__file__)) ).parent.joinpath('solver') )
  
  # Get path to user-defined data directory
  user_defined_path = os.path.splitext(path)[0]

  print('Copying solver templates to directory:') 
  for fileName in os.listdir(solver_templates_path):
    source = Path(solver_templates_path).joinpath(fileName)
    destination = Path(user_defined_path).joinpath(fileName) 
    
    if os.path.isfile(source):
      shutil.copy(source, destination)
      print('copied {} {}'.format(source, destination) )

  # NOTE: Needs refactor - if optional arguments
  if end_frequency != 0 and step !=0 : 
    for frequency in range( start_frequency, end_frequency + step, step ):
      export_parameterisable_solver_input_file( user_defined_path, frequency )
  else:  
      export_parameterisable_solver_input_file( user_defined_path, start_frequency )
        
  
  
def copy_sif( path, sif_path="" ):   
  print('Copying SIF to directory:') 
  if sif_path != "":
    sif_path = str( Path( os.path.dirname(os.path.realpath(__file__)) ).parent.joinpath('tests').joinpath('sif').joinpath(sif_path) )
    if os.path.isfile(sif_path):
      shutil.copy(sif_path, path)




# TODO validate input 
def convert_mesh(filename, options=""):
  """
    Input
      filename: name of the .unv file exported by Salome
      parallel: mesh partitioning for parallel ElmerSolver runs

    Output
      .unv to *.mesh (Elmer format)

    -partition int[3]   : the mesh will be partitioned in cartesian main directions
    -partorder real[3]  : in the 'partition' method set the direction of the ordering
    -partcell int[3]    : the mesh will be partitioned in cells of fixed sizes
    -partcyl int[3]     : the mesh will be partitioned in cylindrical main directions
    -metis int          : mesh will be partitioned with Metis using mesh routines
    -metiskway int      : mesh will be partitioned with Metis using graph Kway routine
    -metisrec int       : mesh will be partitioned with Metis using graph Recursive routine
    -metiscontig        : enforce that the metis partitions are contiguous
    -metisseed          : random number generator seed for Metis algorithms
    -partdual           : use the dual graph in partition method (when available)
    -halo               : create halo for the partitioning for DG
    -halobc             : create halo for the partitioning at boundaries only
    -haloz / -halor     : create halo for the the special z- or r-partitioning-halogreedy

  """
  
  if os.name == 'nt':
    os.system('cmd /c "ElmerGrid 8 2 {} -autoclean {}"'.format(filename, options))
  elif os.name == 'posix': 
    os.system('ElmerGrid 8 2 {} -autoclean {}'.format(filename, options))  
  else: 
    raise NotImplementedError('operating system not support') 


def export_parameterisable_solver_input_file_0( path, frequency):
  """
    Input

    Output
      .unv to *.mesh (Elmer w)
  """

  os.chdir(path)
 
  sif = f'''
Check Keywords "Warn"
  INCLUDE mesh.names
! location of mesh files
Header
  CHECK KEYWORDS Warn
  Mesh DB "." "."
  Include Path ""
  Results Directory ""
  $ rho0 = 1.205                     ! Medium (Air) Equilibrium Density
  $ c0 = -343.                       ! Medium Sound Phase Speed
  $ f = 40000                        ! Source Frequency
  $ p = 1.205                        ! Medium (Air) Equilibrium Density
  $ U = 10                           ! Source Surface Velocity (Orthogonal to surface)
  ! $freqVec = vector(100,1800,50)
End

! general information that is not specific to a particular Helmholtz
Simulation
  Max Output Level = 5
  Coordinate System = Cartesian
  Coordinate Mapping(3) = 1 2 3
  Coordinate Scaling = Real 0.001   ! set dimensions in mm (instead of m)
  !  Simulation Type = Scanning     ! set Frequency sweeps
  Simulation Type = Steady state    ! set Stationary problem
  Steady State Max Iterations = 1
  Output Intervals = 1
  Timestepping Method = BDF
  BDF Order = 1
  Post File = case-{frequency}.vtu  ! Export VTU file for visualization in Paraview
End

Constants
  Gravity(4) = 0 -1 0 9.82
  Stefan Boltzmann = 5.67e-08
  Permittivity of Vacuum = 8.8542e-12
  Boltzmann Constant = 1.3807e-23
  Unit Charge = 1.602e-19
End

! %%%%%%%%%%%%
! %% BODY SECTIONS %%
! %% body sections associate each body with an equation set, material properties, body forces, and initial conditions 
! %% by referring to definitions given in a specified equation section, material section, body force section, and initial condition section. 
! %%%%%%%%%%%%

Body 1
  Target Bodies(1) = $pml_inlet
  Name = "pml_inlet"
  Equation = 1
  Material = 1
End

Body 2
  Target Bodies(1) = $brick
  Name = "brick"
  Equation = 1
  Material = 2
End

Body 3
  Target Bodies(1) = $air
  Name = "air"
  Equation = 1
  Material = 1
  Body Force = 1                    ! Force applied to Air body, with scalars apply 
End

Body 4
  Target Bodies(1) = $pml_outlet
  Name = "pml_outlet"
  Equation = 1
  Material = 1
End


! %%%%%%%%%%%%
! %% SOLVERS SECTIONS %%
! %% 
! %%%%%%%%%%%%


! Export the Sound Pressure Level with the Pressure Wave variables in vtu file (see below body force)
Solver 1
  Equation = Helmholtz Equation
  Procedure = "HelmholtzSolve" "HelmholtzSolver"
  Variable = -dofs 2 Pressure Wave
  Nonlinear Update Exported Variables = Logical True
  Exported Variable 1 = Pabs
  Exported Variable 2 = SPL
  Exported Variable 3 = Phase
  Exported Variable 4 = PhaseAtan2
  Exec Solver = Always
  Stabilize = True
  Bubbles = False
  Lumped Mass Matrix = False
  Optimize Bandwidth = True
  Steady State Convergence Tolerance = 1.0e-5
  Nonlinear System Convergence Tolerance = 1.0e-7
  Nonlinear System Max Iterations = 20
  Nonlinear System Newton After Iterations = 3
  Nonlinear System Newton After Tolerance = 1.0e-3
  Nonlinear System Relaxation Factor = 1
  Linear System Solver = Iterative
  Linear System Iterative Method = BiCGStabl
  Linear System Max Iterations = 1000
  Linear System Convergence Tolerance = 1.0e-10
  BiCGstabl polynomial degree = 2
  ! Linear System Preconditioning = ILU0
  ! Linear System Preconditioning = ILU1
  ! Linear System Preconditioning = ILU2
  Linear System Preconditioning = ILUT
  Linear System ILUT Tolerance = 1.0e-3
  Linear System Abort Not Converged = False
  Linear System Residual Output = 10
  Linear System Precondition Recompute = 1
End

! ! “Flux Computation” - ElmerModelsManual.pdf
! Solver 2
!   Equation = "flux compute 1"
!   Procedure = "FluxSolver" "FluxSolver"
!   Calculate Flux = Logical True
!   Target Variable = String "Pressure Wave 1"
!   Flux Coefficient = String "Cv"
!   Linear System Solver = Direct
!   Linear System Direct Method = Banded
! End

! Solver 3
!   Equation = "flux compute 2"
!   Procedure = "FluxSolver" "FluxSolver"
!   Calculate Flux = Logical True
!   Target Variable = String "Pressure Wave 2"
!   Flux Coefficient = String "Cv"
!   Linear System Solver = Direct
!   Linear System Direct Method = Banded
! End

! Solver 4
!   Exec Solver = After Timestep
!   Equation = "Grad compute 1"
!   Procedure = "FluxSolver" "FluxSolver"
!   Calculate Grad = True
!   Target Variable = Pressure Wave 1
!   Linear System Solver = Iterative
!   Linear System Iterative Method = BiCGStab
!   Linear System Preconditioning = None
!   Linear System Max Iterations = 100
!   Linear System Convergence Tolerance = 1.0e-10
! End


! Solver 5
!   Exec Solver = After Timestep
!   Equation = "Grad compute 2"
!   Procedure = "FluxSolver" "FluxSolver"
!   Calculate Grad = True
!   Target Variable = Pressure Wave 2
!   Linear System Solver = Iterative
!   Linear System Iterative Method = BiCGStab
!   Linear System Preconditioning = None
!   Linear System Max Iterations = 100
!   Linear System Convergence Tolerance = 1.0e-10
! End

! Solver 6
!   Exec Solver = after Timestep
!   Equation = "SaveScalars"
!   Procedure = "SaveData" "SaveScalars"  
!   Filename = File "SPLmean.dat"
!   Variable 1 = "Pressure Wave 1"
!   Operator 1 = "boundary mean"
!   Variable 2 = "Pressure Wave 2"
!   Operator 2 = "boundary mean"
!   Variable 3 = "Pressure Wave 1 Grad 1"
!   Operator 3 = "boundary mean"
!   Variable 4 = "Pressure Wave 2 Grad 1"
!   Operator 4 = "boundary mean"
!   Variable 5 = "Pressure Wave 1 Grad 2"
!   Operator 5 = "boundary mean"
!   Variable 6 = "Pressure Wave 2 Grad 2"
!   Operator 6 = "boundary mean"
!   Variable 7 = "Pressure Wave 1 Grad 3"       ! Only exists for 3D
!   Operator 7 = "boundary mean"
!   Variable 8 = "Pressure Wave 2 Grad 3"
!   Operator 8 = "boundary mean"
!   ! Want to append to file?
!   File Append = Logical True
! End



! Solver 7
!   Equation = Result Output
!   Procedure = "ResultOutputSolve" "ResultOutputSolver"
!   Save Geometry Ids = False
!   Output File Name = "case-{frequency}"
!   Output Format = Vtu
!   Scalar Field 2 = Pressure wave 2
!   Scalar Field 1 = Pressure wave 1
!   Vector Field 1 = Pressure wave 2 flux
!   Vector Field 2 = Pressure wave 1 flux
!   Vector Field 1 = Pressure wave 2 grad
!   Vector Field 2 = Pressure wave 1 grad
!   Scalar Field 3 = "Pabs"
!   Scalar Field 4 = "SPL"
!   Scalar Field 5 = "Phase"
!   Scalar Field 6 = "PhaseAtan2"
! End


! %%%%%%%%%%%%
! %% EQUATION SECTIONS %%
! %% 
! %%%%%%%%%%%%



Equation 1
  Name = "Helmholtz"
  ! Frequency = Variable time; Real MATC "freqVec(tx - 1)"
Angular Frequency = $ 2.0 * pi * {frequency}
  Active Solvers(1) = 1
End

! Equation 2
!   Name = "Result Output EQ"
!   Active Solvers(1) = 7
! End



! %%%%%%%%%%%%
! %% MATERIAL SECTIONS %%
! %% 
! %%%%%%%%%%%%



! %%%%%%%%%
! %% Air %%
! %%%%%%%%%

Material 1 
  Name = "Air (room temperature)"
  Relative Permittivity = 1.00059
  Heat Conductivity = 0.0257
  Sound speed = 343.0
  Density = Real MATC "p"
  Porosity Model = Always saturated
  Heat Capacity = 1005.0
  Viscosity = 1.983e-5
  Heat expansion Coefficient = 3.43e-3
  !  Cv = Real $ 1/(1.205 * 2.0 * pi * {frequency} )
End

! %%%%%%%%%%%%%
! %% Plastic %%
! %%%%%%%%%%%%%

Material 2 
  Name = "Plastic"
  Heat expansion Coefficient = 7.0e-5
  Heat Conductivity = 0.18
  Sound speed = 2750
  Heat Capacity = 1470
  Density = 1190
  Poisson ratio = 0.35
  Youngs modulus = 3.2e9
End


Body Force 1
  Name = "Pabs"
Pabs = Variable Pressure Wave 1, Pressure Wave 2 
      Real MATC "sqrt(tx(0)^2+tx(1)^2)"
  Name = "SPL" 
SPL = Variable Pressure Wave 1, Pressure Wave 2
      Real MATC "20*log(((sqrt(tx(0)^2+tx(1)^2))/(sqrt(2)*20e-6)))"
  Name = "Phase"
Phase = Variable Pressure Wave 1, Pressure Wave 2
      Real MATC "atan(tx(0)/(tx(1)))"
  Name = "PhaseAtan2"    
PhaseAtan2 = Variable Pressure Wave 1, Pressure Wave 2
      Real MATC "atan2(tx(0),tx(1))"
End



! BOUNDARY CONDITIONS
! 
! the usual BC for the Helmholtz PDE is to give the flux on the boundary
! also define the Dirichlet boundary conditions for all the primary field variables 
! -- in our case the real component of pressure, Pressure 1
! we can also define the Sommerfeldt or far field BC
! Elmer mesh files (mesh.*) contain information on how the boundaries of the bodies are divided into parts distinguished by their own boundary numbers
! Target Boundaries is used to list the boundary numbers that form the domain for imposing the boundary condition
! mesh.names
!
! ----- names for bodies -----
! $ pml_inlet = 1
! $ brick = 2
! $ air = 3
! $ pml_outlet = 4
! ----- names for boundaries -----
! $ top_bottom_walls = 1
! $ inlet = 2
! $ outlet = 3
! $ brick_faces = 4
! $ brick_left = 5
! $ brick_front = 6
! $ brick_back = 7
! $ brick_right = 8
! $ left = 9
! $ front = 10
! $ back = 11
! $ right = 12


! %%%%%%%%%%%%
! %% Inlet  %%
! %%%%%%%%%%%%


! Boundary condition at the inlet ($inlet = 2) for variable Pressure
! Pressure i Real - Dirichlet boundary condition for real and imaginary parts of the variable. 
! Here the values i= 1, 2 correspond to the real and imaginary parts of the unknown field.

Boundary Condition 1
  Target Boundaries(1) = $ inlet
  Name = "In"
  Plane Wave BC = True ! Automatically sets the boundary conditions assuming outgoing plane waves
$p0=1.0
$k1=0.0
$k2=0.0
$k3=1.0
  Pressure Wave 1 = Variable Coordinate 
    Real MATC "p0 * cos(k1*tx(0) + k2*tx(1) + k3*tx(2))"
  Pressure Wave 2 = 0
  ! Wave Impedance 1 = $ c0 !
  ! We want to save data at the inlet 
  Save Scalars = Logical True
End

! %%%%%%%%%%%
! %% Walls %% 
! %%%%%%%%%%%


! Wave Flux 1,2 Real
! Values i= 1, 2 correspond to the real and imaginary parts of the boundary flux.
! Make boundaries of the brick rigid, 
! by imposing the normal component particle velocity null at the boundaries

Boundary Condition 2
Target Boundaries(5) = $ brick_faces brick_left brick_right brick_front brick_back
  Name = "Wall"
  Wave Flux 1 = 0
  Wave Flux 2 = 0
End

! %%%%%%%%%%%%
! %% Air    %% 
! %%%%%%%%%%%%

! Wave Impedance 1,2 Real — used to define the real and imaginary parts of the complex-valued quantity Z in the Sommerfeldt or far field boundary condition.
! which may be defined by the user. Incoming and outgoing waves may be approximated by setting Z = ±c, respectively.
! Here the values i= 1, 2 correspond to the real and imaginary parts of Z.

Boundary Condition 3
  Target Boundaries(1) = $ outlet 
  Name = "Air"
  Wave Impedance 1 = $ c0
  Save Scalars = Logical True
End

Boundary Condition 4
  Target Boundaries(1) = $ top_bottom_walls 
  Name = "PML"
  Wave Impedance 1 = $ c0
  Save Scalars = Logical True
End

! %%%%%%%%%%%
! %%  PBC  %%
! %%%%%%%%%%%

Boundary Condition 5 
  Target Boundaries(1) = $ left 
End

Boundary Condition 6 
  Target Boundaries(1) = $ right 
  Periodic BC = 5
End

Boundary Condition 7 
  Target Boundaries(1) = $ front 
End

Boundary Condition 8 
  Target Boundaries(1) = $ back 
  Periodic BC = 7
End
  '''.format(frequency)


  # print(sif)
  file = open(f"case-{frequency}.sif","w")
  file.write(sif)
  file.close()
  



def export_parameterisable_solver_input_file( path, frequency ):
  """
  Input


  Output

    .unv to *.mesh (Elmer w)
  
  """
  
  sif = f'''

Check Keywords "Warn"
  INCLUDE mesh.names
! location of mesh files

Header
  Mesh DB "." "."
  Include Path ""
  Results Directory ""
  $ rho0 = 1.205                     ! Medium (Air) Equilibrium Density
  $ c0 = -343                        ! Medium Sound Phase Speed
  $ f = {frequency}                  ! Source Frequency
  $ p = 1.205                        ! Medium (Air) Equilibrium Density
  $ U = 10                           ! Source Surface Velocity
  ! $freqVec = vector(100,1800,50)
End

! general information that is not specific to a particular Helmholtz
Simulation
  Max Output Level = 5
  Coordinate System = Cartesian
  Coordinate Mapping(3) = 1 2 3
  Coordinate Scaling = Real 0.001   ! set dimensions in mm (instead of m)
  !  Simulation Type = Scanning     ! set Frequency sweeps
  Simulation Type = Steady state    ! set Stationary problem
  Steady State Max Iterations = 1
  Output Intervals = 1
  Timestepping Method = BDF
  BDF Order = 1
  Post File = case-{frequency}.vtu  ! set VTU file Export for visualization in Paraview
End

Constants
  Gravity(4) = 0 -1 0 9.82
  Stefan Boltzmann = 5.67e-08
  Permittivity of Vacuum = 8.8542e-12
  Boltzmann Constant = 1.3807e-23
  Unit Charge = 1.602e-19
End

! %%%%%%%%%%%%
! %% BODY SECTIONS %%
! %% body sections associate each body with an equation set, material properties, body forces, and initial conditions 
! %% by referring to definitions given in a specified equation section, material section, body force section, and initial condition section. 
! %%%%%%%%%%%%

Body 1
  Target Bodies(1) = $air
  Name = "air"
  Equation = 1
  Material = 1
  Body Force = 1 ! Force applied to Air body, with scalars apply 
End







Body Force 1
  Name = "Pabs"
Pabs = Variable Pressure Wave 1, Pressure Wave 2 
      Real MATC "sqrt(tx(0)^2+tx(1)^2)"
  Name = "SPL" 
SPL = Variable Pressure Wave 1, Pressure Wave 2
      Real MATC "20*log(((sqrt(tx(0)^2+tx(1)^2))/(sqrt(2)*20e-6)))"
  Name = "Phase"
Phase = Variable Pressure Wave 1, Pressure Wave 2
      Real MATC "atan(tx(0)/(tx(1)))"
  Name = "PhaseAtan2"    
PhaseAtan2 = Variable Pressure Wave 1, Pressure Wave 2
      Real MATC "atan2(tx(0),tx(1))"
End

! Body 3 (Air) has Body Force 1 associated 

Body 2
  Target Bodies(1) = $ lens
  Name = "lens"
  Equation = 1
  Material = 2
End

Body 3
  Target Bodies(1) = $pml_inlet
  Name = "pml_inlet"
  Equation = 1
  Material = 1
End

Body 4
  Target Bodies(1) = $ pml_outlet
  Name = "pml_outlet"
  Equation = 1
  Material = 1
End


! Export the Sound Pressure Level with the Pressure Wave variables in vtu file (see below body force)
Solver 1
  Equation = Helmholtz Equation
  Procedure = "HelmholtzSolve" "HelmholtzSolver"
  Variable = -dofs 2 Pressure Wave
  Nonlinear Update Exported Variables = Logical True
  Exported Variable 1 = Pabs
  Exported Variable 2 = SPL
  Exported Variable 3 = Phase
  Exported Variable 4 = PhaseAtan2
  Exec Solver = Always
  Stabilize = True
  Bubbles = False
  Lumped Mass Matrix = False
  Optimize Bandwidth = True
  
  Steady State Convergence Tolerance = 1.0e-5
  
  Nonlinear System Convergence Tolerance = 1.0e-7
  ! Nonlinear System Max Iterations = 1
  Nonlinear System Max Iterations = 20
  Nonlinear System Newton After Iterations = 3
  Nonlinear System Newton After Tolerance = 1.0e-3
  Nonlinear System Relaxation Factor = 1



  ! ! ! ! DIRECT LINEAR SOLVER CONFIGURATION ! ! ! ! ! 
  ! Linear System Solver = Direct
  ! Linear System Direct Method = MUMPS   ! (serial and parallel)
  ! Linear System Direct Method = umfpack ! (serial only)
  ! Linear System Direct Method = Banded  ! (serial only)


  ! ! ! ! ITERATIVE LINEAR SOLVER CONFIGURATION ! ! ! ! ! 
  ! Linear System Solver = Iterative
  ! Linear System Iterative Method = CG
  ! Linear System Iterative Method = CGS
  
  ! Linear System Iterative Method = BiCGStabl
  ! BiCGstabl polynomial degree = 2
  ! BiCGstabl polynomial degree = 6
  ! BiCGstabl polynomial degree = 10
  
  ! Linear System Iterative Method = BiCGStab
  ! Linear System Iterative Method = GCR
  ! Linear System Iterative Method = TFQMR
  
  ! Linear System Iterative Method = GMRES
  ! Linear System GMRES Restart = 10
  
  ! Linear System Iterative Method = Idrs
  ! Idrs Parameter = 4
  
  ! Linear System Max Iterations = 10000
  Linear System Max Iterations = 100000
  Linear System Convergence Tolerance = 1.0e-10


  ! ! ! ! PRECONDITIONER CONFIGURATION !  
  ! Linear System Preconditioning = None
  ! Linear System Preconditioning = ILU0
  ! Linear System Preconditioning = ILU1
  ! Linear System Preconditioning = ILU2
  ! Linear System Preconditioning = ILUT
  ! Linear System ILUT Tolerance = 1.0e-3

  ! Linear System Preconditioning = Diagonal
  Linear System Preconditioning = Multigrid
  Linear System Abort Not Converged = True
  Linear System Residual Output = 10
  Linear System Precondition Recompute = 1
  

  ! ! ! ! INTERNAL MULTIGRID SOLVER CONFIGURATION !  
  ! Linear System Solver = Multigrid
  ! Linear System Iterative Method = BoomerAMG
  ! BoomerAMG Relax = 0-9
  ! BoomerAMG Coarsen = 0-9
  ! BoomerAMG Num Sweeps = 2 ! sets the number of sweeps on the finest level (default value = 1)
  ! Boomeramg Max Levels = 50 ! sets maximum number of MG levels (default value = 25)
  ! BoomerAMG Interpolation Type = 4 ! [1-13] Sets parallel interpolation operator. Possible options are

  ! MG Equal Split = False ! [False] to enable the use of user-supplied meshes
  ! MG Levels = 4
  ! MG Mesh Name = xpto
  ! MG Max Iterations = 100000
  ! MG Convergence Tolerance = 1.0e-10
  ! MG Smoother = BiCGStab
  ! MG Recompute Projector = True               ! This flag may be used to enforce recomputation of the projector each time the algebraic multigrid
solver is called. The default is False as usually the same projector is appropriate for all computations.
  ! MG Eliminate Dirichlet = True               ! At the highest level the fixed nodes may all be set to be coarse since their value is not affected by the
lower levels. The default is True
  ! MG Eliminate Dirichlet Limit = Real         ! Gives the maximum fraction of non-diagonal entries for a Dirichlet node.
  ! MG Smoother = String                        ! In addition to the selection for the GMG option sor (symmetric over relaxation) is possible.
  ! MG SOR Relax = String !                     ! The relaxation factor for the SOR method. The default is 1.
  ! MG Strong Connection Limit = Real !         ! The coefficient c in the coarsening scheme. Default is 0.25.
  ! MG Positive Connection Limit = Real !       ! The coefficient c+ in the coarsening scheme. Default is 1.0.
  ! MG Projection Limit = Real !                ! The coefficient cw in the truncation of the small weights. The default is 0.1.
  ! MG Direct Interpolate = Logical !           ! Chooses between direct and standard interpolation. The default is False.
  ! MG Direct Interpolate Limit = Integer       ! The standard interpolation may also be applied to nodes with only a small number of coarse connection. This gives the smallest number of nodes for which direct interpolation is used.
  ! MG Cluster Size = Integer                   ! The desired choice of the cluster. Possible choices are 2,3,4,5,. . . and zero which corresponds to the
maximum cluster.
  ! MG Cluster Alpha = Real                     ! In the clustering algorithm the coarse level matrix is not optimal for getting the correct convergence. Tuning this value between 1 and 2 may give better performance.
  ! MG Strong Connection Limit = Real           ! This is used similarly as in the AMG method except it is related to positive and negative connections
alike.
  ! MG Strong Connection Minimum = Integer      ! If the number of strong connections with the given limit is
End


! Flux Computation - ElmerModelsManual.pdf
! Solver 2
!   Equation = "flux compute 1"
!   Procedure = "FluxSolver" "FluxSolver"
!   Calculate Flux = Logical True
!   Target Variable = String "Pressure Wave 1"
!   Flux Coefficient = String "Cv"
!   Linear System Solver = Direct
!   Linear System Direct Method = Banded
! End

! Solver 3
!   Equation = "flux compute 2"
!   Procedure = "FluxSolver" "FluxSolver"
!   Calculate Flux = Logical True
!   Target Variable = String "Pressure Wave 2"
!   Flux Coefficient = String "Cv"
!   Linear System Solver = Direct
!   Linear System Direct Method = Banded
! End

! Solver 4
!   Exec Solver = After Timestep
!   Equation = "Grad compute 1"
!   Procedure = "FluxSolver" "FluxSolver"
!   Calculate Grad = True
!   Target Variable = Pressure Wave 1
!   Linear System Solver = Iterative
!   Linear System Iterative Method = BiCGStab
!   Linear System Preconditioning = None
!   Linear System Max Iterations = 100
!   Linear System Convergence Tolerance = 1.0e-10
! End


! Solver 5
!   Exec Solver = After Timestep
!   Equation = "Grad compute 2"
!   Procedure = "FluxSolver" "FluxSolver"
!   Calculate Grad = True
!   Target Variable = Pressure Wave 2
!   Linear System Solver = Iterative
!   Linear System Iterative Method = BiCGStab
!   Linear System Preconditioning = None
!   Linear System Max Iterations = 100
!   Linear System Convergence Tolerance = 1.0e-10
! End

! Solver 6
!   Exec Solver = after Timestep
!   Equation = "SaveScalars"
!   Procedure = "SaveData" "SaveScalars"  
!   Filename = File "SPLmean.dat"
!   Variable 1 = "Pressure Wave 1"
!   Operator 1 = "boundary mean"
!   Variable 2 = "Pressure Wave 2"
!   Operator 2 = "boundary mean"
!   Variable 3 = "Pressure Wave 1 Grad 1"
!   Operator 3 = "boundary mean"
!   Variable 4 = "Pressure Wave 2 Grad 1"
!   Operator 4 = "boundary mean"
!   Variable 5 = "Pressure Wave 1 Grad 2"
!   Operator 5 = "boundary mean"
!   Variable 6 = "Pressure Wave 2 Grad 2"
!   Operator 6 = "boundary mean"
!   Variable 7 = "Pressure Wave 1 Grad 3"       ! Only exists for 3D
!   Operator 7 = "boundary mean"
!   Variable 8 = "Pressure Wave 2 Grad 3"
!   Operator 8 = "boundary mean"
!   ! Want to append to file?
!   File Append = Logical True
! End



! Solver 7
!   Equation = Result Output
!   Procedure = "ResultOutputSolve" "ResultOutputSolver"
!   Save Geometry Ids = False
!   Output File Name = "case-40000"
!   Output Format = Vtu
!   Scalar Field 2 = Pressure wave 2
!   Scalar Field 1 = Pressure wave 1
!   Vector Field 1 = Pressure wave 2 flux
!   Vector Field 2 = Pressure wave 1 flux
!   Vector Field 1 = Pressure wave 2 grad
!   Vector Field 2 = Pressure wave 1 grad
!   Scalar Field 3 = "Pabs"
!   Scalar Field 4 = "SPL"
!   Scalar Field 5 = "Phase"
!   Scalar Field 6 = "PhaseAtan2"
! End


! %%%%%%%%%%%%
! %% EQUATION SECTIONS %%
! %% 
! %%%%%%%%%%%%

Equation 1
  Name = "Helmholtz"
Angular Frequency = $ 2.0 * pi * f
  Active Solvers(1) = 1
End


! Equation 1
!   Name = "Helmholtz"
!   ! Frequency = Variable time; Real MATC "freqVec(tx - 1)"
!   Angular Frequency = $ 2.0 * pi * {frequency}
!   Active Solvers(6) = 1 2 3 4 5 6
! End

! Equation 2
!   Name = "Result Output EQ"
!   Active Solvers(1) = 7
! End



! %%%%%%%%%%%%
! %% MATERIAL SECTIONS %%
! %% 
! %%%%%%%%%%%%



! %%%%%%%%%
! %% Air %%
! %%%%%%%%%

Material 1
  Name = "Air (room temperature)"
  Relative Permittivity = 1.00059
  Heat Conductivity = 0.0257
  Sound speed = 343.0
  Density = Real MATC "p"
  Porosity Model = Always saturated
  Heat Capacity = 1005.0
  Viscosity = 1.983e-5
  Heat expansion Coefficient = 3.43e-3
End


! Material 1 
!   Name = "Air (room temperature)"
!   Viscosity = 1.983e-5
!   Heat expansion Coefficient = 3.43e-3
!   Heat Conductivity = 0.0257
!   Relative Permittivity = 1.00059
!   Sound speed = 343.0
!   Heat Capacity = 1005.0
!   Density = 1.205
!   ! Cv = Real $ 1/(1.205 * 2.0 * pi * 40000 )
! End

! %%%%%%%%%%%%%
! %% Plastic %%
! %%%%%%%%%%%%%

Material 2 
  Name = "Plastic"
  Heat expansion Coefficient = 7.0e-5
  Heat Conductivity = 0.18
  Sound speed = 2750
  Heat Capacity = 1470
  Density = 1190
  Poisson ratio = 0.35
  Youngs modulus = 3.2e9
End



! BOUNDARY CONDITIONS
! 
! the usual BC for the Helmholtz PDE is to give the flux on the boundary
! also define the Dirichlet boundary conditions for all the primary field variables -- in our case the real component of pressure, Pressure 1
! can also define the Sommerfeldt or far field BC
! Elmer mesh files (mesh.*) contain information on how the boundaries of the bodies are divided into parts distinguished by their own boundary numbers
! Target Boundaries is used to list the boundary numbers that form the domain for imposing the boundary condition
! mesh.names
!

! At the inlet boundary condition, which corresponds to ! $ inlet = 2

Boundary Condition 1
  Target Boundaries(1) = $ inlet
  Name = "In"
  Plane Wave BC = False ! Automatically sets the boundary conditions assuming outgoing plane waves
$p0=100.0
$k1=1.0
$k2=0.0
$k3=1.0
  ! Pressure Wave 1 = 100
  Pressure Wave 2 = 0
  Pressure Wave 1 = Variable Coordinate 
    Real MATC "p0 * cos(k1*tx(0) + k2*tx(1) + k3*tx(2))"
  ! Wave Impedance 1 = $ c0 !
  ! Pressure Wave 1 = 1
  ! Wave Flux 1 = Variable time; Real MATC "2 * pi * f * p * U"
  ! Wave Flux 2 = 0
  ! We want to save data at the inlet 
  ! TODO how do we save data at the outlet
  Save Scalars = Logical True
End

! %%%%%%%%%%%%
! %% Air    %% 
! %%%%%%%%%%%%

Boundary Condition 2
Target Boundaries(1) = $ outlet 
  Name = "outlet"
  Wave Impedance 1 = $ c0
  Wave Impedance 2 = 0  
  Save Scalars = Logical True
End


! %%%%%%%%%%%
! %%  PBC  %%
! %%%%%%%%%%%

Boundary Condition 3
  Target Boundaries(2) = $ lens_air lens_shell
  Name = "Lens"
  Wave Flux 1 = 0
  Wave Flux 2 = 0
End

Boundary Condition 4 
Target Boundaries(1) = $ front
  Wave Impedance 1 = $ c0
  Wave Impedance 2 = 0
End

Boundary Condition 5 
  Target Boundaries(1) = $ back
  Periodic BC = 4
End

Boundary Condition 6 
Target Boundaries(1) = $ right
  Wave Impedance 1 = $ c0
  Wave Impedance 2 = 0
End


Boundary Condition 7 
Target Boundaries(1) = $ left
  Periodic BC = 6
End

Boundary Condition 8
Target Boundaries(1) = $ top_bottom
  Wave Impedance 1 = $ c0
  Wave Impedance 2 = 0
End
  '''.format(frequency)


  # print(sif)
  file = open(f"case-{frequency}.sif","w")
  file.write(sif)
  file.close() 
