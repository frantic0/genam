#!/usr/bin/env python

###
### This file is generated automatically by SALOME v9.8.0 with dump python functionality
###

import sys
import salome
import time, os

salome.salome_init()
import salome_notebook
notebook = salome_notebook.NoteBook()
sys.path.insert(0, r'C:/Users/Francisco/Documents/dev/pipeline/ammgdop')

###
### GEOM component
###

import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS

start = time.time()


geompy = geomBuilder.New()

O = geompy.MakeVertex(0, 0, 0)
OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)
Sphere_1 = geompy.MakeSpherePntR(O, 5)
Sphere_2 = geompy.MakeSpherePntR(O, 20)
# Sphere_2 = geompy.MakeSpherePntR(O, 100)
Partition_1 = geompy.MakePartition([Sphere_1, Sphere_2], [], [], [], geompy.ShapeType["SOLID"], 0, [], 0)
[Face_1,Face_2] = geompy.ExtractShapes(Partition_1, geompy.ShapeType["FACE"], True)
solids = [Solid_1, Solid_2] = geompy.ExtractShapes(Partition_1, geompy.ShapeType["SOLID"], True)
print(solids)
geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )
geompy.addToStudy( Sphere_2, 'Sphere_2' )
geompy.addToStudy( Sphere_1, 'Sphere_1' )
geompy.addToStudy( Partition_1, 'Partition_1' )

geompy.addToStudyInFather( Partition_1, Face_1, 'Face_1' )
geompy.addToStudyInFather( Partition_1, Face_2, 'Face_2' )
geompy.addToStudyInFather( Partition_1, Solid_1, 'Solid_1' )
geompy.addToStudyInFather( Partition_1, Solid_2, 'Solid_2' )



###
### SMESH component
###


end = time.time()
print("Geometry computation time: {:.2f} sec".format(end - start))

import  SMESH, SALOMEDS
from salome.smesh import smeshBuilder

start = time.time()

smesh = smeshBuilder.New()
#smesh.SetEnablePublish( False ) # Set to False to avoid publish in study if not needed or in some particular situations:
                                 # multiples meshes built in parallel, complex and numerous mesh edition (performance)

Mesh_1 = smesh.Mesh(Partition_1)
NETGEN_1D_2D_3D = Mesh_1.Tetrahedron(algo=smeshBuilder.NETGEN_1D2D3D)
NETGEN_3D_Parameters_1 = NETGEN_1D_2D_3D.Parameters()
# NETGEN_3D_Parameters_1.SetMaxSize( 3.4641 )                 # default parameter  
# NETGEN_3D_Parameters_1.SetMinSize( 0.141616 )               # default parameter 
# NETGEN_3D_Parameters_1.SetMaxSize( 0.08575 )
# NETGEN_3D_Parameters_1.SetMinSize( 0.01616 )
NETGEN_3D_Parameters_1.SetMaxSize( 0.8575 )
NETGEN_3D_Parameters_1.SetMinSize( 0.1616 )
NETGEN_3D_Parameters_1.SetSecondOrder( 1 )
NETGEN_3D_Parameters_1.SetOptimize( 1 )
NETGEN_3D_Parameters_1.SetFineness( 4 )
NETGEN_3D_Parameters_1.SetChordalError( -1 )
NETGEN_3D_Parameters_1.SetChordalErrorEnabled( 0 )
NETGEN_3D_Parameters_1.SetUseSurfaceCurvature( 1 )
NETGEN_3D_Parameters_1.SetFuseEdges( 1 )
NETGEN_3D_Parameters_1.SetQuadAllowed( 0 )
NETGEN_3D_Parameters_1.SetCheckChartBoundary( 120 )
Face_1_1 = Mesh_1.GroupOnGeom(Face_1,'Face_1',SMESH.FACE)
Face_2_1 = Mesh_1.GroupOnGeom(Face_2,'Face_2',SMESH.FACE)

isDone = Mesh_1.Compute()

end = time.time()
print("Mesh computation time: {:.2f} sec".format(end - start))

# [ Face_1_1, Face_2_1 ] = Mesh_1.GetGroups()
print(Mesh_1.GetGroups())
try:
  Mesh_1.ExportUNV( r'C:/Users/francisco/Documents/dev/pipeline/data/sphere.unv' )
  pass
except:
  print('ExportUNV() failed. Invalid file name?')


## Set names of Mesh objects
smesh.SetName(NETGEN_1D_2D_3D.GetAlgorithm(), 'NETGEN 1D-2D-3D')
smesh.SetName(NETGEN_3D_Parameters_1, 'NETGEN 3D Parameters_1')
smesh.SetName(Face_1_1, 'Face_1')
smesh.SetName(Face_2_1, 'Face_2')
smesh.SetName(Mesh_1.GetMesh(), 'Mesh_1')


if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser()
