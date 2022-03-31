import sys
import salome
import numpy as np
# import pandas as pd
import time, os
import random

# os.chdir(r"C:/Users/Francisco/Documents/dev/pipeline")
# sys.path.insert(0, r'C:/Users/Francisco/Documents/dev/pipeline')
os.chdir(r"C:/Users/francisco/Documents/dev/pipeline/ammgdop")
sys.path.insert(0, r'C:/Users/francisco/Documents/dev/pipeline/ammgdop')

from utility_functions import * 
from parametric_shape import * 

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

### SMESH component
###

import  SMESH, SALOMEDS
from salome.smesh import smeshBuilder
from salome.GMSHPlugin import GMSHPluginBuilder


data = { 
  'length':   [.062, .092, .112, .132, .152, .162, .171, .191, .221, .241, .251, .271, .281, .301, .321],
  'distance': [.216, .212, .207, .189, .161, .166, .171, .134, .257, .234, .230, .207, .203, .175, .152],  
  'radius':   [.062, .092, .1, .1, .1, .1, .1, .1, .1, .1, .1, .1, .1, .1, .1] 
}


def process_geometry(data):

  start = time.time()
  geompy = geomBuilder.New()


  origin = geompy.MakeVertex(0, 0, 0)

  x = geompy.MakeVectorDXDYDZ(1, 0, 0)
  y = geompy.MakeVectorDXDYDZ(0, 1, 0)
  z = geompy.MakeVectorDXDYDZ(0, 0, 1)

  geompy.addToStudy( x, 'x' )
  geompy.addToStudy( y, 'y' )
  geompy.addToStudy( z, 'z' )

  probing_distance = 100

  lens_grid_n = 8 
  
  waveLenght = 8.661

  lens_side = waveLenght/40 + lens_grid_n * (waveLenght/2 + waveLenght/40)

  array_side = 2* waveLenght/40 + waveLenght/2

  boxSide = waveLenght/2 + 2 * waveLenght/40
  
  pml_bottom_height = 2.573
  # pml_bottom_height = 0
 
  air_bottom_height = 4.288
 
  y_translation_shift = -(waveLenght/40 + 4*(waveLenght/2 + waveLenght/40))
 
  counter = 0


  #################################


  pml_bottom = geompy.MakeTranslation( geompy.MakeBoxDXDYDZ( array_side, lens_side, pml_bottom_height), \
                                        0, y_translation_shift, \
                                        0 )
  # geompy.addToStudy( pml_bottom, 'pml_bottom' )

  pml_bottom_faces = geompy.ExtractShapes(pml_bottom, geompy.ShapeType["FACE"], True)

  for num, f in enumerate(pml_bottom_faces): # add faces to study
    counter += 1
    # geompy.addToStudyInFather( pml_bottom, f, 'face_{}'.format(counter) )



  #################################

  air_inlet = geompy.MakeTranslation( geompy.MakeBoxDXDYDZ( array_side, lens_side, air_bottom_height),
                                      0, y_translation_shift,
                                      pml_bottom_height )
  # geompy.addToStudy( air_inlet, 'air_inlet' )
  
  air_inlet_faces = geompy.ExtractShapes(air_inlet, geompy.ShapeType["FACE"], True)
  
  for num, f in enumerate(air_inlet_faces): # add faces to study
    counter += 1
    # geompy.addToStudyInFather(air_inlet, f, 'face_{}'.format(counter) ) 

  #################################

  # section_intersect_PML_in_air_in = geompy.MakeFaceWires([ geompy.MakeSection(pml_bottom, air_inlet) ], 1) 


  # id_section = geompy.addToStudy(section_intersect_PML_in_air_in, "intersect_PML_air_in")
  # print(section_intersect_PML_in_air_in)
  # print(type(section_intersect_PML_in_air_in))
  # print( section_intersect_PML_in_air_in.GetType() )

  # isOk, res1, res2 = geompy.FastIntersect(pml_bottom, air_inlet)

  # print('OK {} res1 {} res2 {}'.format(isOk, res1, res2))

  #################################

  lens_outer = geompy.MakeTranslation(  geompy.MakeBoxDXDYDZ( array_side, lens_side, waveLenght ),
                                        0, y_translation_shift,
                                        pml_bottom_height + air_bottom_height )
  # geompy.addToStudy( lens_outer, 'lens_outer' )

  #################################

  air_height = probing_distance - (pml_bottom_height + air_bottom_height + waveLenght)

  #################################
  # box_2 = geompy.MakeTranslation( geompy.MakeBoxDXDYDZ(  array_side, lens_side, air_bottom_height*3 ),\
  air_outlet = geompy.MakeTranslation( geompy.MakeBoxDXDYDZ( array_side, lens_side, air_height ),\
                                        0, y_translation_shift, \
                                        pml_bottom_height + air_bottom_height + waveLenght )
  # geompy.addToStudy( air_outlet, 'air_outlet' )
  air_outlet_faces = geompy.ExtractShapes(air_outlet, geompy.ShapeType["FACE"], True)

  # for num, f in enumerate(air_outlet_faces): # add faces to study
  #   counter += 1
  #   geompy.addToStudyInFather(air_outlet, f, 'face_{}'.format(counter) ) 

  #################################

  # isOk, res1, res2 = geompy.FastIntersect(lens_outer, air_outlet)

  # print('OK {} res1 {} res2 {}'.format(isOk, res1, res2))

  #################################
  pml_top = geompy.MakeTranslation( pml_bottom, \
                                    # 0, y_translation_shift, \
                                    0, 0, \
                                    # pml_bottom_height + air_bottom_height + waveLenght + 3*air_bottom_height )
                                    probing_distance )

  # geompy.addToStudy( pml_top, 'pml_top' )
  #################################








  #################################


  # GENERATE RANDOM ARRAY of 8 BRICKS and ADD to FATHER
  row = 0
  column = 0

  bricks = list()

  translation = ( 0, 0, 0 )
  translation_shift = ( 0, y_translation_shift , 0 )
  
  bricks_faces = []

  for m in range( 0, lens_grid_n ):
  # for n in range( 0, lens_grid_n ):

    # brickID = random.randint(1, 15)                                   # generate random brickID
    brickID = [*range(1,9),*range(10,16)][random.randint(0, 13)]        # generate random brickID, but exclude index 9, shape is buggy 

    Sketch_1 = parameterize_2D_inner_shape( waveLenght, \
                                            data['length'][brickID - 1] * waveLenght, \
                                            data['distance'][brickID - 1] * waveLenght )

    # geompy.addToStudy( Sketch_1, 'Sketch' )
    rotation = [(x, 90)]
    # translation = ( waveLenght/40, waveLenght/40 + waveLenght/2, 6.861)
    translation_x = waveLenght/40 + column * ( waveLenght/40 + waveLenght/2 )     
    translation_y = waveLenght/40 + row * (waveLenght/40 + waveLenght/2 )     
    
    translation = ( translation_shift[0] + translation_x, translation_shift[1] + translation_y + waveLenght/2 , 6.861 )
    
    brick_inner = sketch_to_volume( geompy, Sketch_1, waveLenght/2, rotation, translation)
    
    
    # print(*bricks_faces, sep='\n')
    bricks.append(brick_inner)
    brick_faces = geompy.ExtractShapes(brick_inner, geompy.ShapeType["FACE"], True)  # generates 1946 faces instead of 54
    bricks_faces.append(brick_faces) 

    for num, f in enumerate(brick_faces): # add faces to study
      counter += 1
      name = 'face_{}'.format(counter)
      f.SetName(name)
      # print('face_{}: {}'.format(name, f.GetEntry()))
      bricks_faces.append(f) 


    # print('Brick {} - type:{} #faces:{}'.format(m+1, brickID, len(bricks_faces[m]) ) )
    # print( *brick_faces, sep='\n')
    # column += 1
  # column = 0
    row += 1


  #################################



  print('#brickFaces: {}'.format( len(bricks_faces) ) )
  # print(bricks)
  # print(*bricks_faces, sep='\n')

  #################################
  # Fuse the Lens_Outer (box that will contain all the brics ) with all the bricks  
  lens_fused = geompy.MakeFuseList( [ lens_outer ] + bricks, True, True)
  # geompy.addToStudy( lens_fused, 'Fused' )


  group_fused = geompy.CreateGroup(lens_fused, geompy.ShapeType["FACE"])

  lens_fused_faces = geompy.SubShapeAll(group_fused, geompy.ShapeType["FACE"])

  # geompy.addToStudyInFather(lens_fused, f, 'face_{}'.format(counter) ) 

  # lens_fused_faces = geompy.ExtractShapes(lens_fused, geompy.ShapeType["FACE"], True)

  # for num, f in enumerate(lens_fused_faces): # add faces to study
  #   counter += 1
  #   geompy.addToStudyInFather(lens_fused, f, 'face_{}'.format(counter) ) 

  #################################

  # Cut the bricks positives from the above fused result 
  lens = geompy.MakeCutList( lens_fused, bricks, True)
  geompy.addToStudy( lens, 'Lens' )

  lens_faces = []
  lens_faces =  geompy.ExtractShapes(lens, geompy.ShapeType["FACE"], True) # generates 1946 faces instead of 54
  print( '#lensFaces: {}'.format(len(lens_faces)) ) 
  # print( *lens_faces, sep='\n') 

  
  # Fuse all the air sections, the bricks positives with air sections at the inlet and outlet 
  air = geompy.MakeFuseList( [ air_inlet, air_outlet ] + bricks, True, True)
  geompy.addToStudy( air, 'Air' )



  Structure = geompy.MakePartition([pml_bottom, pml_top, lens, air], [], [], [], geompy.ShapeType["SOLID"], 0, [], 0)
  geompy.addToStudy( Structure, 'Structure' )
  
  # solids = [Solid_1, Solid_2, Solid_3, Solid_4] = geompy.ExtractShapes(Structure, geompy.ShapeType["SOLID"], True)
  solids = [Solid_1, Solid_2, Solid_3, Solid_4] = geompy.SubShapeAllSortedCentres(Structure, geompy.ShapeType["SOLID"])
  # solids = geompy.SubShapeAllSortedCentres(Structure, geompy.ShapeType["SOLID"])

  print( geompy.PointCoordinates(geompy.MakeCDG(Solid_1))[2] )
  print( geompy.PointCoordinates(geompy.MakeCDG(Solid_2))[2] )
  print( geompy.PointCoordinates(geompy.MakeCDG(Solid_3))[2] )
  print( geompy.PointCoordinates(geompy.MakeCDG(Solid_4))[2] )

  solids_sorted = sorted(solids, key=lambda s: geompy.PointCoordinates(geompy.MakeCDG(s))[2] )
  # solids.sort( key=lambda s: geompy.PointCoordinates(geompy.MakeCDG(s))[2] )

  [solid_pml_inlet, solid_lens, solid_air, solid_pml_outlet] = solids_sorted

  print( "sorted" )

  print( geompy.PointCoordinates(geompy.MakeCDG(solid_pml_inlet))[2] )
  print( geompy.PointCoordinates(geompy.MakeCDG(solid_lens))[2] )
  print( geompy.PointCoordinates(geompy.MakeCDG(solid_air))[2] )
  print( geompy.PointCoordinates(geompy.MakeCDG(solid_pml_outlet))[2] )


  #################################

  faces = geompy.ExtractShapes(Structure, geompy.ShapeType["FACE"], True)
  # print( '#faces: {}'.format(len(faces)) )
  # # print( *faces, sep='\n' )
  # print( type(faces[0]) )
  # print( dir(faces[0]) )
  # print( faces[1].GetType() )
  # print( faces[1].GetName() )
  # print( faces[1].GetParameters() )
  # print( geompy.GetNormal(faces[0]) ) # 28 - SUBSHAPE
  # print( geompy.ShapeIdToType(faces[0].GetType()) ) # 28 - SUBSHAPE
  # print( geompy.BasicProperties( faces[0].GetType() ) ) # 28 - SUBSHAPE

  print( 'len faces: ', len(faces))

  pml_inlet_air_shared_faces = geompy.GetSharedShapesMulti( [ solid_pml_inlet, solid_air ],  geompy.ShapeType['FACE'], False) 
  pml_outlet_air_shared_faces = geompy.GetSharedShapesMulti( [ solid_pml_outlet, solid_air ],  geompy.ShapeType['FACE'], False) 
  lens_solid_air_shared_faces = geompy.GetSharedShapesMulti( [ solid_lens, solid_air ],  geompy.ShapeType['FACE'], False) 

  Group_Air_Lens_Faces = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"])
  geompy.UnionList(Group_Air_Lens_Faces, lens_solid_air_shared_faces )
  geompy.addToStudyInFather( Structure, Group_Air_Lens_Faces, 'Group_Air_Lens_Faces' )

  Group_PML_In_Faces = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"])
  geompy.UnionList(Group_PML_In_Faces, pml_inlet_air_shared_faces )
  geompy.addToStudyInFather( Structure, Group_PML_In_Faces, 'Group_PML_In_Faces' )
  
  Group_PML_Out_Faces = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"])
  geompy.UnionList(Group_PML_Out_Faces, pml_outlet_air_shared_faces )
  geompy.addToStudyInFather( Structure, Group_PML_Out_Faces, 'Group_PML_Out_Faces' )

  air_subshapes = geompy.SubShapeAll(solid_air, geompy.ShapeType["FACE"])
  # air_subshapes = geompy.SubShapeAll(air, geompy.ShapeType["FACE"])
  # air_subshapes = geompy.SubShapeAllSortedCentres(air, geompy.ShapeType["FACE"])
  # air_subshapes = geompy.GetSharedShapesMulti(air, geompy.ShapeType['FACE'], False)
  # print(air_subshapes)

  Group_Air_Faces = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"])
  geompy.UnionList( Group_Air_Faces, air_subshapes )
  geompy.addToStudyInFather(Structure, Group_Air_Faces, 'Group_Air_Faces' )
  
  # group_faces_air_cut = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"])
  group_faces_air_cut = geompy.CutGroups(Group_Air_Faces, Group_Air_Lens_Faces )
  group_faces_air_cut = geompy.CutListOfGroups( [Group_Air_Faces],
                                                [ Group_Air_Lens_Faces, Group_PML_In_Faces, Group_PML_Out_Faces] )

  geompy.addToStudyInFather(Structure, group_faces_air_cut, 'group_faces_air' )


  # Group_Lens = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"])
  # # geompy.UnionIDs(Group_Lens, [1015, 1018, 1025, 1075, 1080, 72, 82, 89, 1128, 1131, 1134, 1137, 1140, 1143, 1146, 1149, 1152, 1155, 1158, 1161, 1164, 1167, 1170, 1173, 166, 1176, 1179, 171, 1182, 1185, 1188, 1191, 1194, 1197, 1200, 1203, 1206, 1208, 1211, 1214, 1217, 1220, 1223, 1226, 1229, 1232, 1235, 1238, 1240, 1243, 1246, 1249, 1252, 246, 1255, 248, 1258, 1261, 255, 1264, 1267, 1270, 1272, 1275, 1278, 1281, 1284, 1287, 1290, 1293, 1296, 1299, 1302, 1304, 1307, 1310, 1313, 305, 1316, 1319, 1322, 1325, 1328, 1331, 1334, 1336, 1339, 1342, 1345, 1348, 1351, 1354, 1357, 1360, 1363, 355, 1366, 358, 1368, 1371, 1374, 365, 1377, 1380, 1383, 1386, 1389, 1392, 1395, 1398, 1400, 1403, 1406, 1409, 1412, 1415, 1418, 1421, 1424, 415, 1427, 1430, 1432, 1435, 1438, 1441, 1444, 1447, 1450, 1453, 1456, 1459, 1462, 1464, 1467, 1470, 1473, 465, 1476, 468, 1479, 1482, 475, 1485, 1488, 1491, 1494, 1496, 1499, 1502, 1505, 1508, 1511, 1514, 1517, 1520, 1523, 1526, 1528, 1531, 1534, 525, 1537, 1540, 1543, 1546, 1549, 1552, 1555, 1558, 1560, 1563, 1566, 1569, 1572, 1575, 1578, 1581, 1584, 575, 1587, 578, 1590, 1592, 585, 1595, 1598, 1601, 1604, 1607, 1610, 1613, 1616, 1619, 1622, 1624, 1627, 1630, 1633, 1636, 1639, 1642, 635, 1645, 1648, 1651, 1654, 1656, 1659, 1662, 1665, 1668, 1671, 1674, 1677, 1680, 1683, 1686, 685, 688, 695, 745, 795, 798, 805, 855, 905, 908, 915, 965])
  # geompy.UnionIDs(Group_Lens, SubFaceListIDs)

  # # geompy.UnionList(Group_Lens, [lens_faces] )
  # # geompy.UnionList(Group_Lens, [SubFaceList] )

  # geompy.addToStudyInFather( Structure, Group_Lens, 'Group_Lens' ) 

  # def flatten(t):
  #   return [item for sublist in t for item in sublist]
    
  # SubFaceListAir_1 = geompy.SubShapeAll(air, geompy.ShapeType["FACE"])
  # SubFaceListAir_2 = geompy.SubShapeAll(air, geompy.ShapeType["VERTEX"])
  # SubFaceListAir_3 = geompy.ExtractShapes(air, geompy.ShapeType["FACE"], True)
  # SubFaceListAirIDs = [ geompy.GetSubShapeID(air, sf) for sf in flatten([SubFaceListAir_1,SubFaceListAir_2, SubFaceListAir_3 ]) ] 
  

  # Group_Air_Faces = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"])

  # SubFaceListAir = geompy.ExtractShapes(air, geompy.ShapeType["FACE"], True)
  # SubFaceListAir = geompy.SubShapeAll(air, geompy.ShapeType["FACE"])
  # SubFaceListAir = geompy.SubShapeAll(air, geompy.ShapeType["VERTEX"])

  # SubFaceListAirIDs = [ geompy.GetSubShapeID(air, sf) for sf in SubFaceListAir ] 

  #################################
  # Autogroups in geometry for meshing
  Auto_group_for_top_bottom_walls = geompy.CreateGroup( Structure, geompy.ShapeType["FACE"]) # set top & bottom walls
  # geompy.UnionList(Auto_group_for_top_bottom_walls, [ faces[24], faces[30] ] ) # [Face_25, Face_30] ) 
  # geompy.UnionList(Auto_group_for_top_bottom_walls, [ section_intersect_PML_in_air_in, section_intersect_PML_out_air_out ] )

  Auto_group_for_brick_faces = geompy.CreateGroup( Structure, geompy.ShapeType["FACE"]) # set brick faces
  # geompy.UnionList( Auto_group_for_brick_faces, [ bricks_faces ] )
  # geompy.UnionList( Auto_group_for_brick_faces, [Faces[5], Face_7, Face_8, Face_9, Face_10, Face_11, Face_12, Face_13, Face_14, \
  #                                               Face_20, Face_21, Face_22, Face_23, Face_24, \
  #                                               Face_31, Face_32, Face_33, Face_34, Face_35, \
  #                                               Face_28, Face_31, Face_38, \
  #                                               Face_41, Face_42, Face_43, Face_44, Face_45, Face_46, Face_47, Face_48, Face_49, \
  #                                               Face_3, Face_17, Face_38, Face_52, Face_27, Face_28])

  # Auto_group_for_front = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set front walls
  # geompy.UnionList(Auto_group_for_front, [Face_15, Face_16, Face_18, Face_19])
  
  # Auto_group_for_air = geompy.CreateGroup(air, geompy.ShapeType["FACE"]) # set front walls
  # Auto_group_for_air = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set front walls

  # Auto_group_for_left = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set left walls/
  # geompy.UnionList(Auto_group_for_left, [Face_1, Face_2, Face_4, Face_5])
  # geompy.UnionList(Auto_group_for_left, [faces[27], faces[29], faces[31], faces[32] ]) # Face_31 is brick wall

  # Auto_group_for_back = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set back walls
  # geompy.UnionList(Auto_group_for_back, [Face_36, Face_37, Face_39, Face_40])

  # Auto_group_for_right = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"]) # set right walls
  # geompy.UnionList(Auto_group_for_right, [Face_50, Face_51, Face_53, Face_54])

  #################################
  # Add autogroups to study
  # geompy.addToStudyInFather(Structure, Auto_group_for_right, 'Auto_group_for_right')
  # geompy.addToStudyInFather(Structure, Auto_group_for_air, 'Auto_group_for_air')
  # geompy.addToStudyInFather(Structure, Auto_group_for_left, 'Auto_group_for_left')
  # geompy.addToStudyInFather(Structure, Auto_group_for_back, 'Auto_group_for_back')
  # geompy.addTo  'Auto_group_for_top_bottom_walls')
  # geompy.addToStudyInFather(Structure, Auto_group_for_lens_faces, 'Auto_group_for_lens_faces')
  # geompy.addToStudyInFather(Structure, Auto_group_for_front, 'Auto_group_for_front')

  #################################

  # Add to solids & faces to study
  



  # geompy.addToStudy(Structure, 'Structure')
  










  # for num, f in enumerate(faces): # add faces to study
  #   geompy.addToStudyInFather(Structure, f, 'face_{}'.format(num + 1) )  
 
  # # Add solids to study
  # for num, s in enumerate(solids): 
  #   geompy.addToStudyInFather(Structure, s, 'solid_{}'.format(num + 1))  

  # geompy.addToStudy(Sketch_1, 'Sketch') 



  # group_faces_air_subshape = geompy.SubShapeAll(Lens, geompy.ShapeType["FACE"])


  # geompy.addToStudyInFather( Structure, pml_inlet, 'pml_inlet' )
  # geompy.addToStudyInFather( Structure, air, 'air' )
  # geompy.addToStudyInFather( Structure, lens, 'lens' )
  # geompy.addToStudyInFather( Structure, pml_outlet, 'pml_outlet' )


  # geompy.addToStudyInFather( Structure, group_faces_air, 'group_faces_air' )
  # geompy.addToStudyInFather( Structure, group_faces_pml_in, 'group_faces_pml_in' )
  # geompy.addToStudyInFather( Structure, group_face_air_pml_in, 'group_face_air_pml_in' )
  # geompy.addToStudyInFather( Structure, group_faces_pml_out, 'group_faces_pml_out' )




  end = time.time()
  print("Geometry computation time: {:.2f} sec".format(end - start))
  
  # start = time.time()
  smesh = smeshBuilder.New()
  

  Structure_1 = smesh.Mesh(Structure)
  
  NETGEN_1D_2D_3D = Structure_1.Tetrahedron( algo=smeshBuilder.NETGEN_1D2D3D )
  NETGEN_3D_Parameters_1 = NETGEN_1D_2D_3D.Parameters()
  # NETGEN_3D_Parameters_1.SetMaxSize( 3.1461 )
  # NETGEN_3D_Parameters_1.SetMinSize( 0.0844741 )
  NETGEN_3D_Parameters_1.SetMaxSize( 1 )
  NETGEN_3D_Parameters_1.SetMinSize( 0.1 )
  NETGEN_3D_Parameters_1.SetSecondOrder( 1 )
  NETGEN_3D_Parameters_1.SetOptimize( 1 )
  NETGEN_3D_Parameters_1.SetFineness( 4 )
  NETGEN_3D_Parameters_1.SetChordalError( -1 )
  NETGEN_3D_Parameters_1.SetChordalErrorEnabled( 0 )
  NETGEN_3D_Parameters_1.SetUseSurfaceCurvature( 1 )
  NETGEN_3D_Parameters_1.SetFuseEdges( 1 )
  NETGEN_3D_Parameters_1.SetQuadAllowed( 0 )
  NETGEN_3D_Parameters_1.SetCheckChartBoundary( 72 )



  # 2. Create a 3D mesh on the box with GMSH_3D algorithm
  # Structure_1 = smesh.Mesh(Structure, "GMSH_3D_Mesh")
  # # create a Gmsh 3D algorithm for solids
  # Algo_3D = Structure_1.Tetrahedron(algo=smeshBuilder.GMSH)
  # # define hypotheses
  # Param_3D = Algo_3D.Parameters()
  # # define algorithms
  # Param_3D.Set2DAlgo( 0 )
  # Param_3D.SetIs2d( 0 )
  # # Set Algorithm3D - 10: HXT
  # Param_3D.Set3DAlgo( 10 )
  # Param_3D.SetMinSize( 0.1 )
  # Param_3D.SetMaxSize( 0.8 )
  # Param_3D.SetOrder( 2 )
  # Set output format - 2: unv
  # Param_3D.SetFormat( 2 )
  # compute the meshes
  # Mesh_3D.Compute()

