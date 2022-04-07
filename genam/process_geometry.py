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




barLen = {  'b1': 0.062, 
            'b2': 0.092, 
            'b3': 0.112, 
            'b4': 0.132, 
            'b5': 0.152, 
            'b6': 0.162, 
            'b7': 0.171, 
            'b8': 0.191, 
            'b9': 0.221, 
            'b10': 0.241, 
            'b11': 0.251, 
            'b12': 0.271, 
            'b13': 0.281, 
            'b14': 0.301, 
            'b15': 0.321 
          }

barSpa = {  'b1': 0.216, 
            'b2': 0.212, 
            'b3': 0.207,
            'b4': 0.189, 
            'b5': 0.161, 
            'b6': 0.166, 
            'b7': 0.171, 
            'b8': 0.134, 
            'b9': 0.257, 
            'b10': 0.234, 
            'b11': 0.230, 
            'b12': 0.207, 
            'b13': 0.203, 
            'b14': 0.175, 
            'b15': 0.152 
          }

filletRad = { 'b1': 0.062, 
              'b2': 0.092, 
              'b3': 0.1,
              'b4': 0.1, 
              'b5': 0.1, 
              'b6': 0.1, 
              'b7': 0.1, 
              'b8': 0.1, 
              'b9': 0.1, 
              'b10': 0.1, 
              'b11': 0.1, 
              'b12': 0.1, 
              'b13': 0.1, 
              'b14': 0.1, 
              'b15': 0.1 
          }

# Parse CLI arguments
if len(sys.argv[1:]) >= 1:
  brickID = int(sys.argv[1:][0])
else:
  brickID = 15

print("Generating brick #" + str(brickID) )

barLength = list(barLen.values())[brickID - 1] * waveLenght
barSpacing = list(barSpa.values())[brickID -1] * waveLenght




Sketch_1 = parameterize_2D_inner_shape( waveLenght, barLength, barSpacing )
# geompy.addToStudy( Sketch_1, 'Sketch' )

### Convert sketch to 3d object
rotation = [(x, 90)]
translation = ( waveLenght/40, waveLenght/40 + waveLenght/2, 6.861)

brick_inner = sketch_to_volume( geompy, Sketch_1, waveLenght/2, rotation, translation)
# geompy.addToStudy( brick_inner, 'Inner' )

brick_outer = geompy.MakeTranslation( geompy.MakeBoxDXDYDZ( boxSide, boxSide, waveLenght), \
                                      0, 0, \
                                      pml_inlet_height + air_inlet_height )

brick_fused = geompy.MakeFuseList([brick_outer, brick_inner], True, True)
# geompy.addToStudy( brick_fused, 'Fused' )

brick = geompy.MakeCutList( brick_fused, [brick_inner], True)
# geompy.addToStudy( brick, 'Brick' )

air = geompy.MakeFuseList( [box_1, box_2, brick_inner], True, True)
# geompy.addToStudy( air, 'Air' )

Structure = geompy.MakePartition([pml_inlet, pml_outlet, brick, air], [], [], [], geompy.ShapeType["SOLID"], 0, [], 0)
# geompy.addToStudy( Structure, 'Structure' )




solids = [Solid_1, Solid_2, Solid_3, Solid_4] = geompy.ExtractShapes(Structure, geompy.ShapeType["SOLID"], True)


print(solids)

faces = [Face_1, Face_2, Face_3, Face_4, Face_5, Face_6, Face_7, Face_8, Face_9,\
        Face_10, Face_11, Face_12, Face_13, Face_14, Face_15, Face_16, Face_17, \
        Face_18, Face_19, Face_20, Face_21, Face_22, Face_23, Face_24, Face_25, \
        Face_26, Face_27, Face_28, Face_29, Face_30, Face_31, Face_32, Face_33, \
        Face_34, Face_35, Face_36, Face_37, Face_38, Face_39, Face_40, Face_41, \
        Face_42, Face_43, Face_44, Face_45, Face_46, Face_47, Face_48, Face_49, \
        Face_50, Face_51, Face_52, Face_53, Face_54] = geompy.ExtractShapes(Structure, geompy.ShapeType["FACE"], True)

# faces = geompy.ExtractShapes(Structure, geompy.ShapeType["FACE"], True) # generates 59 faces instead of 54
# print(len(faces))

# Autogroups in geometry for meshing



