from stringprep import in_table_c12
import sys
import salome
import numpy as np
import time, os

print(os.getcwd())

os.chdir(r"C:/Users/francisco/Documents/dev/pipeline/ammgdop")
sys.path.insert(0, r'C:/Users/francisco/Documents/dev/pipeline/ammgdop')

print(os.getcwd())

from utility_functions import * 
from parametric_shape import * 

salome.standalone()
salome.salome_init()
import salome_notebook
notebook = salome_notebook.NoteBook()


#################################################################
###
###     GEOM component -- Setting up geometry computation
###
#################################################################

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

geompy.addToStudy( x, 'x' )
geompy.addToStudy( y, 'y' )
geompy.addToStudy( z, 'z' )

waveLenght = 8.661

boxSide = waveLenght/2 + 2 * waveLenght/40

pml_inlet_height = 2.573

pml_inlet = geompy.MakeBoxDXDYDZ(boxSide, boxSide, pml_inlet_height)

air_inlet_height = 4.288


box_1 = geompy.MakeTranslation( geompy.MakeBoxDXDYDZ( boxSide, boxSide, air_inlet_height), 0, 0, pml_inlet_height )

box_2 = geompy.MakeTranslation( geompy.MakeBoxDXDYDZ( boxSide, boxSide, air_inlet_height*3 ), 0, 0, pml_inlet_height + air_inlet_height + waveLenght )

pml_outlet = geompy.MakeTranslation( pml_inlet, 0, 0, pml_inlet_height + air_inlet_height + waveLenght + 3*air_inlet_height )

air = geompy.MakeTranslation( geompy.MakeBoxDXDYDZ( boxSide, boxSide, waveLenght), \
                                      0, 0, \
                                      pml_inlet_height + air_inlet_height )

air = geompy.MakeFuseList( [box_1, box_2, air], True, True)
# geompy.addToStudy( air, 'Air' )

Structure = geompy.MakePartition([pml_inlet, pml_outlet, air], [], [], [], geompy.ShapeType["SOLID"], 0, [], 0)

solids = [Solid_1, Solid_2, Solid_3] = geompy.ExtractShapes(Structure, geompy.ShapeType["SOLID"], True)
# print(solids)

faces = [Face_1, Face_2, Face_3, Face_4, Face_5, Face_6, Face_7, Face_8, Face_9,\
        Face_10, Face_11, Face_12, Face_13, Face_14, Face_15, Face_16] = geompy.ExtractShapes(Structure, geompy.ShapeType["FACE"], True)

faces = geompy.ExtractShapes(Structure, geompy.ShapeType["FACE"], True) # generates 16 faces instead of 54
# print(len(faces))



# Autogroups in geometry for meshing

# TODO: Encapsulate behaviour

Auto_group_for_left = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set left walls
geompy.UnionList(Auto_group_for_left, [Face_1, Face_2, Face_3])

Auto_group_for_front = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set front walls
geompy.UnionList(Auto_group_for_front, [Face_4, Face_5, Face_6])

Auto_group_for_top_bottom_walls = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set top & bottom walls
geompy.UnionList(Auto_group_for_top_bottom_walls, [Face_7, Face_10] ) 

Auto_group_for_inlet = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set inlet walls
geompy.UnionList(Auto_group_for_inlet, [Face_8])

Auto_group_for_outlet = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set outlet walls
geompy.UnionList(Auto_group_for_outlet, [Face_9])

Auto_group_for_back = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set back walls
geompy.UnionList(Auto_group_for_back, [Face_11, Face_12, Face_13])

Auto_group_for_right = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set right walls
geompy.UnionList(Auto_group_for_right, [Face_14, Face_15, Face_16])



# Add autogroups to study

geompy.addToStudyInFather(Structure, Auto_group_for_right, 'Auto_group_for_right')
geompy.addToStudyInFather(Structure, Auto_group_for_left, 'Auto_group_for_left')
geompy.addToStudyInFather(Structure, Auto_group_for_back, 'Auto_group_for_back')
geompy.addToStudyInFather(Structure, Auto_group_for_top_bottom_walls, 'Auto_group_for_top_bottom_walls')
geompy.addToStudyInFather(Structure, Auto_group_for_front, 'Auto_group_for_front')

# Add to solids & faces to study
geompy.addToStudy(Structure, 'Structure-{}'.format('no-brick') )
for num, f in enumerate(faces): # add faces to study
  geompy.addToStudyInFather(Structure, f, 'face_{}'.format(num + 1) )  
for num, s in enumerate(solids): # add solids to study
  geompy.addToStudyInFather(Structure, s, 'solid_{}'.format(num + 1))  

end = time.time()

print("Geometry computation time: {:.2f} sec".format(end - start))


#################################################################
###
###     SMESH component -- Setting up Mesh computation
###
#################################################################


import SMESH, SALOMEDS
from salome.smesh import smeshBuilder

print("Mesh computation time: {:.2f} sec".format(end - start))

smesh = smeshBuilder.New()

start = time.time()



