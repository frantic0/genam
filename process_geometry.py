#!/usr/bin/env python

###
### This file is generated automatically by SALOME v9.3.0 with dump python functionality
###

import sys
import salome
import numpy as np
import time, os

os.chdir(r"C:/Users/Francisco/Documents/dev/acoustic-brick")
sys.path.insert(0, r'C:/Users/Francisco/Documents/dev/acoustic-brick')


from utility_functions import * 
from parametric_brick import * 

salome.salome_init()
import salome_notebook
notebook = salome_notebook.NoteBook()

###
### GEOM component
###

import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS

start = time.time()
geompy = geomBuilder.New()
origin = geompy.MakeVertex(0, 0, 0)
x = geompy.MakeVectorDXDYDZ(1, 0, 0)
y = geompy.MakeVectorDXDYDZ(0, 1, 0)
z = geompy.MakeVectorDXDYDZ(0, 0, 1)
pml_bottom = geompy.MakeBoxDXDYDZ(4.288, 4.288, 2.573)
box_1 = geompy.MakeTranslation(geompy.MakeBoxDXDYDZ(4.288, 4.288, 4.288), 0, 0, 2.573)
box_2 = geompy.MakeTranslation(geompy.MakeBoxDXDYDZ(4.288, 4.288, 12.776), 0, 0, 15.522)
pml_top = geompy.MakeTranslation(pml_bottom, 0, 0, 28.298)
brick_outer = geompy.MakeTranslation(geompy.MakeBoxDXDYDZ(4.288, 4.288, 8.661), 0, 0, 6.861)


Sketch_1 = draw_brick(6)

### Convert sketch to 3d object
rotation = [(x, 90)]
translation = (0.22, 4.068, 6.861)
brick_inner = sketch_to_volume(geompy, Sketch_1, 3.848, rotation, translation)
brick_fused = geompy.MakeFuseList([brick_outer, brick_inner], True, True)
brick = geompy.MakeCutList(brick_fused, [brick_inner], True)
air = geompy.MakeFuseList([box_1, box_2, brick_inner], True, True)
Structure = geompy.MakePartition([pml_bottom, pml_top, brick, air], [], [], [], geompy.ShapeType["SOLID"], 0, [], 0)

# solids = [Solid_1, Solid_2, Solid_3, Solid_4] = geompy.ExtractShapes(Structure, geompy.ShapeType["SOLID"], True)
solids = geompy.ExtractShapes(Structure, geompy.ShapeType["SOLID"], True)
print(solids)

faces = [Face_1, Face_2, Face_3, Face_4, Face_5, Face_6, Face_7, Face_8, Face_9, Face_10, Face_11, Face_12,\
        Face_13, Face_14, Face_15, Face_16, Face_17, Face_18, Face_19, Face_20, Face_21, Face_22, Face_23, \
        Face_24, Face_25, Face_26, Face_27, Face_28, Face_29, Face_30, Face_31, Face_32, Face_33, Face_34, \
        Face_35, Face_36, Face_37, Face_38, Face_39, Face_40, Face_41, Face_42, Face_43, Face_44, Face_45, \
        Face_46, Face_47, Face_48, Face_49, Face_50, Face_51, Face_52, Face_53, Face_54] = geompy.ExtractShapes(Structure, geompy.ShapeType["FACE"], True)

# Autogroups in geometry for meshing
Auto_group_for_top_bottom_walls = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set top & bottom walls
geompy.UnionList(Auto_group_for_top_bottom_walls, [Face_25, Face_30]) 
Auto_group_for_brick_faces = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set brick faces
geompy.UnionList(Auto_group_for_brick_faces, [Face_6, Face_7, Face_8, Face_9, Face_10, Face_11, Face_12, Face_13, \
                                              Face_14, Face_15, Face_16, Face_17,  Face_18, Face_24, Face_27, \
                                              Face_28, Face_31, Face_37, Face_38, Face_39, Face_40, Face_41, Face_42, \
                                              Face_43, Face_44, Face_45, Face_46, Face_47, Face_48, Face_49])
Auto_group_for_front = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set front walls
geompy.UnionList(Auto_group_for_front, [Face_19, Face_20, Face_22, Face_23])
Auto_group_for_left = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set left walls
geompy.UnionList(Auto_group_for_left, [Face_1, Face_2, Face_4, Face_5])
Auto_group_for_back = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set back walls
geompy.UnionList(Auto_group_for_back, [Face_32, Face_33, Face_35, Face_36])
Auto_group_for_right = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set right walls
geompy.UnionList(Auto_group_for_right, [Face_50, Face_51, Face_53, Face_54])

# Add autogroups to study
geompy.addToStudyInFather(Structure, Auto_group_for_right, 'Auto_group_for_right')
geompy.addToStudyInFather(Structure, Auto_group_for_left, 'Auto_group_for_left')
geompy.addToStudyInFather(Structure, Auto_group_for_back, 'Auto_group_for_back')
geompy.addToStudyInFather(Structure, Auto_group_for_top_bottom_walls, 'Auto_group_for_top_bottom_walls')
geompy.addToStudyInFather(Structure, Auto_group_for_brick_faces, 'Auto_group_for_brick_faces')
geompy.addToStudyInFather(Structure, Auto_group_for_front, 'Auto_group_for_front')

# Add to solids & faces to study
geompy.addToStudy(Structure, 'Structure')
for num, f in enumerate(faces): # add faces to study
  geompy.addToStudyInFather(Structure, f, 'face_{}'.format(num + 1) )  
for num, s in enumerate(solids): # add solids to study
  geompy.addToStudyInFather(Structure, s, 'solid_{}'.format(num + 1))  

