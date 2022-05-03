# Generative Acoustic Metamaterial

__genam__ is a python package and framework for the generative design and optimisation of acoustic metamaterials.

### Dependencies 

This is the list of software required to run the Python scripts in the next section. 

* [Salome 9.8.0](https://salome-platform.org/) – Integration platform for numerical simulation
* [ElmerFEM](http://www.csc.fi/elmer) – Multiphysical simulation
* [Paraview](https://www.paraview.org/) – Data analysis and visualization 
* [Python 3.9](https://www.python.org/) and libraries for post-processing and analysis:
  * [Jupyter Notebooks](https://www.python.org/)
  * [numpy](https://www.python.org/)
  * [pandas](https://www.python.org/)
  * [matplotlib](https://www.python.org/)


### Models 

* [parametric_brick.py](https://github.com/frantic0/ammgdop/blob/main/parametric_brick.py) –
* [lens.py](https://github.com/frantic0/ammgdop/blob/main/assemble_lens.py) –
* [export_structures.py](https://github.com/frantic0/ammgdop/blob/main/export_structures.py) – 
* [process_geometry.py](https://github.com/frantic0/ammgdop/blob/main/process_geometry.py) –
* [run_elmer_solver.py](https://github.com/frantic0/ammgdop/blob/main/run_elmer_solver.py) – 
* [utility_functions.py](https://github.com/frantic0/ammgdop/blob/main/utility_functions.py) –

### Elmer Template


### Command Line Interface

Start a Salome instance that will generate the labyrinthine brick's geometry and . 

```
python salome
```

Generate .unv and Elmer .sif template for for labyrinthine brick #15 

```
python '..\..\..\..\..\SALOME-9.8.0\salome' shell -p 2819 .\process_geometry.py args:15,40000,41000,1000 
```

You can also use salome in batch mode

```
..\..\..\..\..\..\SALOME-9.8.0\salome -t -w1 .\process_geometry.py args:15,40000,41000,250 .\run_elmer_solver.py args:15 .\process_geometry.py args:14,40000,41000,250 .\run_elmer_solver.py args:15 .\process_geometry.py args:13,40000,41000,250 .\run_elmer_solver.py args:13 .\process_geometry.py args:12,40000,41000,250 .\run_elmer_solver.py args:12 .\process_geometry.py args:11,40000,41000,250 .\run_elmer_solver.py args:11 .\process_geometry.py args:10,40000,41000,250 .\run_elmer_solver.py args:10 .\process_geometry.py args:9,40000,41000,250 .\run_elmer_solver.py args:9 .\process_geometry.py args:8,40000,41000,250 .\run_elmer_solver.py args:8 .\process_geometry.py args:7,40000,41000,250 .\run_elmer_solver.py args:7 .\process_geometry.py args:6,40000,41000,250 .\run_elmer_solver.py args:6 .\process_geometry.py args:5,40000,41000,250 .\run_elmer_solver.py args:5 .\process_geometry.py args:4,40000,41000,250 .\run_elmer_solver.py args:4 .\process_geometry.py args:3,40000,41000,250 .\run_elmer_solver.py args:3 .\process_geometry.py args:2,40000,41000,250 .\run_elmer_solver.py args:2 .\process_geometry.py args:1,40000,41000,250 .\run_elmer_solver.py args:1
```


Generate .unv and Elmer .sif template for all labyrinthine bricks

```
python '..\..\..\..\..\SALOME-9.8.0\salome' shell -p 2819 
.\process_geometry.py args:15,40000,41000,1000 
.\process_geometry.py args:14,40000,41000,1000 
.\process_geometry.py args:13,40000,41000,1000 
.\process_geometry.py args:12,40000,41000,1000 
.\process_geometry.py args:11,40000,41000,1000 
.\process_geometry.py args:10,40000,41000,1000 
.\process_geometry.py args:9,40000,41000,1000 
.\process_geometry.py args:8,40000,41000,1000 
.\process_geometry.py args:7,40000,41000,1000 
.\process_geometry.py args:6,40000,41000,1000 
.\process_geometry.py args:5,40000,41000,1000 
.\process_geometry.py args:4,40000,41000,1000 
.\process_geometry.py args:3,40000,41000,1000 
.\process_geometry.py args:2,40000,41000,1000 
.\process_geometry.py args:1,40000,41000,1000
```


Generate .unv and Elmer .sif template first and then and Elmer solver for labyrinthine brick #15 to generate a .vtu file  

```
python ..\..\..\..\..\SALOME-9.8.0\salome shell -p 2821 .\process_geometry.py args:15,40000,41000,500 .\run_elmer_solver.py args:15
```


Generate .unv and Elmer .sif template first and then and Elmer solver for all labyrinthine bricks to generate a .vtu file

```
import sys
from pathlib import Path

### Salome GEOM and SMESH components
import salome
salome.salome_init()

# Set file paths for library and tests  
# TODO: find a way to remove this into dependant classes as platform-dependent relative paths 
sys.path.insert(0, r'C:/Users/francisco/Documents/dev/pipeline')
sys.path.insert(0, r'C:/Users/francisco/Documents/dev/pipeline/genam')
sys.path.insert(0, r'C:/Users/francisco/Documents/dev/pipeline/tests')

# Genam Lens, mesh configurator
from genam.lens import Lens
from genam.lens_configuration import lens_configurator 
from genam.mesh_configuration import selector as mesh_config_selector
from matrices.quantized_1_1 import quantized_matrix_1_1
from genam.utility_functions import convert_mesh, copy_solver_templates

lens_config = lens_configurator( quantized_matrix_1_1 )

lens_name = 'quantized_matrix_1_1' 

# Create lens with name, bricks ID and mesh configurations 

lens = Lens( lens_config, mesh_config_selector(3), name = lens_name  )

lens.process_geometry() # Create the lens geometry 

lens.process_mesh() # Create lens mesh 

# define a path where all data will be stored (.unv mesh file, solver *.mesh files, sif. file )
path = str(Path('C:/Users/francisco/Documents/acoustic-brick/').joinpath( lens_name + '.unv')) 

lens.export_mesh( path ) # export .unv mesh file

convert_mesh( path ) # run elmergrid convert .unv mesh file to elmer format *.mesh files in a directory 

# copy all the necessary templates to run elmer solver
copy_solver_templates(  path, 
                        start_frequency = 40000, 
                        end_frequency = 41000, 
                        step = 1000 )

```