Structure_1 = smesh.Mesh(Structure)
NETGEN_1D_2D_3D = Structure_1.Tetrahedron( algo=smeshBuilder.NETGEN_1D2D3D )
NETGEN_3D_Parameters_1 = NETGEN_1D_2D_3D.Parameters()
NETGEN_3D_Parameters_1.SetMaxSize( 0.5 )
# At 40 kHz the wavelength is around 8.5 mm. With standard nodal FEs you need at least ~10 elements per wave. 
# Mesh size, h, should be smaller than 1 mm in order to capture the phenomena.
NETGEN_3D_Parameters_1.SetMinSize( 0.944741 ) 
# NETGEN_3D_Parameters_1.SetMaxSize( 0.619 )
# NETGEN_3D_Parameters_1.SetMaxSize( 3.1461 )
# NETGEN_3D_Parameters_1.SetMinSize( 0.0844741 )
# NETGEN_3D_Parameters_1.SetMaxSize( 3.1461 )
# NETGEN_3D_Parameters_1.SetMinSize( 0.0844741 )
NETGEN_3D_Parameters_1.SetSecondOrder( 0 )
# NETGEN_3D_Parameters_1.SetSecondOrder( 0 )
NETGEN_3D_Parameters_1.SetOptimize( 1 )
NETGEN_3D_Parameters_1.SetFineness( 4 ) # VeryFine = 4
NETGEN_3D_Parameters_1.SetChordalError( -1 )
NETGEN_3D_Parameters_1.SetChordalErrorEnabled( 0 )
NETGEN_3D_Parameters_1.SetUseSurfaceCurvature( 1 )
NETGEN_3D_Parameters_1.SetFuseEdges( 1 )
NETGEN_3D_Parameters_1.SetQuadAllowed( 0 )
NETGEN_3D_Parameters_1.SetCheckChartBoundary( 72 )

# Add meshing groups
pml_inlet_mesh = Structure_1.GroupOnGeom(Solid_1,'pml_inlet',SMESH.VOLUME)
air = Structure_1.GroupOnGeom(Solid_2,'air',SMESH.VOLUME)
pml_outlet_mesh = Structure_1.GroupOnGeom(Solid_3,'pml_outlet',SMESH.VOLUME)


top_bottom_walls = Structure_1.GroupOnGeom(Auto_group_for_top_bottom_walls,'Auto_group_for_top_bottom_walls',SMESH.FACE)
top_bottom_walls.SetName( 'top_bottom_walls' )

inlet = Structure_1.GroupOnGeom(Auto_group_for_inlet,'Auto_group_for_inlet',SMESH.FACE)
inlet.SetName('inlet')
outlet = Structure_1.GroupOnGeom(Auto_group_for_outlet,'Auto_group_for_outlet',SMESH.FACE)
outlet.SetName('outlet')

left = Structure_1.GroupOnGeom(Auto_group_for_left,'left',SMESH.FACE)
front = Structure_1.GroupOnGeom(Auto_group_for_front,'front',SMESH.FACE)
back = Structure_1.GroupOnGeom(Auto_group_for_back,'back',SMESH.FACE)
right = Structure_1.GroupOnGeom(Auto_group_for_right,'right',SMESH.FACE)

isDone = Structure_1.Compute()

# Add groups in mesh.unv
[pml_inlet, pml_outlet, air, top_bottom_walls, inlet, outlet, left, front, back, right ] = Structure_1.GetGroups()

# [pml_inlet, pml_outlet, brick, air, top_bottom_walls, inlet, outlet, brick_faces, brick_left, brick_front, brick_back, brick_right, left, front, back, right ] = Structure_1.GetGroups()


# Mesh computation time
end = time.time()
print("Mesh computation time: {:.2f} sec".format(end - start))

# Rename bodies for Elmer
# smesh.SetName(solids_mesh[0], 'pml_bot')
# smesh.SetName(solids_mesh[1], 'brick')
# smesh.SetName(solids_mesh[2], 'air')
# smesh.SetName(solids_mesh[3], 'pml_outlet')

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


print('#args', sys.argv)

start = time.time()

try:
  # Generate brick folder
  newpath = f'C:/Users/francisco/Documents/dev/pipeline/data/'
  if not os.path.exists(newpath):
    os.makedirs(newpath)
  os.chdir(newpath)
  Structure_1.ExportUNV( r'C:/Users/francisco/Documents/dev/pipeline/data/_no-brick.unv' )
  pass
except:
  print('ExportUNV() failed. Invalid file name?')

  # time.sleep(0.5)

  # if not os.path.exists(newpath + '/structure.unv'):
  #   print(f'.unv file does NOT exist in {newpath}')
  # if os.path.exists(newpath + '/structure.unv'):
  #   print(f'.unv file exists in {newpath}')

try:
  # Export mesh to Elmer
  # if os.path.exists(newpath + '/structure.unv'):
  export_elmer('_no-brick')
  # copy_elmer_template( f'brick-{brickID}' )
  pass
except: 
  print('Could not find UNV file.')


if len(sys.argv[1:]) >= 2:
  start_frequency = int(sys.argv[1:][1])
  end_frequency = int(sys.argv[1:][2])
  step = int(sys.argv[1:][3])
  print('checkpoint brick-{}'.format(0), start_frequency, end_frequency, step )
  copy_elmer_templates( '_no-brick', start_frequency, end_frequency, step )
else:
  # copy elmer template for 40 KHz
  copy_elmer_templates( '_no-brick'.format(0), 40000, 41000, 1000 )


end = time.time()
print("Salome to Elmer computation time: {:.2f} sec".format(end - start))

if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser()
