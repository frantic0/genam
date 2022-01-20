import sys
import salome
import numpy as np
import time, os, shutil

import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS

def sketch_to_volume(geom_builder, sketch_obj, thickness, rotation=None, translation=None):
  # Inputs
  # 
  #   sketch: 2d sketch of the object
  #   thickness: thickness of volume in z axis
  #   rotation: provide a list of tuples with (axis, angle) as a tuple i.e. (x, 90), in the order you want to rotate in x axis
  #
  # Returns
  #   
  #   sketch_rotation: sketch to 3d object
  
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



def copy_elmer_templates(dirname, start_frequency, end_frequency, step): 

  src = r'C:/Users/francisco/Documents/dev/pipeline/template/'  
  dst = r'C:/Users/francisco/Documents/dev/pipeline/data/' + dirname + '/'

  # print('copy template to dest: ' + dst)

  for fileName in os.listdir(src):
    source = src + fileName
    destination = dst + fileName 
    if os.path.isfile(source):
      shutil.copy(source, destination)
      print('copied', fileName)
  
  for frequency in range(start_frequency, end_frequency + step, step):
    export_parameterisable_elmer_sif( dirname, frequency )



def export_elmer(filename):
  """
  Input

    filename: name of the .unv file exported by Salome

  Output

    .unv to *.mesh (Elmer format)
  
  """
  print(filename)
  # os.system(f'cmd /c "dir C:\Users\francisco\Documents\dev\pipeline\data\brick-15"')
  # execute comand and terminate
  # os.chdir(f"C:/Users/francisco/Documents/dev/pipeline/data/{dirname}")
  os.system('cmd /c "ElmerGrid 8 2 {}.unv -autoclean"'.format(filename))  