# TODO: Encapsulate behaviour

if brickID in [1,2,7,8,9]: 

  Auto_group_for_left = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set left walls
  geompy.UnionList(Auto_group_for_left, [Face_1, Face_2, Face_4, Face_5])

  Auto_group_for_front = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set front walls
  geompy.UnionList(Auto_group_for_front, [Face_19, Face_20, Face_22, Face_23])

  Auto_group_for_top_bottom_walls = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set top & bottom walls
  geompy.UnionList(Auto_group_for_top_bottom_walls, [Face_25, Face_30] ) 

  Auto_group_for_inlet = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set inlet walls
  geompy.UnionList(Auto_group_for_inlet, [Face_26])
  
  Auto_group_for_outlet = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set outlet walls
  geompy.UnionList(Auto_group_for_outlet, [Face_29])

  Auto_group_for_back = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set back walls
  geompy.UnionList(Auto_group_for_back, [Face_32, Face_33, Face_35, Face_36])

  Auto_group_for_right = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set right walls
  geompy.UnionList(Auto_group_for_right, [Face_50, Face_51, Face_53, Face_54])
  

  Auto_group_for_brick_faces = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set brick faces
  geompy.UnionList(Auto_group_for_brick_faces, [Face_3, \
                                                Face_6, Face_7, Face_8, Face_9, Face_10, Face_11, Face_12, Face_13, Face_14, Face_15, Face_16, Face_17, Face_18, 
                                                Face_21, \
                                                Face_24, \
                                                Face_27, Face_28, \
                                                Face_31, \
                                                Face_34, \
                                                Face_37, Face_38, Face_39, Face_40, Face_41, Face_42, Face_43, Face_44, Face_45, Face_46, Face_47, Face_48, Face_49, \
                                                Face_52])


elif brickID in [3,5]: 

  Auto_group_for_left = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set left walls
  geompy.UnionList(Auto_group_for_left, [Face_1, Face_2, Face_4, Face_5])

  Auto_group_for_front = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set front walls
  geompy.UnionList(Auto_group_for_front, [Face_17, Face_18, Face_20, Face_21])
  # geompy.UnionList(Auto_group_for_front, [Face_17, Face_19, Face_22, Face_23])

  Auto_group_for_top_bottom_walls = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set top & bottom walls
  geompy.UnionList(Auto_group_for_top_bottom_walls, [Face_25, Face_30] ) 

  Auto_group_for_inlet = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set right walls
  geompy.UnionList(Auto_group_for_inlet, [Face_26])
  
  Auto_group_for_outlet = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set right walls
  geompy.UnionList(Auto_group_for_outlet, [Face_29])

  Auto_group_for_back = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set back walls
  geompy.UnionList(Auto_group_for_back, [Face_34, Face_35, Face_37, Face_38])
  # geompy.UnionList(Auto_group_for_back, [Face_32, Face_33, Face_37, Face_38])
  
  Auto_group_for_right = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set right walls
  geompy.UnionList(Auto_group_for_right, [Face_50, Face_51, Face_53, Face_54])

  Auto_group_for_brick_faces = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set brick faces
  geompy.UnionList(Auto_group_for_brick_faces, [Face_3, \
                                                Face_6, Face_7, Face_8, Face_9, Face_10, Face_11, Face_12, Face_13, Face_14, Face_15, Face_16, \
                                                Face_19, \
                                                Face_22, Face_23, Face_24, \
                                                Face_27, Face_28, \
                                                Face_31, Face_32, Face_33, \
                                                Face_36, \
                                                Face_39, Face_40, Face_41, Face_42, Face_43, Face_44, Face_45, Face_46, Face_47, Face_48, Face_49, \
                                                Face_52])