geompy.addToStudy(Sketch_1, 'Sketch') 

end = time.time()
print("Geometry computation time: {:.2f} sec".format(end - start))

### SMESH component
###

import  SMESH, SALOMEDS
from salome.smesh import smeshBuilder

start = time.time()
smesh = smeshBuilder.New()

Structure_1 = smesh.Mesh(Structure)
NETGEN_1D_2D_3D = Structure_1.Tetrahedron(algo=smeshBuilder.NETGEN_1D2D3D)
NETGEN_3D_Parameters_1 = NETGEN_1D_2D_3D.Parameters()
NETGEN_3D_Parameters_1.SetMaxSize( 3.1461 )
NETGEN_3D_Parameters_1.SetMinSize( 0.0844741 )
NETGEN_3D_Parameters_1.SetSecondOrder( 0 )
NETGEN_3D_Parameters_1.SetOptimize( 1 )
NETGEN_3D_Parameters_1.SetFineness( 4 )
NETGEN_3D_Parameters_1.SetChordalError( -1 )
NETGEN_3D_Parameters_1.SetChordalErrorEnabled( 0 )
NETGEN_3D_Parameters_1.SetUseSurfaceCurvature( 1 )
NETGEN_3D_Parameters_1.SetFuseEdges( 1 )
NETGEN_3D_Parameters_1.SetQuadAllowed( 0 )
NETGEN_3D_Parameters_1.SetCheckChartBoundary( 72 )

# Add meshing groups
pml_bottom_mesh = Structure_1.GroupOnGeom(Solid_1,'pml_bottom',SMESH.VOLUME)
brick_mesh = Structure_1.GroupOnGeom(Solid_2,'brick',SMESH.VOLUME)
air_mesh = Structure_1.GroupOnGeom(Solid_3,'air',SMESH.VOLUME)
pml_top_mesh = Structure_1.GroupOnGeom(Solid_4,'pml_top',SMESH.VOLUME)

top_bottom_walls = Structure_1.GroupOnGeom(Auto_group_for_top_bottom_walls,'Auto_group_for_top_bottom_walls',SMESH.FACE)
top_bottom_walls.SetName( 'top_bottom_walls' )
inlet = Structure_1.GroupOnGeom(Face_26,'Face_26',SMESH.FACE)
inlet.SetName('inlet')
outlet = Structure_1.GroupOnGeom(Face_29,'Face_29',SMESH.FACE)
outlet.SetName('outlet')
brick_faces = Structure_1.GroupOnGeom(Auto_group_for_brick_faces,'Auto_group_for_brick_faces',SMESH.FACE)
brick_faces.SetName('brick_faces')
brick_left = Structure_1.GroupOnGeom(Face_3,'Face_3',SMESH.FACE)
brick_left.SetName('brick_left')
brick_front = Structure_1.GroupOnGeom(Face_21,'Face_21',SMESH.FACE)
brick_front.SetName('brick_front')
brick_back = Structure_1.GroupOnGeom(Face_34,'Face_34',SMESH.FACE)
brick_back.SetName('brick_back')
brick_right = Structure_1.GroupOnGeom(Face_52,'Face_52',SMESH.FACE)
brick_right.SetName('brick_right')
left = Structure_1.GroupOnGeom(Auto_group_for_left,'left',SMESH.FACE)
front = Structure_1.GroupOnGeom(Auto_group_for_front,'front',SMESH.FACE)
back = Structure_1.GroupOnGeom(Auto_group_for_back,'back',SMESH.FACE)
right = Structure_1.GroupOnGeom(Auto_group_for_right,'right',SMESH.FACE)

isDone = Structure_1.Compute()

# Add groups in mesh.unv
[pml_bottom, pml_top, brick, air, top_bottom_walls, inlet, outlet, brick_faces, brick_left, brick_front, brick_back, brick_right, left, front, back, right ] = Structure_1.GetGroups()


# Mesh computation time
end = time.time()
print("Mesh computation time: {:.2f} sec".format(end - start))

# Rename bodies for Elmer
# smesh.SetName(solids_mesh[0], 'pml_bot')
# smesh.SetName(solids_mesh[1], 'brick')
# smesh.SetName(solids_mesh[2], 'air')
# smesh.SetName(solids_mesh[3], 'pml_top')

# Rename faces for Elmer
# smesh.SetName(left, 'left')
# smesh.SetName(back, 'back')
# smesh.SetName(front, 'front')
# smesh.SetName(NETGEN_2D3D_1.GetAlgorithm(), 'NETGEN_2D3D_1')
# smesh.SetName(right, 'right')
# smesh.SetName(brick_front, 'brick_front')
# smesh.SetName(brick_back, 'brick_back')
# smesh.SetName(brick_right, 'brick_right')
# smesh.SetName(NETGEN_Parameters, 'NETGEN_Parameters')
# smesh.SetName(Structure_1.GetMesh(), 'Structure')
# smesh.SetName(brick_left, 'brick_left')
# smesh.SetName(brick_faces, 'brick_faces')
# smesh.SetName(outlet, 'outlet')
# smesh.SetName(inlet, 'inlet')
# smesh.SetName(top_bottom_walls, 'top_bottom_walls')

start = time.time()
  
# First export mesh in .unv format
try:
  Structure_1.ExportUNV( r'C:\Users\Francisco\dev\acoustic-brick\Structure.unv' )
  pass
except:
  print('ExportUNV() failed. Invalid file name?')

# Export mesh to Elmer
export_elmer('Structure')

end = time.time()
print("Salome to Elmer computation time: {:.2f} sec".format(end - start))

if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser()
