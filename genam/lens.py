from utility_functions import * 
from parametric_shape import * 

###
### Salome GEOM and SMESH components
###

import salome
import GEOM
from salome.geom import geomBuilder
import SALOMEDS

import SMESH, SALOMEDS
from salome.smesh import smeshBuilder
from salome.GMSHPlugin import GMSHPluginBuilder


class Lens:
  
  def __init__( 
                self,
                unit_cells_config,
                mesh_config,
                name = 'lens',
                probing_distance = 100,
                nearfield_limit = 8.661,
                wavelenght = 8.661
              ):

    self.wavelenght = wavelenght

    self.unit_cells_config = unit_cells_config
    self.mesh_config = mesh_config
    self.name = name

    # TODO: Make sure this is consistent with the input matrix expectations
    self.m = len(unit_cells_config)
    self.n = len(unit_cells_config[0])

    self.nearfield_limit = nearfield_limit
    self.probing_distance = probing_distance

    self.geompy = geomBuilder.New()
    self.geometry = {}
    self.solids = []
    self.groups = {}

    self.smesh = smeshBuilder.New()
    self.mesh = {}

    self.start = 0
    self.end = 0

    pass


  # TODO: add try catch exceptions
  def process_geometry(self):

    origin = geompy.MakeVertex(0, 0, 0)

    x = geompy.MakeVectorDXDYDZ(1, 0, 0)
    y = geompy.MakeVectorDXDYDZ(0, 1, 0)
    z = geompy.MakeVectorDXDYDZ(0, 0, 1)

    geompy.addToStudy( x, 'x' )
    geompy.addToStudy( y, 'y' )
    geompy.addToStudy( z, 'z' )

    probing_distance = 100


    # TODO: we want to make 'm' and 'n' consistent with the input grid size. 
    # Check self.m and self.n initialisation
    lens_side_x = self.wavelenght/40 + self.n * ( self.wavelenght/2 + self.wavelenght/40 )
    lens_side_y = self.wavelenght/40 + self.m * ( self.wavelenght/2 + self.wavelenght/40 )

    boxSide = self.wavelenght/2 + 2 * self.wavelenght/40
    
    pml_bottom_height = 2.573
  
    air_bottom_height = 4.288
  
    # y_translation_shift = - ( self.wavelenght/40 + self.m * ( self.wavelenght/2 + self.wavelenght/40 ))
    y_translation_shift =  -( self.wavelenght/40 + self.m * ( self.wavelenght/2 + self.wavelenght/40 )) / 2 
    x_translation_shift =  -( self.wavelenght/40 + self.n * ( self.wavelenght/2 + self.wavelenght/40 )) / 2
  
    counter = 0

    pml_bottom = geompy.MakeTranslation( geompy.MakeBoxDXDYDZ( lens_side_x, lens_side_y, pml_bottom_height),
                                          x_translation_shift, 
                                          y_translation_shift,
                                          0 )
    # geompy.addToStudy( pml_bottom, 'pml_bottom' )

    air_inlet = geompy.MakeTranslation( geompy.MakeBoxDXDYDZ( lens_side_x, lens_side_y, air_bottom_height),
                                        x_translation_shift, 
                                        y_translation_shift,
                                        pml_bottom_height )
    # geompy.addToStudy( air_inlet, 'air_inlet' )
    
    lens_outer = geompy.MakeTranslation(  geompy.MakeBoxDXDYDZ( lens_side_x, lens_side_y, self.wavelenght ),
                                          x_translation_shift, 
                                          y_translation_shift,
                                          pml_bottom_height + air_bottom_height )
    # geompy.addToStudy( lens_outer, 'lens_outer' )

    air_height = probing_distance - (pml_bottom_height + air_bottom_height + self.wavelenght)

    air_outlet = geompy.MakeTranslation( geompy.MakeBoxDXDYDZ( lens_side_x, lens_side_y, air_height ),
                                          x_translation_shift, 
                                          y_translation_shift, 
                                          pml_bottom_height + air_bottom_height + self.wavelenght )

    pml_top = geompy.MakeTranslation( pml_bottom,
                                      0, 0,
                                      probing_distance )
    # geompy.addToStudy( pml_top, 'pml_top' )

    row = 0
    column = 0

    translation = ( 0, 0, 0 )

    translation_shift = ( x_translation_shift, y_translation_shift , 0 )
    

    #################################
    
    # GENERATE RANDOM ARRAY of 8 BRICKS and ADD to FATHER
    
    bricks = list()
    # bricks_faces = []

    for m in range( 0, self.m ):
      for n in range( 0, self.n ):

        # brickID = random.randint(1, 15)                                   # generate random brickID
        # brickID = [*range(1,9),*range(10,16)][random.randint(0, 13)]        # generate random brickID, but exclude index 9, shape is buggy 

        # Sketch_1 = parameterize_2D_inner_shape( waveLenght,
        #                                         self.unit_cells_config['length'][brickID-1] * waveLenght,
        #                                         self.unit_cells_config['distance'][brickID-1] * waveLenght )

        brick_inner = []

        translation_x = self.wavelenght/40 + column * ( self.wavelenght/2 + self.wavelenght/40 )     
        translation_y = self.wavelenght/40 + row    * ( self.wavelenght/2 + self.wavelenght/40 )     
  
        if self.unit_cells_config[m][n][0] == 0:

          # brick_inner = geompy.MakeTranslation(
          #                   geompy.MakeBoxDXDYDZ( boxSide - 2 * self.wavelenght/40, 
          #                                         boxSide - 2 * self.wavelenght/40, 
          #                                         self.wavelenght ),
          #                   self.wavelenght/40, 
          #                   self.wavelenght/40,
          #                   pml_bottom_height + air_bottom_height )    

          brick_inner = geompy.MakeTranslation(
                            geompy.MakeBoxDXDYDZ( boxSide - 2 * self.wavelenght/40, 
                                                  boxSide - 2 * self.wavelenght/40, 
                                                  self.wavelenght ),
                            translation_shift[0] + translation_x,
                            translation_shift[1] + translation_y,
                            6.861 )    

        else: 

          Sketch_1 = parameterize_2D_inner_shape( self.wavelenght,
                                                  self.unit_cells_config[m][n][1] * self.wavelenght,
                                                  self.unit_cells_config[m][n][2] * self.wavelenght )

          # geompy.addToStudy( Sketch_1, 'Sketch' )
          rotation = [(x, 90)]
          
          # translation = ( waveLenght/40, waveLenght/40 + waveLenght/2, 6.861)
          translation_x = self.wavelenght/40 + column * ( self.wavelenght/40 + self.wavelenght/2 )     
          translation_y = self.wavelenght/40 + row * (self.wavelenght/40 + self.wavelenght/2 )     
          
          # TODO : replace hardcoded constant but ratio
          translation = ( translation_shift[0] + translation_x,
                          translation_shift[1] + translation_y + self.wavelenght/2, 
                          6.861 )
          
          try:
            brick_inner = sketch_to_volume( geompy, Sketch_1, self.wavelenght /2, rotation, translation)
          except: 
            print("{} {} {}".format(Sketch_1, m, n))

        bricks.append(brick_inner)

        column += 1
      row += 1
      column = 0


    #################################

    # Fuse the Lens_Outer (box that will contain all the brics ) with all the bricks  

    lens_fused = geompy.MakeFuseList( [ lens_outer ] + bricks, True, True)
    # geompy.addToStudy( lens_fused, 'Fused' )

    group_fused = geompy.CreateGroup( lens_fused, geompy.ShapeType["FACE"] )

    lens_fused_faces = geompy.SubShapeAll( group_fused, geompy.ShapeType["FACE"] )

    #################################

    # Cut the bricks positives from the above fused result 
    lens = geompy.MakeCutList( lens_fused, bricks, True)
    # geompy.addToStudy( lens, 'Lens' )

    lens_faces = []
    lens_faces =  geompy.ExtractShapes(lens, geompy.ShapeType["FACE"], True) # generates 1946 faces instead of 54
    # print( '#lensFaces: {}'.format(len(lens_faces)) ) 
    # print( *lens_faces, sep='\n') 

    
    # Fuse all the air sections, the bricks positives with air sections at the inlet and outlet 
    air = geompy.MakeFuseList( [ air_inlet, air_outlet ] + bricks, True, True)
    # geompy.addToStudy( air, 'Air' )

    self.geometry = geompy.MakePartition([pml_bottom, pml_top, lens, air], [], [], [], geompy.ShapeType["SOLID"], 0, [], 0)
    geompy.addToStudy( self.geometry, 'Structure' )
    
    # solids = [Solid_1, Solid_2, Solid_3, Solid_4] = geompy.SubShapeAllSortedCentres(Structure, geompy.ShapeType["SOLID"])
    solids = geompy.SubShapeAllSortedCentres( self.geometry, geompy.ShapeType["SOLID"] )
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

    self.groups['solid_pml_inlet'] = solid_pml_inlet
    self.groups['solid_lens'] = solid_lens
    self.groups['solid_air'] = solid_air
    self.groups['solid_pml_outlet'] = solid_pml_outlet

    # print( "sorted" ) # DEBUG
    # print( geompy.PointCoordinates(geompy.MakeCDG(solid_pml_inlet))[2] )
    # print( geompy.PointCoordinates(geompy.MakeCDG(solid_lens))[2] )
    # print( geompy.PointCoordinates(geompy.MakeCDG(solid_air))[2] )
    # print( geompy.PointCoordinates(geompy.MakeCDG(solid_pml_outlet))[2] )

    #################################
  
    shared_faces_pml_inlet_air = geompy.GetSharedShapesMulti( [ solid_pml_inlet, solid_air ],  geompy.ShapeType['FACE'], False) 
    shared_faces_pml_outlet_air = geompy.GetSharedShapesMulti( [ solid_pml_outlet, solid_air ],  geompy.ShapeType['FACE'], False) 
    shared_faces_lens_solid_air = geompy.GetSharedShapesMulti( [ solid_lens, solid_air ],  geompy.ShapeType['FACE'], False) 

    group_faces_air_lens = geompy.CreateGroup( self.geometry, geompy.ShapeType["FACE"] )
    geompy.UnionList(group_faces_air_lens, shared_faces_lens_solid_air )
    self.groups['group_faces_air_lens'] = group_faces_air_lens
    geompy.addToStudyInFather( self.geometry, group_faces_air_lens, 'group_faces_air_lens' )

    group_faces_inlet = geompy.CreateGroup( self.geometry, geompy.ShapeType["FACE"])
    geompy.UnionList(group_faces_inlet, shared_faces_pml_inlet_air )
    self.groups['group_faces_inlet'] = group_faces_inlet
    geompy.addToStudyInFather( self.geometry, group_faces_inlet, 'group_faces_inlet' )
    
    group_faces_outlet = geompy.CreateGroup( self.geometry, geompy.ShapeType["FACE"])
    geompy.UnionList(group_faces_outlet, shared_faces_pml_outlet_air )
    self.groups['group_faces_outlet'] = group_faces_outlet
    geompy.addToStudyInFather( self.geometry, group_faces_outlet, 'group_faces_outlet' )

    # face_pml_inlet_right = geompy.GetFaceNearPoint(group_faces_pml_inlet,   geompy.MakeVertex(36.592725, -0.108263, 1.2865))

    subshapes_air = geompy.SubShapeAll(solid_air, geompy.ShapeType["FACE"])
    # air_subshapes = geompy.SubShapeAll(air, geompy.ShapeType["FACE"])
    # air_subshapes = geompy.SubShapeAllSortedCentres(air, geompy.ShapeType["FACE"])
    # air_subshapes = geompy.GetSharedShapesMulti(air, geompy.ShapeType['FACE'], False)
    # print(air_subshapes)

    group_faces_air = geompy.CreateGroup( self.geometry, geompy.ShapeType["FACE"])
    geompy.UnionList( group_faces_air, subshapes_air )
    self.groups['group_faces_air'] = group_faces_air
    geompy.addToStudyInFather( self.geometry, group_faces_air, 'group_faces_air' )
      
    # group_faces_air_cut = geompy.CutGroups( group_faces_air, group_faces_air_lens )
    group_faces_air_cut = geompy.CutListOfGroups( [ group_faces_air ],
                                                  [ group_faces_air_lens, group_faces_inlet, group_faces_outlet] )

    self.groups['group_faces_air_cut'] = group_faces_air_cut
    geompy.addToStudyInFather( self.geometry, group_faces_air_cut, 'group_faces_air_cut' )

    subshapes_lens = geompy.SubShapeAll( solid_lens, geompy.ShapeType["FACE"] )
    group_faces_lens = geompy.CreateGroup( self.geometry, geompy.ShapeType["FACE"])
    geompy.UnionList( group_faces_lens, subshapes_lens )
    
    group_faces_lens_cut = geompy.CutListOfGroups(  [ group_faces_lens ], [ group_faces_air_lens ] )
    self.groups['group_faces_lens_cut'] = group_faces_lens_cut
    geompy.addToStudyInFather( self.geometry, group_faces_lens_cut, 'group_faces_lens_cut' )

    ##############################################

    # Group Air and PML faces for BCs and PBCs
    # which require specific points for extracting the faces

    subshapes_pml_inlet = geompy.SubShapeAll(solid_pml_inlet, geompy.ShapeType["FACE"])
    subshapes_pml_outlet = geompy.SubShapeAll(solid_pml_outlet, geompy.ShapeType["FACE"])

    group_faces_pml_inlet = geompy.CreateGroup( self.geometry, geompy.ShapeType["FACE"])
    geompy.UnionList( group_faces_pml_inlet, subshapes_pml_inlet )
    self.groups['group_faces_pml_inlet'] = group_faces_pml_inlet
    geompy.addToStudyInFather( self.geometry, group_faces_pml_inlet, 'group_faces_pml_inlet' )

    group_faces_pml_outlet = geompy.CreateGroup( self.geometry, geompy.ShapeType["FACE"])
    geompy.UnionList( group_faces_pml_outlet, subshapes_pml_outlet )
    self.groups['group_faces_pml_outlet'] = group_faces_pml_outlet
    geompy.addToStudyInFather( self.geometry, group_faces_pml_outlet, 'group_faces_pml_outlet' )

    face_pml_inlet_left = geompy.GetFaceNearPoint(group_faces_pml_inlet,    geompy.MakeVertex( -lens_side_x/2, 0, 1.2865))
    face_air_left_1 = geompy.GetFaceNearPoint(group_faces_air,              geompy.MakeVertex( -lens_side_x/2, 0, 57.761))
    face_air_left_2 = geompy.GetFaceNearPoint(group_faces_air,              geompy.MakeVertex( -lens_side_x/2, 0, 4.717))
    face_pml_outlet_left = geompy.GetFaceNearPoint(group_faces_pml_outlet,  geompy.MakeVertex( -lens_side_x/2, 0, 101.2865))

    group_faces_air_left = geompy.CreateGroup( self.geometry, geompy.ShapeType["FACE"])
    geompy.UnionList( group_faces_air_left, [face_air_left_1, face_air_left_2, face_pml_inlet_left, face_pml_outlet_left] )
    self.groups['group_faces_left'] = group_faces_air_left
    geompy.addToStudyInFather( self.geometry, group_faces_air_left, 'group_faces_left' )

    face_pml_inlet_right = geompy.GetFaceNearPoint(group_faces_pml_inlet,   geompy.MakeVertex( lens_side_x/2, 0, 1.2865))
    face_air_right_1 = geompy.GetFaceNearPoint(group_faces_air,             geompy.MakeVertex( lens_side_x/2, 0, 57.761))
    face_air_right_2 = geompy.GetFaceNearPoint(group_faces_air,             geompy.MakeVertex( lens_side_x/2, 0, 4.717))
    face_pml_outlet_right = geompy.GetFaceNearPoint(group_faces_pml_outlet, geompy.MakeVertex( lens_side_x/2, 0, 101.2865))

    group_faces_air_right = geompy.CreateGroup( self.geometry, geompy.ShapeType["FACE"])
    geompy.UnionList( group_faces_air_right, [face_air_right_1, face_air_right_2, face_pml_inlet_right, face_pml_outlet_right] )
    self.groups['group_faces_right'] = group_faces_air_right 
    geompy.addToStudyInFather( self.geometry, group_faces_air_right, 'group_faces_right' )

    face_pml_inlet_back = geompy.GetFaceNearPoint(group_faces_pml_inlet,    geompy.MakeVertex(0, lens_side_y/2, 1.2865))
    face_air_back_1 = geompy.GetFaceNearPoint(group_faces_air,              geompy.MakeVertex(0, lens_side_y/2, 57.761))
    face_air_back_2 = geompy.GetFaceNearPoint(group_faces_air,              geompy.MakeVertex(0, lens_side_y/2, 4.717))
    face_pml_outlet_back = geompy.GetFaceNearPoint(group_faces_pml_outlet,  geompy.MakeVertex(0, lens_side_y/2, 101.2865))

    group_faces_air_back = geompy.CreateGroup( self.geometry, geompy.ShapeType["FACE"])
    geompy.UnionList( group_faces_air_back, [face_air_back_1, face_air_back_2, face_pml_inlet_back, face_pml_outlet_back] )
    self.groups['group_faces_back'] = group_faces_air_back
    geompy.addToStudyInFather( self.geometry, group_faces_air_back, 'group_faces_back' )

    face_pml_inlet_front = geompy.GetFaceNearPoint(group_faces_pml_inlet,   geompy.MakeVertex(0, -lens_side_y/2, 1.2865))
    face_air_front_1 = geompy.GetFaceNearPoint(group_faces_air,             geompy.MakeVertex(0, -lens_side_y/2, 57.761))
    face_air_front_2 = geompy.GetFaceNearPoint(group_faces_air,             geompy.MakeVertex(0, -lens_side_y/2, 4.717))
    face_pml_outlet_front = geompy.GetFaceNearPoint(group_faces_pml_outlet, geompy.MakeVertex(0, -lens_side_y/2, 101.2865))

    group_faces_air_front = geompy.CreateGroup( self.geometry, geompy.ShapeType["FACE"])
    geompy.UnionList( group_faces_air_front, [face_air_front_1, face_air_front_2, face_pml_inlet_front, face_pml_outlet_front] )
    self.groups['group_faces_front'] = group_faces_air_front
    geompy.addToStudyInFather( self.geometry, group_faces_air_front, 'group_faces_front' )

    
    # Group top and bottom walls faces

    group_faces_top_bottom_walls = geompy.CreateGroup( self.geometry, geompy.ShapeType["FACE"])

    shared_faces_pml_inlet = geompy.CreateGroup( self.geometry, geompy.ShapeType["FACE"])
    geompy.UnionList( shared_faces_pml_inlet, 
                      [ group_faces_inlet, face_pml_inlet_left, face_pml_inlet_back, face_pml_inlet_right, face_pml_inlet_front ] )    
    shared_faces_pml_outlet = geompy.CreateGroup( self.geometry, geompy.ShapeType["FACE"])
    geompy.UnionList( shared_faces_pml_outlet, 
                      [ group_faces_outlet, face_pml_outlet_left, face_pml_outlet_back, face_pml_outlet_right, face_pml_outlet_front ] )
    
    face_pml_outlet_outer = geompy.CutGroups( group_faces_pml_outlet, shared_faces_pml_outlet )
    face_pml_inlet_outer = geompy.CutGroups( group_faces_pml_inlet, shared_faces_pml_inlet )

    geompy.UnionList( group_faces_top_bottom_walls, [ face_pml_inlet_outer, face_pml_outlet_outer ] )
    self.groups['group_faces_top_bottom_walls'] = group_faces_top_bottom_walls
    geompy.addToStudyInFather( self.geometry, group_faces_top_bottom_walls, 'group_faces_top_bottom_walls' )
 
    return
  
  # def flatten(t):
  #   return [item for sublist in t for item in sublist]

  
  def __set_mesh_strategy__(  self, 
                              algo = smeshBuilder.NETGEN_1D2D3D ) :

    if algo == smeshBuilder.NETGEN_1D2D3D :

      NETGEN_1D_2D_3D = self.mesh.Tetrahedron( algo = smeshBuilder.NETGEN_1D2D3D )
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

    else : 

      # create a Gmsh 3D algorithm for solids
      Algo_3D = self.mesh.Tetrahedron( algo = smeshBuilder.GMSH )
      # define hypotheses
      Param_3D = Algo_3D.Parameters()
      # define algorithms
      Param_3D.Set2DAlgo( 0 )
      Param_3D.SetIs2d( 0 )
      # Set Algorithm3D - 10: HXT
      Param_3D.Set3DAlgo( 10 )
      Param_3D.SetMinSize( 0.1 )
      Param_3D.SetMaxSize( 0.8 )
      Param_3D.SetOrder( 2 )
      # Set output format - 2: unv
      Param_3D.SetFormat( 2 )

  # TODO : validate inputs & add exceptions
  def process_mesh( self,
                    algo = smeshBuilder.NETGEN_1D2D3D ) :
                    
    self.mesh = self.smesh.Mesh(self.geometry)
    
    self.__set_mesh_strategy__( algo )
    
    # Add meshing groups
    
    pml_bottom_mesh = self.mesh.GroupOnGeom( self.groups['solid_pml_inlet'], 'pml_inlet', SMESH.VOLUME)
    brick_mesh = self.mesh.GroupOnGeom( self.groups['solid_lens'], 'lens', SMESH.VOLUME)
    air_mesh = self.mesh.GroupOnGeom( self.groups['solid_air'], 'air', SMESH.VOLUME)
    pml_top_mesh = self.mesh.GroupOnGeom( self.groups['solid_pml_outlet'], 'pml_outlet', SMESH.VOLUME)
    
    # air_faces_mesh = Structure_1.GroupOnGeom(Group_Air_Faces,'air_faces', SMESH.FACE)
    inlet_face_mesh = self.mesh.GroupOnGeom( self.groups['group_faces_inlet'],'inlet', SMESH.FACE)
    outlet_faces_mesh = self.mesh.GroupOnGeom( self.groups['group_faces_outlet'],'outlet', SMESH.FACE)
    # faces_air_cut_mesh = Structure_1.GroupOnGeom( group_faces_air_cut, 'air', SMESH.FACE)
    brick_faces_mesh = self.mesh.GroupOnGeom( self.groups['group_faces_air_lens'], 'lens_air', SMESH.FACE)
    faces_lens_cut_mesh = self.mesh.GroupOnGeom( self.groups['group_faces_lens_cut'], 'lens_shell', SMESH.FACE)
    
    mesh_top_bottom = self.mesh.GroupOnGeom( self.groups['group_faces_top_bottom_walls'], 'top_bottom', SMESH.FACE)


    mesh_air_front = self.mesh.GroupOnGeom( self.groups['group_faces_front'], 'front', SMESH.FACE)
    mesh_air_back = self.mesh.GroupOnGeom( self.groups['group_faces_back'], 'back', SMESH.FACE)
    mesh_air_right = self.mesh.GroupOnGeom( self.groups['group_faces_right'], 'right', SMESH.FACE)
    mesh_air_left = self.mesh.GroupOnGeom( self.groups['group_faces_left'], 'left', SMESH.FACE)

    isDone = self.mesh.Compute()  

  def export_mesh( self, path ) : 
    """

      Input


      Output

        .unv to *.mesh (Elmer w)  
    
    """
    path_dir = os.path.dirname(path)
    if not os.path.exists( path_dir ):
      try:
        os.makedirs( path_dir )
      except:
        print('ExportUNV() failed. Directory does not exist and could not create it')

    # os.chdir(path)

    try:
      # self.mesh.ExportUNV( str( Path(path).joinpath( self.name + '.unv' ) ) ) # ExportUNV requires string as input type, not path!
      self.mesh.ExportUNV( path ) # ExportUNV requires string as input type, not path!
    except:
      print('ExportUNV() failed. Invalid file name?')