elif brickID==4: 

  Auto_group_for_left = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set left walls
  geompy.UnionList(Auto_group_for_left, [Face_1, Face_2, Face_4, Face_5])

  Auto_group_for_front = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set front walls
  geompy.UnionList(Auto_group_for_front, [Face_17, Face_18, Face_20, Face_21])
  
  Auto_group_for_top_bottom_walls = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set top & bottom walls
  geompy.UnionList(Auto_group_for_top_bottom_walls, [Face_25, Face_31] ) 
  # geompy.UnionList(Auto_group_for_top_bottom_walls, [Face_25, Face_30] ) 

  Auto_group_for_inlet = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set inlet walls
  geompy.UnionList(Auto_group_for_inlet, [Face_26])
  
  Auto_group_for_outlet = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set outlet walls
  geompy.UnionList(Auto_group_for_outlet, [Face_29])
  
  Auto_group_for_back = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set back walls
  geompy.UnionList(Auto_group_for_back, [Face_34, Face_35, Face_37, Face_38])
    
  Auto_group_for_right = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set right walls
  geompy.UnionList(Auto_group_for_right, [Face_50, Face_51, Face_53, Face_54])
  

  Auto_group_for_brick_faces = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set brick faces
  geompy.UnionList(Auto_group_for_brick_faces, [Face_3, \
                                                Face_6, Face_7, Face_8, Face_9, Face_10, Face_11, Face_12, Face_13, Face_14, Face_15, Face_16, \
                                                Face_19, \
                                                Face_22, Face_23, Face_24, \
                                                Face_27, Face_28, \
                                                Face_30, Face_32, Face_33, \
                                                Face_36, \
                                                Face_39, Face_40, Face_41, Face_42, Face_43, Face_44, Face_45, Face_46, Face_47, Face_48, Face_49, \
                                                Face_52])


elif brickID==6: 

  Auto_group_for_left = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set left walls
  geompy.UnionList(Auto_group_for_left, [Face_1, Face_2, Face_4, Face_5])

  Auto_group_for_front = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set front walls
  geompy.UnionList(Auto_group_for_front, [Face_17, Face_19, Face_22, Face_23])
  # geompy.UnionList(Auto_group_for_front, [Face_19, Face_20, Face_22, Face_23])

  Auto_group_for_top_bottom_walls = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set top & bottom walls
  geompy.UnionList(Auto_group_for_top_bottom_walls, [Face_25, Face_30] ) 
  
  Auto_group_for_inlet = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set right walls
  geompy.UnionList(Auto_group_for_inlet, [Face_26])
  
  Auto_group_for_outlet = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set right walls
  geompy.UnionList(Auto_group_for_outlet, [Face_29])
  
  Auto_group_for_back = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set back walls
  geompy.UnionList(Auto_group_for_back, [Face_32, Face_33, Face_37, Face_38])
  # geompy.UnionList(Auto_group_for_back, [Face_32, Face_33, Face_35, Face_36])

  Auto_group_for_right = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set right walls
  geompy.UnionList(Auto_group_for_right, [Face_50, Face_51, Face_53, Face_54])
  
  Auto_group_for_brick_faces = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set brick faces
  geompy.UnionList(Auto_group_for_brick_faces, [Face_3, \
                                                Face_6, Face_7, Face_8, Face_9, Face_10, Face_11, Face_12, Face_13, Face_14, Face_15, Face_16, \
                                                Face_18, \
                                                Face_21, \
                                                Face_24, \
                                                Face_27, Face_28, \
                                                Face_31, \
                                                Face_34, Face_35, Face_36, \
                                                Face_39, Face_40, Face_41, Face_42, Face_43, Face_44, Face_45, Face_46, \
                                                Face_47, Face_48, Face_49, \
                                                Face_52])


elif brickID == 10: 

  Auto_group_for_left = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set left walls
  geompy.UnionList(Auto_group_for_left, [Face_1, Face_2, Face_4, Face_5])

  Auto_group_for_front = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set front walls
  geompy.UnionList(Auto_group_for_front, [Face_19, Face_20, Face_22, Face_23])
  # geompy.UnionList(Auto_group_for_front, [Face_17, Face_18, Face_20, Face_21])
  
  Auto_group_for_back = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set back walls
  geompy.UnionList(Auto_group_for_back, [Face_32, Face_33, Face_35, Face_36])
  # geompy.UnionList(Auto_group_for_back, [Face_34, Face_35, Face_37, Face_38])
  
  Auto_group_for_top_bottom_walls = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set top & bottom walls
  geompy.UnionList(Auto_group_for_top_bottom_walls, [Face_25, Face_30] ) 

  Auto_group_for_right = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set right walls
  geompy.UnionList(Auto_group_for_right, [Face_50, Face_51, Face_53, Face_54])
  
  Auto_group_for_inlet = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set inlet walls
  geompy.UnionList(Auto_group_for_inlet, [Face_26])
  
  Auto_group_for_outlet = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set outlet walls
  geompy.UnionList(Auto_group_for_outlet, [Face_29])

  Auto_group_for_brick_faces = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set brick faces
  geompy.UnionList(Auto_group_for_brick_faces, [Face_3, \
                                                Face_6, Face_7, Face_8, Face_9, Face_10, Face_11, Face_12, Face_13, Face_14, Face_15, Face_16, Face_17, Face_18, \
                                                Face_21, \
                                                Face_24, \
                                                Face_27, Face_28, \
                                                Face_31, \
                                                Face_34, \
                                                Face_37, Face_38, Face_39, Face_40, Face_41, Face_42, Face_43, Face_44, Face_45, Face_46, \
                                                Face_47, Face_48, Face_49, \
                                                Face_52])



