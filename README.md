# Generative Acoustic Metamaterial

__genam__ is a python package and a framework for the generative design and optimisation of acoustic metamaterials.

![alt text](https://github.com/frantic0/genam/blob/main/docs/img/labyrinthine.png)

<br />

__genam__ implements an automation pipeline for geometric modelling, finite elements method, wave scattering simulation and synthetic data generation for acoustic metamaterials. 

![alt text](https://github.com/frantic0/genam/blob/main/docs/img/forward-inverse-design.png)


__genam__ runs against Salome 9.8.0 and Elmer (Windows and Linux) and its typical use is installed and running in an HPC cluster or a powerfull server.

__genam__ is designed with an easy-to-use, small surface API with a object-oriented architecture, and test suites with exemplars for different lens configuration (1x1, 2x2, 4x4, 8x1, 16x1, 16x2, 16x6).​

<br />

### Parametric modelling, meshing and simulation

![alt text](https://github.com/frantic0/genam/blob/main/docs/img/parametric-modelling-simulation.png)

Genam implements algorithms for building parametric 3D models of labyrinthine bricks with multiple degrees-of-freedom (DoFs):
* Wavelength 
* Aggregate Flap size 
* Aggregate Flap distance
* Perfect Matched Layer offset 
* Mesh size
* Mesh Element Order

Genam also allows the specification of complex metasurface lens macros. For instance, a 16x16 unit-cell focusing metasurface lens can be specified like so:


```python
import numpy as np

quantized_matrix_16_16 = np.array([
                                  [ 13,  0,  3,  5,  7,  8,  9, 10, 10,  9,  8,  7,  5,  3,  0, 13 ], #0
                                  [  0,  3,  6,  8, 10, 12, 13, 13, 13, 13, 12, 10,  8,  6,  3,  0 ], #1 
                                  [  3,  6,  9, 11, 13, 15,  0,  0,  0,  0, 15, 13, 11,  9,  6,  3 ], #2 
                                  [  5,  8, 11, 14,  0,  1,  2,  3,  3,  2,  1,  0, 14, 11,  8,  5 ], #3 
                                  [  7, 10, 13,  0,  2,  3,  4,  5,  5,  4,  3,  2,  0, 13, 10,  7 ], #4 
                                  [  8, 12, 15,  1,  3,  5,  6,  6,  6,  6,  5,  3,  1, 15, 12,  8 ], #5                                 
                                  [  9, 13,  1,  4,  5,  6,  7,  7,  7,  7,  6,  5,  4,  1, 13,  9 ], #6
                                  [ 10, 13,  0,  3,  5,  6,  7,  8,  8,  7,  6,  5,  3,  0, 13, 10 ], #7 
                                  [ 10, 13,  0,  3,  5,  6,  7,  8,  8,  7,  6,  5,  3,  0, 13, 10 ], #8
                                  [  9, 13,  1,  4,  5,  6,  7,  7,  7,  7,  6,  5,  4,  1, 13,  9 ], #9
                                  [  8, 12, 15,  1,  3,  5,  6,  6,  6,  6,  5,  3,  1, 15, 12,  8 ], #10
                                  [  7, 10, 13,  0,  2,  3,  4,  5,  5,  4,  3,  2,  0, 13, 10,  7 ], #11
                                  [  5,  8, 11, 14,  0,  1,  2,  3,  3,  2,  1,  0, 14, 11,  8,  5 ], #12
                                  [  3,  6,  9, 11, 13, 15,  0,  0,  0,  0, 15, 13, 11,  9,  6,  3 ], #13 
                                  [  0,  3,  6,  8, 10, 12, 13, 13, 13, 13, 12, 10,  8,  6,  3,  0 ], #14
                                  [ 13,  0,  3,  5,  7,  8,  9, 10, 10,  9,  8,  7,  5,  3,  0, 13 ], #15
                                ])

```

<br />

## Dependencies 

__genam__ scripts run on Salome's Python virtual environment. 

* [Salome 9.8.0](https://salome-platform.org/) – Integration platform for numerical simulation

That means that, rather than executing __genam__ scripts using your Python installation on your terminal, shell or integrated development environment (IDE, e.g. VS Code, Atom or Pylance), you need to run them with Salome. Next section will show how to open scripts on Salome's graphical user interface, or run them with Salome in batch mode in the command line interface. 

The following is the list of third-party software and python modules that aren not installed by default in Salome but are necessary to run __genam__ scripts:

* [ElmerFEM](http://www.csc.fi/elmer) – Multiphysical simulation
* [Paraview](https://www.paraview.org/) – Data analysis and visualization 
* [Python](https://www.python.org/) libraries for post-processing and analysis:
  * [numpy](https://www.python.org/)
  * [pandas](https://www.python.org/)
  * [matplotlib](https://www.python.org/)
  * [meshio](https://www.python.org/)
  * [pytorch](https://pytorch.org)

Additionally, you may want to install Jupiter notebooks to run interactive analyis:

* [Jupyter Notebooks](https://www.python.org/)

You will also need an IDE or code editor to edit the Python code in your scripts. Here's is a useful thread on how to set up a code editor with Salome.

* [Using python salome libraries from a python IDE](https://discourse.salome-platform.org/t/using-python-salome-libraries-from-a-python-ide/63/7)

<br />

## Installation

To install Salome in your system after you download the package, we suggest you unpack Salome to your **home** directory (Linux) or to the following directory (Windows): 

```
C:\SALOME-9.8.0
```

Once you have unpacked Salome, you will find there the following scripts:

* Linux: source ```env_launch.sh``` (generated by ./sat environ SALOME)
* Windows: ```env_launch.bat``` (shipped with SALOME).

You will need to run these to set Salome's virtual environment to install the Python module dependencies listed above. To do so, you have to install a module like ```pandas``` using Salome's virtual environment python and pip, like so:   

```
C:\SALOME-9.8.0\W64\Python\python -m pip install pandas
```

<br />

## Up and Running


Once you have everything set up, start a Salome instance from your command line interface

```
python salome
```

You can also use salome in batch mode, which means without the graphical user interface and environment.  

```
python .\salome -t -w1 
```

For instance, to generate and run a study of the labyrinthine brick #15 using Salome in batch mode,  

```
python .\salome -t -w1  .test_quantized_matrix_1_1.py args:15
```

If all goes well, this will generate the geometry and mesh files for labyrinthine brick #15 (.unv and Elmer format files *.mesh), and the .sif template for the Elmer solver to generate a simulation which will be stored in a .vtu file.
  

## Usage 

This section introduces what a typical __genam__ script is and how it is structured. It provides a short and cursory tutorial that break down a script into it most important parts and explains 


A high-level __genam__ script runs within the Salome environment, so it needs to import the main Salome module and request an initialisation. It also interacts files and from specific directories in the file system, from which it reads and/or writes intermediate data for the meshing and simulation stages.


```python
import sys
from pathlib import Path

### Salome GEOM and SMESH components
import salome
salome.salome_init()
```

Because the script is running within Salome, which takes over the current working directory, we need to tell Salome where the __genam__ package is installed, like so:   


```python
# Set file paths for library and tests  
sys.path.insert(0, r'C:/Users/user/Documents/dev/pipeline')
sys.path.insert(0, r'C:/Users/user/Documents/dev/pipeline/genam')
sys.path.insert(0, r'C:/Users/user/Documents/dev/pipeline/tests')
```

The __genam__ package is structured with a simple namespace that reflects its main package concepts, such as entities and workflow stages, and implementation. Typically, we to use geometry and meshing classes and methods, configuration entities and data structures, and utility functions: 

```python
# Genam Lens, mesh configurator
from matrices.quantized_8_8 import quantized_matrix_8_8
from genam.lens import Lens
from genam.configuration.lens import configurator as lens_configurator 
from genam.configuration.mesh import configurator as mesh_configurator
from genam.solver import convert_mesh, copy_solver_templates, copy_sif, run_elmer_solver
from genam.analysis import Analysis
```

To create a model of a lens, or a metasurface, you configure it with a matrice of quantized bricks identifiers (between 0 and 15), configure its mesh parameters and name it. 

```python
lens_config = lens_configurator( quantized_matrix_8_8 )

lens_name = 'quantized_matrix_8_8' 

lens = Lens( lens_config, mesh_config_selector(3), name = lens_name  )
```

For instance, the matrix configuration for an 8x8 lens of quantised bricks can be something like this:

```python
quantized_matrix_8_8 = np.array([ 
                                  [  4,  7, 10, 13, 13, 10,  7,  4 ],
                                  [  5,  9, 13,  3,  3, 13,  9,  5 ],
                                  [ 10, 13,  0,  6,  6,  0, 13, 10 ],
                                  [ 15,  3,  6,  7,  7,  6,  3, 15 ],
                                  [ 15,  3,  6,  7,  7,  6,  3, 15 ],
                                  [ 10, 13,  0,  6,  6,  0, 13, 10 ],
                                  [  5,  9, 13,  3,  3, 13,  9,  5 ],
                                  [  4,  7, 10, 13, 13, 10,  7,  4 ],
                                ])
```

Once the lens is created, you can request the lens geometry and mesh processing in that order: 

```python
lens.process_geometry() 

lens.process_mesh() 
```

Once the pre-processing stage is completed, we can prepare all the data files and paths for running the ElmerSolver simulation.
First we define a dataset path, where all data will be stored - .unv mesh files and solver directories, solver *.mesh files, sif. file.

```python
DATASET_PATH = Path('/SAN/uclic/ammdgop/data')              
```

Then we can export the lens mesh data to a __.unv__ file in a dataset subdirectory named after the lens and convert the mesh.
```python
UNV_PATH = DATASET_PATH.joinpath( lens_name + '.unv')       

lens.export_mesh( str( UNV_PATH ) ) 

convert_mesh( UNV_PATH ) # run elmergrid convert .unv mesh file to elmer format *.mesh files in a directory 
```

We also need to set up everything the ElmerSolver needs to run, which includes setting up the path for folder where the solver configuration file and templates will be copied to. Only then we can run the solver to obtain the simulation.


```python
SOLVER_DATA_PATH = DATASET_PATH.joinpath( lens_name )       
SIF_PATH = Path('test_quantised_matrix.sif')     

copy_solver_templates( SOLVER_DATA_PATH )         
copy_sif( SOLVER_DATA_PATH, SIF_PATH )  

run_elmer_solver( SOLVER_DATA_PATH )
```

Once the ElmerSolver simulation completes and gets its data stored in a __.vtu__ file, we can get values of specific data series like pressure and phase, and analyse specific data points.

```python
analysis = Analysis( str(SOLVER_DATA_PATH.joinpath( 'case-40000_t0001.vtu' )) )

find_optimisation_target = lambda points, precision, value: sorted(list(filter( lambda x: x[2] == 0.1 and x[0] < 0 and x[1] < 0, points)))

optimisation_targets = find_optimisation_target(analysis.points, 2, 0.1)
optimisation_target = optimisation_targets[len(optimisation_targets)-1]
optimisation_target_id = analysis.points.index(optimisation_targets[len(optimisation_targets)-1])
optimisation_target_pressure = analysis._absolute_pressure.GetValue(optimisation_target_id)
```


## License

__genam__ is licensed under the MIT License