def export_parameterisable_elmer_sif( dirname, frequency):
  """
  Input


  Output

    .unv to *.mesh (Elmer w)
  
  """
  print(dirname)
  os.chdir(f"C:/Users/francisco/Documents/dev/pipeline/data/{dirname}")
 
  sif = f'''
!match face ids to names according to mesh.names files

$ freqVec = vector(100,1800,50)

Check Keywords "Warn"
  INCLUDE mesh.names

Header
  CHECK KEYWORDS Warn
  Mesh DB "." "."
  Include Path ""
  Results Directory ""
  $rho0 = 1.205
  $c0 = 343.0
End

Simulation
  Max Output Level = 5
  Coordinate System = Cartesian
  Coordinate Mapping(3) = 1 2 3
  Simulation Type = Steady state
  Steady State Max Iterations = 1
  Output Intervals = 1
  Timestepping Method = BDF
  BDF Order = 1
  Coordinate Scaling = Real 0.001 ! notify Elmer that our dimensions are in mm
  Post File = case-{frequency}.vtu
End

Constants
  Gravity(4) = 0 -1 0 9.82
  Stefan Boltzmann = 5.67e-08
  Permittivity of Vacuum = 8.8542e-12
  Boltzmann Constant = 1.3807e-23
  Unit Charge = 1.602e-19
End

Body 1
  Target Bodies(1) = $pml_bottom
  Name = "pml_bottom"
  Equation = 1
  Material = 1
End

!  Export the Sound Pressure Level in vtu file
Body Force 1
  Name = "SPL"
SPL = Variable Pressure Wave 1, Pressure Wave 2
      Real MATC "20 * log(((sqrt(tx(0)^2 + tx(1)^2)) /sqrt(2)))"
End

!  Export the Sound Pressure Level in vtu file
Body Force 1
  Name = "SPL"
SPL = Variable Pressure Wave 1, Pressure Wave 2
      Real MATC "20 * log(((sqrt(tx(0)^2 + tx(1)^2)) /sqrt(2)))"
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
  Body Force(2) = 1 2
End

Body 4
  Target Bodies(1) = $pml_top
  Name = "pml_top"
  Equation = 1
  Material = 1
End

Solver 1
  Equation = Helmholtz Equation
  Procedure = "HelmholtzSolve" "HelmholtzSolver"
  Variable = -dofs 2 Pressure Wave
  ! Export the Sound Pressure Level with the Pressure Wave variables in vtu file (see below body force)
  Nonlinear Update Exported Variables = Logical True
  Exported Variable 1 = SPL
  Exported Variable 2 = Phase
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
  Linear System Preconditioning = ILU2
  Linear System ILUT Tolerance = 1.0e-3
  Linear System Abort Not Converged = False
  Linear System Residual Output = 10
  Linear System Precondition Recompute = 1
End

Solver 2
  Procedure = "SaveData" "SaveScalars"  
  Filename = SPLmean.dat
  Operator 1 = boundary mean
  Variable 1 = SPL
  ! Want to append to file?
  File Append = Logical True
End

Solver 3
  Equation = "flux compute 1"
  Procedure = "FluxSolver" "FluxSolver"
  Calculate Flux = Logical True
  Target Variable = String "Pressure Wave 2"
  Flux Coefficient = String "Cv"
  Linear System Solver = Direct
  Linear System Direct Method = Banded
End

Solver 4
  Equation = "flux compute 2"
  Procedure = "FluxSolver" "FluxSolver"
  Calculate Flux = Logical True
  Target Variable = String "Pressure Wave 1"
  Flux Coefficient = String "Cv"
  Linear System Solver = Direct
  Linear System Direct Method = Banded
End


Solver 5
  Equation = Result Output
  Procedure = "ResultOutputSolve" "ResultOutputSolver"
  Save Geometry Ids = True
  Output File Name = "brick-{frequency}"
  Output Format = Vtu
  Scalar Field 2 = Pressure wave 2
  Scalar Field 1 = Pressure wave 1
  Vector Field 1 = Pressure wave 2 flux
  Vector Field 2 = Pressure wave 1 flux
  Scalar Field 3 = "SPL"
End


Equation 1
  Name = "Helmholtz"
  ! Frequency = Variable time; Real MATC "freqVec(tx - 1)"
  Angular Frequency = $ 2.0 * pi * {frequency}
  Active Solvers(4) = 1 2 3 4
End

Equation 2
  Name = "Result Output EQ"
  Active Solvers(1) = 5
End

! %%%%%%%%%
! %% Air %%
! %%%%%%%%%

Material 1 
  Name = "Air"
  Viscosity = 1.983e-5
  Heat expansion Coefficient = 3.43e-3
  Heat Conductivity = 0.0257
  Relative Permittivity = 1.00059
  Sound speed = 343.0
  Heat Capacity = 1005.0
  Density = 1.205
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

! %%%%%%%%%%%%
! %% Inlet  %%
! %%%%%%%%%%%%

Boundary Condition 1
  Target Boundaries(1) = $ inlet
  Name = "In"
  Plane Wave BC = True
$p0=1.0
$k1=0.0
$k2=0.0
$k3=1.0
  Pressure Wave 1 = Variable Coordinate 
    Real MATC "p0 * cos(k1*tx(0) + k2*tx(1) + k3*tx(2))"
  Pressure Wave 2 = 0
  Wave Impedance 1 = $ c0
End

! %%%%%%%%%%%
! %% Walls %% 
! %%%%%%%%%%%

Boundary Condition 2
Target Boundaries(5) = $ brick_faces brick_left brick_right brick_back brick_front
  Name = "Wall"
  Wave Flux 1 = 0
  Wave Flux 2 = 0
End

! %%%%%%%%%%%%
! %% Air    %% 
! %%%%%%%%%%%%

Boundary Condition 3
Target Boundaries(2) = $ outlet top_bottom_walls 
  Name = "Air"
  Wave Impedance 1 = $ c0
End

! %%%%%%%%%%%
! %%  PBC  %%
! %%%%%%%%%%%

! left/right
 
Boundary Condition 4 
Target Boundaries(2) = $ left brick_left
End

Boundary Condition 5 
Target Boundaries(2) = $ right brick_right
  Periodic BC = 4
End

! front/back

Boundary Condition 6 
  Target Boundaries(2) = $ front brick_front
End

Boundary Condition 7 
Target Boundaries(2) = $ back brick_back
  Periodic BC = 6
End
  '''.format(frequency)


  print(sif)
  file = open(f"case-{frequency}.sif","w")
  file.write(sif)
  file.close() 