elif brickID == 14: 
  
  Auto_group_for_left = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set left walls
  geompy.UnionList(Auto_group_for_left, [Face_1, Face_2, Face_4, Face_5])

  Auto_group_for_front = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set front walls
  geompy.UnionList(Auto_group_for_front, [Face_15, Face_16, Face_18, Face_19])

  Auto_group_for_top_bottom_walls = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set top & bottom walls
  geompy.UnionList(Auto_group_for_top_bottom_walls, [Face_21, Face_34] ) 
  # geompy.UnionList(Auto_group_for_top_bottom_walls, [Face_25, Face_30] ) 

  Auto_group_for_inlet = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set inlet walls
  geompy.UnionList(Auto_group_for_inlet, [Face_22])
  # geompy.UnionList(Auto_group_for_inlet, [Face_26])
  
  Auto_group_for_outlet = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set outlet walls
  geompy.UnionList(Auto_group_for_outlet, [Face_33])
  # geompy.UnionList(Auto_group_for_outlet, [Face_29])

  Auto_group_for_back = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set back walls
  geompy.UnionList(Auto_group_for_back, [Face_36, Face_37, Face_39, Face_40])

  Auto_group_for_right = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set right walls
  geompy.UnionList(Auto_group_for_right, [Face_50, Face_51, Face_53, Face_54])

  Auto_group_for_brick_faces = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set brick faces
  geompy.UnionList(Auto_group_for_brick_faces, [Face_3, \
                                                Face_6, Face_7, Face_8, Face_9, Face_10, Face_11, Face_12, Face_13, Face_14, \
                                                Face_17, \
                                                Face_20, \
                                                Face_23, Face_24, Face_25, \
                                                Face_26, Face_27, Face_28, Face_29, Face_30, Face_31, Face_32, \
                                                Face_35, \
                                                Face_38, \
                                                Face_41, Face_42, Face_43, Face_44, Face_45, Face_46, Face_47, Face_48, Face_49, \
                                                Face_52])


elif brickID in [11, 12, 13, 15]: 
  
  Auto_group_for_left = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set left walls
  geompy.UnionList(Auto_group_for_left, [Face_1, Face_2, Face_4, Face_5])

  Auto_group_for_front = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set front walls
  geompy.UnionList(Auto_group_for_front, [Face_15, Face_16, Face_18, Face_19])

  Auto_group_for_top_bottom_walls = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set top & bottom walls
  geompy.UnionList(Auto_group_for_top_bottom_walls, [Face_25, Face_30] ) 

  Auto_group_for_inlet = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set inlet walls
  geompy.UnionList(Auto_group_for_inlet, [Face_26])
  
  Auto_group_for_outlet = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set outlet walls
  geompy.UnionList(Auto_group_for_outlet, [Face_29])

  Auto_group_for_back = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set back walls
  geompy.UnionList(Auto_group_for_back, [Face_36, Face_37, Face_39, Face_40])

  Auto_group_for_right = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set right walls
  geompy.UnionList(Auto_group_for_right, [Face_50, Face_51, Face_53, Face_54])

  Auto_group_for_brick_faces = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set brick faces

  geompy.UnionList(Auto_group_for_brick_faces, [Face_3, \
                                                Face_6, Face_7, Face_8, Face_9, Face_10, Face_11, Face_12, Face_13, Face_14, \
                                                Face_17, \
                                                Face_20, Face_21, Face_22, Face_23, Face_24, \
                                                Face_27, Face_28,   
                                                Face_31, Face_32, Face_33, Face_34, Face_35, \
                                                Face_38, \
                                                Face_41, Face_42, Face_43, Face_44, Face_45, Face_46, Face_47, Face_48, Face_49, \
                                                Face_52])


