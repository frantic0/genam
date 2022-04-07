import sys
import salome
import numpy as np
# import pandas as pd
import time, os
import random


salome.salome_init()
import salome_notebook
notebook = salome_notebook.NoteBook()

sys.path.insert(0, r'C:/Users/francisco/Documents/dev/pipeline/ammgdop')

from utility_functions import * 

from parametric_shape import * 

###
### Salome GEOM and SMESH components
###

import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS

import SMESH, SALOMEDS
from salome.smesh import smeshBuilder
from salome.GMSHPlugin import GMSHPluginBuilder


class Lens:
  
  def __init__(self,
               unit_cells_config,
               mesh_config,
               m = 4,
               n = 4,
               probing_distance = 100,
               nearfield_limit = 8.661,
               wavelenght = 8.661
               ):

    self.unit_cells_config = unit_cells_config
    self.mesh_config = mesh_config
    self.wavelenght = wavelenght

    self.m = m
    self.n = n 

    self.nearfield_limit = nearfield_limit
    self.probing_distance = probing_distance

    self.geompy = geomBuilder.New()
    self.smesh = smeshBuilder.New()

    self.geometry = {}
    self.mesh = {}

    self.start = 0
    self.end = 0

    pass


  def process_geometry(self):

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
  
    air_bottom_height = 4.288
  
    y_translation_shift = -(waveLenght/40 + 4*(waveLenght/2 + waveLenght/40))
  
    counter = 0



    pml_bottom = geompy.MakeTranslation( geompy.MakeBoxDXDYDZ( lens_side, lens_side, pml_bottom_height),
                                          0, y_translation_shift,
                                          0 )
    # geompy.addToStudy( pml_bottom, 'pml_bottom' )

    air_inlet = geompy.MakeTranslation( geompy.MakeBoxDXDYDZ( lens_side, lens_side, air_bottom_height),
                                        0, y_translation_shift,
                                        pml_bottom_height )
    # geompy.addToStudy( air_inlet, 'air_inlet' )
    
    lens_outer = geompy.MakeTranslation(  geompy.MakeBoxDXDYDZ( lens_side, lens_side, waveLenght ),
                                          0, y_translation_shift,
                                          pml_bottom_height + air_bottom_height )
    # geompy.addToStudy( lens_outer, 'lens_outer' )

    air_height = probing_distance - (pml_bottom_height + air_bottom_height + waveLenght)

    air_outlet = geompy.MakeTranslation( geompy.MakeBoxDXDYDZ( lens_side, lens_side, air_height ),
                                          0, y_translation_shift, 
                                          pml_bottom_height + air_bottom_height + waveLenght )

    pml_top = geompy.MakeTranslation( pml_bottom,
                                      0, 0,
                                      probing_distance )
    # geompy.addToStudy( pml_top, 'pml_top' )

    row = 0
    column = 0


    translation = ( 0, 0, 0 )
    translation_shift = ( 0, y_translation_shift , 0 )
    

    #################################
    
    # GENERATE RANDOM ARRAY of 8 BRICKS and ADD to FATHER
    
    bricks = list()
    bricks_faces = []

    for m in range( 0, lens_grid_n ):
      for n in range( 0, lens_grid_n ):

        # brickID = random.randint(1, 15)                                   # generate random brickID
        brickID = [*range(1,9),*range(10,16)][random.randint(0, 13)]        # generate random brickID, but exclude index 9, shape is buggy 

        Sketch_1 = parameterize_2D_inner_shape( waveLenght,
                                                self.unit_cells_config['length'][brickID-1] * waveLenght,
                                                self.unit_cells_config['distance'][brickID-1] * waveLenght )

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
        column += 1
      row += 1
      column = 0




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
    # geompy.addToStudy( lens, 'Lens' )

    lens_faces = []
    lens_faces =  geompy.ExtractShapes(lens, geompy.ShapeType["FACE"], True) # generates 1946 faces instead of 54
    print( '#lensFaces: {}'.format(len(lens_faces)) ) 
    # print( *lens_faces, sep='\n') 

    
    # Fuse all the air sections, the bricks positives with air sections at the inlet and outlet 
    air = geompy.MakeFuseList( [ air_inlet, air_outlet ] + bricks, True, True)
    # geompy.addToStudy( air, 'Air' )

    Structure = geompy.MakePartition([pml_bottom, pml_top, lens, air], [], [], [], geompy.ShapeType["SOLID"], 0, [], 0)
    geompy.addToStudy( Structure, 'Structure' )
    
    # solids = [Solid_1, Solid_2, Solid_3, Solid_4] = geompy.SubShapeAllSortedCentres(Structure, geompy.ShapeType["SOLID"])
    solids = geompy.SubShapeAllSortedCentres(Structure, geompy.ShapeType["SOLID"])
    # print(solids)
    # TODO: Extract unit test from this code
    # print( geompy.PointCoordinates(geompy.MakeCDG(Solid_1))[2] )
    # print( geompy.PointCoordinates(geompy.MakeCDG(Solid_2))[2] )
    # print( geompy.PointCoordinates(geompy.MakeCDG(Solid_3))[2] )
    # print( geompy.PointCoordinates(geompy.MakeCDG(Solid_4))[2] )

    # sort by Z coordinate of the center of mass of the solid, which an attribute of the solid object  
    solids_sorted = sorted(solids, key=lambda s: geompy.PointCoordinates(geompy.MakeCDG(s))[2] )
    # solids.sort( key=lambda s: geompy.PointCoordinates(geompy.MakeCDG(s))[2] ) # alternative methods, similar performance

    # expand ordered list and assign to objects for futher processing
    [ solid_pml_inlet, solid_lens, solid_air, solid_pml_outlet ] = solids_sorted

    # print( "sorted" ) # DEBUG
    # print( geompy.PointCoordinates(geompy.MakeCDG(solid_pml_inlet))[2] )
    # print( geompy.PointCoordinates(geompy.MakeCDG(solid_lens))[2] )
    # print( geompy.PointCoordinates(geompy.MakeCDG(solid_air))[2] )
    # print( geompy.PointCoordinates(geompy.MakeCDG(solid_pml_outlet))[2] )

    #################################

    faces = geompy.ExtractShapes(Structure, geompy.ShapeType["FACE"], True)
  
    shared_faces_pml_inlet_air = geompy.GetSharedShapesMulti( [ solid_pml_inlet, solid_air ],  geompy.ShapeType['FACE'], False) 
    shared_faces_pml_outlet_air = geompy.GetSharedShapesMulti( [ solid_pml_outlet, solid_air ],  geompy.ShapeType['FACE'], False) 
    shared_faces_lens_solid_air = geompy.GetSharedShapesMulti( [ solid_lens, solid_air ],  geompy.ShapeType['FACE'], False) 

    # face_top = geompy.GetOppositeFace( shared_faces_pml_inlet_air[0], solid_pml_inlet )	
    # geompy.addToStudy(face_top, 'face_top')
    # face_bottom = geompy.GetOppositeFace( shared_faces_pml_outlet_air[0], solid_pml_outlet )	
    # geompy.addToStudy(face_bottom, 'face_bottom')


    group_faces_air_lens = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"])
    geompy.UnionList(group_faces_air_lens, shared_faces_lens_solid_air )
    geompy.addToStudyInFather( Structure, group_faces_air_lens, 'group_faces_air_lens' )


    group_faces_inlet = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"])
    geompy.UnionList(group_faces_inlet, shared_faces_pml_inlet_air )
    geompy.addToStudyInFather( Structure, group_faces_inlet, 'group_faces_inlet' )
    
    group_faces_outlet = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"])
    geompy.UnionList(group_faces_outlet, shared_faces_pml_outlet_air )
    geompy.addToStudyInFather( Structure, group_faces_outlet, 'group_faces_outlet' )

    subshapes_air = geompy.SubShapeAll(solid_air, geompy.ShapeType["FACE"])
    # air_subshapes = geompy.SubShapeAll(air, geompy.ShapeType["FACE"])
    # air_subshapes = geompy.SubShapeAllSortedCentres(air, geompy.ShapeType["FACE"])
    # air_subshapes = geompy.GetSharedShapesMulti(air, geompy.ShapeType['FACE'], False)
    # print(air_subshapes)

    group_faces_air = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"])
    geompy.UnionList( group_faces_air, subshapes_air )
    geompy.addToStudyInFather(Structure, group_faces_air, 'group_faces_air' )
      
    # group_faces_air_cut = geompy.CutGroups( group_faces_air, group_faces_air_lens )
    group_faces_air_cut = geompy.CutListOfGroups( [ group_faces_air ],
                                                  [ group_faces_air_lens, group_faces_inlet, group_faces_outlet] )

    geompy.addToStudyInFather(Structure, group_faces_air_cut, 'group_faces_air_cut' )

    subshapes_lens = geompy.SubShapeAll( solid_lens, geompy.ShapeType["FACE"] )
    group_faces_lens = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"])
    geompy.UnionList( group_faces_lens, subshapes_lens )
    
    group_faces_lens_cut = geompy.CutListOfGroups(  [ group_faces_lens ], [ group_faces_air_lens ] )
    geompy.addToStudyInFather(Structure, group_faces_lens_cut, 'group_faces_lens_cut' )



    ##############################################

    # Group Air and PML faces for BCs and PBCs
    # which require specific points for extracting the faces

    subshapes_pml_inlet = geompy.SubShapeAll(solid_pml_inlet, geompy.ShapeType["FACE"])
    subshapes_pml_outlet = geompy.SubShapeAll(solid_pml_outlet, geompy.ShapeType["FACE"])

    group_faces_pml_inlet = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"])
    geompy.UnionList( group_faces_pml_inlet, subshapes_pml_inlet )
    geompy.addToStudyInFather(Structure, group_faces_pml_inlet, 'group_faces_pml_inlet' )

    group_faces_pml_outlet = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"])
    geompy.UnionList( group_faces_pml_outlet, subshapes_pml_outlet )
    geompy.addToStudyInFather(Structure, group_faces_pml_outlet, 'group_faces_pml_outlet' )



    face_pml_inlet_left = geompy.GetFaceNearPoint(group_faces_pml_inlet,    geompy.MakeVertex(0, -0.108263, 1.2865))
    face_air_left_1 = geompy.GetFaceNearPoint(group_faces_air,              geompy.MakeVertex(0, -0.108263, 57.761))
    face_air_left_2 = geompy.GetFaceNearPoint(group_faces_air,              geompy.MakeVertex(0, -0.108263, 4.717))
    face_pml_outlet_left = geompy.GetFaceNearPoint(group_faces_pml_outlet,  geompy.MakeVertex(0, -0.108263, 101.2865))

    group_faces_air_left = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"])
    geompy.UnionList( group_faces_air_left, [face_air_left_1, face_air_left_2, face_pml_inlet_left, face_pml_outlet_left] )
    geompy.addToStudyInFather(Structure, group_faces_air_left, 'group_faces_left' )

    face_pml_inlet_right = geompy.GetFaceNearPoint(group_faces_pml_inlet,   geompy.MakeVertex(36.592725, -0.108263, 1.2865))
    face_air_right_1 = geompy.GetFaceNearPoint(group_faces_air,             geompy.MakeVertex(36.592725, -0.108263, 57.761))
    face_air_right_2 = geompy.GetFaceNearPoint(group_faces_air,             geompy.MakeVertex(36.592725, -0.108263, 4.717))
    face_pml_outlet_right = geompy.GetFaceNearPoint(group_faces_pml_outlet, geompy.MakeVertex(36.592725, -0.108263, 101.2865))

    group_faces_air_right = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"])
    geompy.UnionList( group_faces_air_right, [face_air_right_1, face_air_right_2, face_pml_inlet_right, face_pml_outlet_right] )
    geompy.addToStudyInFather(Structure, group_faces_air_right, 'group_faces_right' )

    face_pml_inlet_back = geompy.GetFaceNearPoint(group_faces_pml_inlet,    geompy.MakeVertex(2.381775, 18.404625, 1.2865))
    face_air_back_1 = geompy.GetFaceNearPoint(group_faces_air,              geompy.MakeVertex(2.381775, 18.404625, 57.761))
    face_air_back_2 = geompy.GetFaceNearPoint(group_faces_air,              geompy.MakeVertex(2.381775, 18.404625, 4.717))
    face_pml_outlet_back = geompy.GetFaceNearPoint(group_faces_pml_outlet,  geompy.MakeVertex(2.381775, 18.404625, 101.2865))

    group_faces_air_back = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"])
    geompy.UnionList( group_faces_air_back, [face_air_back_1, face_air_back_2, face_pml_inlet_back, face_pml_outlet_back] )
    geompy.addToStudyInFather(Structure, group_faces_air_back, 'group_faces_back' )

    face_pml_inlet_front = geompy.GetFaceNearPoint(group_faces_pml_inlet,   geompy.MakeVertex(2.381775, -18.404625, 1.2865))
    face_air_front_1 = geompy.GetFaceNearPoint(group_faces_air,             geompy.MakeVertex(2.381775, -18.404625, 57.761))
    face_air_front_2 = geompy.GetFaceNearPoint(group_faces_air,             geompy.MakeVertex(2.381775, -18.404625, 4.717))
    face_pml_outlet_front = geompy.GetFaceNearPoint(group_faces_pml_outlet, geompy.MakeVertex(2.381775, -18.404625, 101.2865))

    group_faces_air_front = geompy.CreateGroup(Structure, geompy.ShapeType["FACE"])
    geompy.UnionList( group_faces_air_front, [face_air_front_1, face_air_front_2, face_pml_inlet_front, face_pml_outlet_front] )
    geompy.addToStudyInFather(Structure, group_faces_air_front, 'group_faces_front' )

    return time.time()
  
  # def flatten(t):
  #   return [item for sublist in t for item in sublist]


  def process_mesh(self): 

    # start = time.time()
    

    Structure_1 = self.smesh.Mesh(self.geometry)
    
    NETGEN_1D_2D_3D = Structure_1.Tetrahedron( algo=smeshBuilder.NETGEN_1D2D3D )
    NETGEN_3D_Parameters_1 = NETGEN_1D_2D_3D.Parameters()
    NETGEN_3D_Parameters_1.SetMaxSize( self.mesh_config[0] )
    NETGEN_3D_Parameters_1.SetMinSize( self.mesh_config[1] )
    NETGEN_3D_Parameters_1.SetSecondOrder( self.mesh_config[2] )
    NETGEN_3D_Parameters_1.SetOptimize( 1 )
    NETGEN_3D_Parameters_1.SetFineness( self.mesh_config[3] )
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

    ####################################################################

    # # Add meshing groups
    
    pml_bottom_mesh = Structure_1.GroupOnGeom(solid_pml_inlet,'pml_inlet',SMESH.VOLUME)
    brick_mesh = Structure_1.GroupOnGeom(solid_lens,'lens',SMESH.VOLUME)
    air_mesh = Structure_1.GroupOnGeom(solid_air,'air',SMESH.VOLUME)
    pml_top_mesh = Structure_1.GroupOnGeom(solid_pml_outlet,'pml_outlet',SMESH.VOLUME)
    
    # air_faces_mesh = Structure_1.GroupOnGeom(Group_Air_Faces,'air_faces', SMESH.FACE)
    inlet_face_mesh = Structure_1.GroupOnGeom(group_faces_inlet,'inlet', SMESH.FACE)
    outlet_faces_mesh = Structure_1.GroupOnGeom(group_faces_outlet,'outlet', SMESH.FACE)
    # faces_air_cut_mesh = Structure_1.GroupOnGeom( group_faces_air_cut, 'air', SMESH.FACE)
    brick_faces_mesh = Structure_1.GroupOnGeom(group_faces_air_lens, 'lens', SMESH.FACE)
    faces_lens_cut_mesh = Structure_1.GroupOnGeom( group_faces_lens_cut, 'lens_shell', SMESH.FACE)

    mesh_air_front = Structure_1.GroupOnGeom( group_faces_air_front, 'front', SMESH.FACE)
    mesh_air_back = Structure_1.GroupOnGeom( group_faces_air_back, 'back', SMESH.FACE)
    mesh_air_right = Structure_1.GroupOnGeom( group_faces_air_right, 'right', SMESH.FACE)
    mesh_air_left = Structure_1.GroupOnGeom( group_faces_air_left, 'left', SMESH.FACE)




    isDone = Structure_1.Compute()  

    # print(Structure_1.GetGroups())

    # Add groups in mesh.unv
    # [pml_bottom, pml_top, brick, air, top_bottom_walls, inlet, outlet, lens_faces, brick_left, brick_front, brick_back, brick_right, left, front, back, right ] = Structure_1.GetGroups()
    # [pml_bottom, pml_top, air, lens_faces ] = Structure_1.GetGroups()

    # Mesh computation time
    return time.time()

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