# Geometry computation time: 4.64 sec
# Mesh computation time: 265.22 sec


  # # Add meshing groups
  pml_bottom_mesh = Structure_1.GroupOnGeom(solid_pml_inlet,'pml_inlet',SMESH.VOLUME)
  brick_mesh = Structure_1.GroupOnGeom(solid_lens,'lens',SMESH.VOLUME)
  air_mesh = Structure_1.GroupOnGeom(solid_air,'air',SMESH.VOLUME)
  pml_top_mesh = Structure_1.GroupOnGeom(solid_pml_outlet,'pml_outlet',SMESH.VOLUME)
  


  # air_faces_mesh = Structure_1.GroupOnGeom(Group_Air_Faces,'air_faces', SMESH.FACE)
  brick_faces_mesh = Structure_1.GroupOnGeom(Group_Air_Lens_Faces,'lens', SMESH.FACE)
  inlet_face_mesh = Structure_1.GroupOnGeom(Group_PML_In_Faces,'inlet', SMESH.FACE)
  outlet_faces_mesh = Structure_1.GroupOnGeom(Group_PML_Out_Faces,'outlet', SMESH.FACE)
  faces_air_cut_mesh = Structure_1.GroupOnGeom( group_faces_air_cut, 'air', SMESH.FACE)


  isDone = Structure_1.Compute()  

  # print(Structure_1.GetGroups())

  # Add groups in mesh.unv
  # [pml_bottom, pml_top, brick, air, top_bottom_walls, inlet, outlet, lens_faces, brick_left, brick_front, brick_back, brick_right, left, front, back, right ] = Structure_1.GetGroups()
  # [pml_bottom, pml_top, air, lens_faces ] = Structure_1.GetGroups()

  # Mesh computation time
  end = time.time()
  print("Mesh computation time: {:.2f} sec".format(end - start))

  # # Rename bodies for Elmer
  # # smesh.SetName(solids_mesh[0], 'pml_bot')
  # # smesh.SetName(solids_mesh[1], 'brick')
  # # smesh.SetName(solids_mesh[2], 'air')
  # # smesh.SetName(solids_mesh[3], 'pml_top')
  # # Rename faces for Elmer
  # # smesh.SetName(left, 'left')
  # # smesh.SetName(back, 'back')
  # # smesh.SetName(front, 'front')2222
  # # smesh.SetName(NETGEN_2D3D_1.GetAlgorithm(), 'NETGEN_2D3D_1')
  # # smesh.SetName(right, 'right')
  # # smesh.SetName(brick_front, 'brick_front')
  # # smesh.SetName(brick_back, 'brick_back')
  # # smesh.SetName(brick_right, 'brick_right')
  # # smesh.SetName(NETGEN_Parameters, 'NETGEN_Parameters')
  # # smesh.SetName(Structure_1.GetMesh(), 'Structure')
  # # smesh.SetName(brick_left, 'brick_left')
  # # smesh.SetName(brick_faces, 'brick_faces')
  # # smesh.SetName(outlet, 'outlet')
  # # smesh.SetName(inlet, 'inlet')
  # # smesh.SetName(top_bottom_walls, 'top_bottom_walls')
  # start = time.time()
  # return Structure_1

process_geometry(data)

# Structure = process_geometry(data)

# # First export mesh in .unv format
# try:
#   Structure.ExportUNV( r'C:/Users/Francisco/Documents/acoustic-brick/Lens.unv' )
#   pass
# except:
#   print('ExportUNV() failed. Invalid file name?')

# # Export mesh to Elmer
# export_elmer('Lens')

# end = time.time()
# print("Salome to Elmer computation time: {:.2f} sec".format(end - start))

# if salome.sg.hasDesktop():
#   salome.sg.updateObjBrowser()