# Add autogroups to study


geompy.addToStudyInFather(Structure, Auto_group_for_right, 'Auto_group_for_right')
geompy.addToStudyInFather(Structure, Auto_group_for_left, 'Auto_group_for_left')
geompy.addToStudyInFather(Structure, Auto_group_for_back, 'Auto_group_for_back')
geompy.addToStudyInFather(Structure, Auto_group_for_top_bottom_walls, 'Auto_group_for_top_bottom_walls')
geompy.addToStudyInFather(Structure, Auto_group_for_brick_faces, 'Auto_group_for_brick_faces')
geompy.addToStudyInFather(Structure, Auto_group_for_front, 'Auto_group_for_front')

# Add to solids & faces to study
geompy.addToStudy(Structure, 'Structure-{}'.format(brickID) )
for num, f in enumerate(faces): # add faces to study
  geompy.addToStudyInFather(Structure, f, 'face_{}'.format(num + 1) )  
for num, s in enumerate(solids): # add solids to study
  geompy.addToStudyInFather(Structure, s, 'solid_{}'.format(num + 1))  

geompy.addToStudy(Sketch_1, 'Sketch') 

end = time.time()
print("Geometry computation time: {:.2f} sec".format(end - start))


#################################################################
###
###     SMESH component -- Setting up Mesh computation
###
#################################################################


import SMESH, SALOMEDS
from salome.smesh import smeshBuilder

smesh = smeshBuilder.New()

start = time.time()


Structure_1 = smesh.Mesh(Structure)
NETGEN_1D_2D_3D = Structure_1.Tetrahedron( algo=smeshBuilder.NETGEN_1D2D3D )
NETGEN_3D_Parameters_1 = NETGEN_1D_2D_3D.Parameters()
# At 40 kHz the wavelength is around 8.5 mm. With standard nodal FEs you need at least ~10 elements per wave. 
# Mesh size, h, should be smaller than 1 mm in order to capture the phenomena.
NETGEN_3D_Parameters_1.SetMaxSize( 0.9461 )
NETGEN_3D_Parameters_1.SetMinSize( 0.1041 ) 
# NETGEN_3D_Parameters_1.SetMaxSize( 0.9461 )
# NETGEN_3D_Parameters_1.SetMinSize( 0.1041 ) 
# NETGEN_3D_Parameters_1.SetMaxSize( 3.1461 )
# NETGEN_3D_Parameters_1.SetMaxSize( 0.619 )
# NETGEN_3D_Parameters_1.SetMinSize( 0.0844741 )
# NETGEN_3D_Parameters_1.SetMinSize( 0.0844741 )
NETGEN_3D_Parameters_1.SetSecondOrder( 1 )
# NETGEN_3D_Parameters_1.SetSecondOrder( 0 )
NETGEN_3D_Parameters_1.SetOptimize( 1 )
NETGEN_3D_Parameters_1.SetFineness( 4 )
NETGEN_3D_Parameters_1.SetChordalError( -1 )
NETGEN_3D_Parameters_1.SetChordalErrorEnabled( 0 )
NETGEN_3D_Parameters_1.SetUseSurfaceCurvature( 1 )
NETGEN_3D_Parameters_1.SetFuseEdges( 1 )
NETGEN_3D_Parameters_1.SetQuadAllowed( 0 )
NETGEN_3D_Parameters_1.SetCheckChartBoundary( 72 )

# Add meshing groups
pml_inlet_mesh = Structure_1.GroupOnGeom(Solid_1,'pml_inlet',SMESH.VOLUME)
brick_mesh = Structure_1.GroupOnGeom(Solid_2,'brick',SMESH.VOLUME)
air_mesh = Structure_1.GroupOnGeom(Solid_3,'air',SMESH.VOLUME)
pml_outlet_mesh = Structure_1.GroupOnGeom(Solid_4,'pml_outlet',SMESH.VOLUME)

top_bottom_walls = Structure_1.GroupOnGeom(Auto_group_for_top_bottom_walls,'Auto_group_for_top_bottom_walls',SMESH.FACE)
top_bottom_walls.SetName( 'top_bottom_walls' )