flap_configs = { 
  'length':   [.062, .092, .112, .132, .152, .162, .171, .191, .221, .241, .251, .271, .281, .301, .321],
  'distance': [.216, .212, .207, .189, .161, .166, .171, .134, .257, .234, .230, .207, .203, .175, .152],  
  'radius':   [.062, .092, .1,   .1,   .1,   .1,   .1,   .1,   .1,   .1,   .1,   .1,   .1,   .1,   .1] 
}

unit_cell_selector = lambda i: (
  flap_configs['length'][i],
  flap_configs['distance'][i],
  flap_configs['radius'][i]
)

lens_configurator = lambda m: [
  [ unit_cell_selector() ]

]



mesh_configs = {
  'maxSize':      [5,     3,    3,    3,    3,    1   ],
  'minSize':      [1,     0.8,  0.5,  0.3,  0.08,  0.1],
  'secondOrder':  [True,  True, True, True, True, True],
  'fineness':     [4,     4,    4,    4,    4,    4   ] 
}

mesh_config_selector = lambda i:  ( 
  mesh_configs['maxSize'][i],
  mesh_configs['minSize'][i],
  mesh_configs['secondOrder'][i],
  mesh_configs['fineness'][i],
) 


lens =  Lens( ,
              mesh_config_selector(3),
              8,
              8,
              
            )

lens.configure()

start = time.time()

end = lens.process_geometry()

print("Geometry computation time: {:.2f} sec".format(end - start))

start = time.time()

end = lens.process_mesh()

print("Mesh computation time: {:.2f} sec".format(end - start))




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
