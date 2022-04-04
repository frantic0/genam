# Generative Acoustic Metamaterial

__genam__ is a framework and pipeline for the generative design and optimisation of acoustic metamaterials.

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
python '..\..\..\..\..\SALOME-9.8.0\salome' shell -p 2819 
.\process_geometry.py args:15,40000,41000,1000 .\run_elmer_solver.py args:15 
.\process_geometry.py args:14,40000,41000,1000 .\run_elmer_solver.py args:14 
.\process_geometry.py args:13,40000,41000,1000 .\run_elmer_solver.py args:13 
.\process_geometry.py args:12,40000,41000,1000 .\run_elmer_solver.py args:12 
.\process_geometry.py args:11,40000,41000,1000 .\run_elmer_solver.py args:11 
.\process_geometry.py args:10,40000,41000,1000 .\run_elmer_solver.py args:10 
.\process_geometry.py args:09,40000,41000,1000 .\run_elmer_solver.py args:09 
.\process_geometry.py args:08,40000,41000,1000 .\run_elmer_solver.py args:08 
.\process_geometry.py args:07,40000,41000,1000 .\run_elmer_solver.py args:07 
.\process_geometry.py args:06,40000,41000,1000 .\run_elmer_solver.py args:06 
.\process_geometry.py args:05,40000,41000,1000 .\run_elmer_solver.py args:05 
.\process_geometry.py args:04,40000,41000,1000 .\run_elmer_solver.py args:04 
.\process_geometry.py args:03,40000,41000,1000 .\run_elmer_solver.py args:03 
.\process_geometry.py args:02,40000,41000,1000 .\run_elmer_solver.py args:02 
.\process_geometry.py args:01,40000,41000,1000 .\run_elmer_solver.py args:01
```