inlet = Structure_1.GroupOnGeom(Auto_group_for_inlet,'Auto_group_for_inlet',SMESH.FACE)
inlet.SetName('inlet')
outlet = Structure_1.GroupOnGeom(Auto_group_for_outlet,'Auto_group_for_outlet',SMESH.FACE)
outlet.SetName('outlet')

brick_faces = Structure_1.GroupOnGeom(Auto_group_for_brick_faces,'Auto_group_for_brick_faces',SMESH.FACE)
brick_faces.SetName('brick_faces')


# TODO: Encapsulate behaviour

if brickID in [11,12,13,14,15]:
  brick_left = Structure_1.GroupOnGeom(Face_3,'Face_3',SMESH.FACE)
  brick_left.SetName('brick_left')
  brick_front = Structure_1.GroupOnGeom(Face_17,'Face_17',SMESH.FACE)
  brick_front.SetName('brick_front')  
  brick_back = Structure_1.GroupOnGeom(Face_38,'Face_38',SMESH.FACE)
  brick_back.SetName('brick_back')
  brick_right = Structure_1.GroupOnGeom(Face_52,'Face_52',SMESH.FACE)
  brick_right.SetName('brick_right')
elif brickID not in [3,4,5]:
  brick_left = Structure_1.GroupOnGeom(Face_3,'Face_3',SMESH.FACE)
  brick_left.SetName('brick_left')
  brick_front = Structure_1.GroupOnGeom(Face_21,'Face_21',SMESH.FACE)
  brick_front.SetName('brick_front')
  brick_back = Structure_1.GroupOnGeom(Face_34,'Face_34',SMESH.FACE)
  brick_back.SetName('brick_back')
  brick_right = Structure_1.GroupOnGeom(Face_52,'Face_52',SMESH.FACE)
  brick_right.SetName('brick_right')
else:  
  brick_left = Structure_1.GroupOnGeom(Face_3,'Face_3',SMESH.FACE)
  brick_left.SetName('brick_left')
  brick_front = Structure_1.GroupOnGeom(Face_19,'Face_19',SMESH.FACE)
  brick_front.SetName('brick_front')
  brick_back = Structure_1.GroupOnGeom(Face_36,'Face_36',SMESH.FACE)
  brick_back.SetName('brick_back')
  brick_right = Structure_1.GroupOnGeom(Face_52,'Face_52',SMESH.FACE)
  brick_right.SetName('brick_right')



left = Structure_1.GroupOnGeom(Auto_group_for_left,'left',SMESH.FACE)
front = Structure_1.GroupOnGeom(Auto_group_for_front,'front',SMESH.FACE)
back = Structure_1.GroupOnGeom(Auto_group_for_back,'back',SMESH.FACE)
right = Structure_1.GroupOnGeom(Auto_group_for_right,'right',SMESH.FACE)

isDone = Structure_1.Compute()

# Add groups in mesh.unv
# [pml_inlet, pml_outlet, brick, air, top_bottom_walls, inlet, outlet, brick_faces, left, front, back, right ] = Structure_1.GetGroups()
[pml_inlet, pml_outlet, brick, air, top_bottom_walls, inlet, outlet, brick_faces, brick_left, brick_front, brick_back, brick_right, left, front, back, right ] = Structure_1.GetGroups()


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
  newpath = f'C:/Users/francisco/Documents/dev/pipeline/data'
  if not os.path.exists(newpath):
    os.makedirs(newpath)
  os.chdir(newpath)
  Structure_1.ExportUNV( r'C:/Users/francisco/Documents/dev/pipeline/data/brick-{}.unv'.format(brickID) )
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
  export_elmer( 'brick-{}'.format(brickID) )
  # copy_elmer_template( f'brick-{brickID}' )
  pass
except: 
  print('Could not find UNV file.')


if len(sys.argv[1:]) >= 2:
  start_frequency = int(sys.argv[1:][1])
  end_frequency = int(sys.argv[1:][2])
  step = int(sys.argv[1:][3])
  print('checkpoint brick-{}'.format(brickID), start_frequency, end_frequency, step )
  copy_elmer_templates( 'brick-{}'.format(brickID), start_frequency, end_frequency, step )
else:
  # copy elmer template for 40 KHz
  copy_elmer_templates( 'brick-{}'.format(brickID), 40000, 41000, 1000 )


end = time.time()
print("Salome to Elmer computation time: {:.2f} sec".format(end - start))

if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser()
