# Acoustic Metamaterial Generative Design and Optimisation Pipeline

## README in progress

### Dependencies 

* [Python](https://www.python.org/) 
* [Salome](https://salome-platform.org/) 
* [ElmerFEM](http://www.csc.fi/elmer)
* [Paraview](https://www.paraview.org/) 


### Pythons scripts

* parametric_brick.py
* assemble_lens.py
* export_structures.py
* process_geometry.py
* run_elmer_solver.py
* utility_functions.py

### Elmer Template

template.sif 

### Command Line Interface

Generate .unv and Elmer .sif template for for labyrinthine brick #15 

```
python '..\..\..\..\..\SALOME-9.7.0\salome' shell -p 2819 
.\process_geometry.py args:15,40000,41000,1000 
```


Generate .unv and Elmer .sif template for all labyrinthine bricks

```
python '..\..\..\..\..\SALOME-9.7.0\salome' shell -p 2819 
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
python '..\..\..\..\..\SALOME-9.7.0\salome' shell -p 2821 
.\process_geometry.py args:15,40000,41000,500 
.\run_elmer_solver.py args:15
```


Generate .unv and Elmer .sif template first and then and Elmer solver for all labyrinthine bricks to generate a .vtu file

```
python '..\..\..\..\..\SALOME-9.7.0\salome' shell -p 2819 
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
