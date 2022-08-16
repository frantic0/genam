from utility_functions import * 
# from brick import * 
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
  
  def __init__( self,
                unit_cells_config,
                mesh_config,
                name = 'lens',
                inlet_offset = 0.001,
                outlet_offset = 0.001,
                wavelength = 8.661,
                set_PML = True,
                source_config = None,
                set_hemisphere = False
              ):

    self.wavelength = wavelength

    self.unit_cells_config = unit_cells_config
    self.mesh_config = mesh_config
    self.name = name

    # TODO: Make sure this is consistent with the input matrix expectations
    self.m = len(unit_cells_config)
    self.n = len(unit_cells_config[0])

    self.inlet_offset = inlet_offset
    self.outlet_offset = outlet_offset
    self.set_PML = set_PML
    self.set_hemisphere = set_hemisphere

    self.geompy = geomBuilder.New()
    self.geometry = {}
    self.solids = []
    self.groups = {}

    self.smesh = smeshBuilder.New()
    self.mesh = {}

    self.start = 0
    self.end = 0
    self.pml_bottom_height = 2.573

    self.source_config = source_config

    pass




  def __create_hemisphere__(  self, radius = 17.322, translationDZ = 16.2 ):
    '''
      create hemisphere for sound diffusion
    '''    
    sphere_inner = geompy.MakeSphereR(radius)
    sphere_outer = geompy.MakeSphereR(radius + self.pml_bottom_height)
    box_cut = geompy.MakeBoxDXDYDZ(40, 40, 20)
    self.geompy.TranslateDXDYDZ(box_cut, -20, -20, -20)
    partition_spheres = geompy.MakePartition([ sphere_inner, sphere_outer ], [], [], [], geompy.ShapeType["SOLID"], 0, [], 0)
    cut_spheres = geompy.MakeCutList(partition_spheres, [box_cut], True)
    hemisphere = geompy.TranslateDXDYDZ(cut_spheres, 0, 0, translationDZ)
    
    # geompy.addToStudy( sphere_inner, 'sphere_inner' )
    # geompy.addToStudy( sphere_outer, 'sphere_outer' )
    # geompy.addToStudy( box_cut, 'box_cut' )
    # geompy.addToStudy( partition_spheres, 'partition_spheres' )
    # geompy.addToStudy( cut_spheres, 'cut_spheres' )
    
    return hemisphere




  # TODO: add try catch exceptions
  def process_geometry(self):

    origin = geompy.MakeVertex(0, 0, 0)

    x = geompy.MakeVectorDXDYDZ(1, 0, 0)
    y = geompy.MakeVectorDXDYDZ(0, 1, 0)
    z = geompy.MakeVectorDXDYDZ(0, 0, 1)

    geompy.addToStudy( x, 'x' )
    geompy.addToStudy( y, 'y' )
    geompy.addToStudy( z, 'z' )

    # TODO: we want to make 'm' and 'n' consistent with the input grid size. 
    # Check self.m and self.n initialisation 
    lens_side_x = self.wavelength/40 + self.n * ( self.wavelength/2 + self.wavelength/40 )
    lens_side_y = self.wavelength/40 + self.m * ( self.wavelength/2 + self.wavelength/40 )

    boxSide = self.wavelength/2 + 2 * self.wavelength/40
    
    # geompy.addToStudy( pml_bottom, 'pml_bottom' )

    # translation = ( 0, 0, 0 )

    x_translation_shift =  -( self.wavelength/40 + self.n * ( self.wavelength/2 + self.wavelength/40 )) / 2 
    y_translation_shift =  -( self.wavelength/40 + self.m * ( self.wavelength/2 + self.wavelength/40 )) / 2
   
    translation_lens_center_origin = ( 
                    -( self.wavelength/40 + self.n * ( self.wavelength/2 + self.wavelength/40 )) / 2,
                    -( self.wavelength/40 + self.m * ( self.wavelength/2 + self.wavelength/40 )) / 2,
                    0
                  )


    pml_bottom = geompy.MakeTranslation( geompy.MakeBoxDXDYDZ( lens_side_x, lens_side_y, self.pml_bottom_height),
                                          x_translation_shift, 
                                          y_translation_shift,
                                          0 )
    #################################
    

    lens_outer = geompy.MakeTranslation(  geompy.MakeBoxDXDYDZ( lens_side_x, lens_side_y, self.wavelength ),
                                          x_translation_shift, 
                                          y_translation_shift,
                                          self.pml_bottom_height + self.inlet_offset )
    # geompy.addToStudy( lens_outer, 'lens_outer' )

    #################################
    

    air_inlet = {}

    if self.inlet_offset > 0:
      air_inlet = geompy.MakeTranslation( geompy.MakeBoxDXDYDZ( lens_side_x, lens_side_y, self.inlet_offset),
                                          x_translation_shift, 
                                          y_translation_shift,
                                          self.pml_bottom_height )
      # geompy.addToStudy( air_inlet, 'air_inlet' )
    

   

    #################################
    
    # GENERATE RANDOM ARRAY of 8 BRICKS and ADD to FATHER
   
    unit_cells = list()

    row = 0
    column = 0


#    for m in range( 0, self.m ):                    # Y row index
#      for n in range( 0, self.n ):                  # X column index
    for m in range( self.m-1, -1, -1 ):                    # Y row index
      for n in range( self.n-1, -1, -1 ):                  # X column index

        unit_cell_negative = {}
        # translation = ( 0, 0, 0 )

        # y_translation_shift =  -( self.wavelength/40 + self.m * ( self.wavelength/2 + self.wavelength/40 )) / 2 
        # x_translation_shift =  -( self.wavelength/40 + self.n * ( self.wavelength/2 + self.wavelength/40 )) / 2
      
        # translation_shift = ( x_translation_shift, y_translation_shift , 0 )

        if self.unit_cells_config[m][n][0] < 0:       # if negative number, do not add unit cell negative for lens cut
          pass

        elif self.unit_cells_config[m][n][0] == 0:      # if zero, add empty unit cell for lens cut

          # translation = (
          #   translation_lens_center_origin[0] + self.wavelength/40 + column * ( self.wavelength/2 + self.wavelength/40 ),
          #   translation_lens_center_origin[1] + self.wavelength/40 +    row * ( self.wavelength/2 + self.wavelength/40 ),
          #   0 )

          translation = (
            translation_lens_center_origin[0] + self.wavelength/40 + column * ( self.wavelength/2 + self.wavelength/40 ),
            translation_lens_center_origin[1] + self.wavelength/40 +    row * ( self.wavelength/2 + self.wavelength/40 ),
            0 )     
    
          unit_cell_negative = geompy.MakeTranslation(
                                  geompy.MakeBoxDXDYDZ( boxSide - 2 * self.wavelength/40, 
                                                        boxSide - 2 * self.wavelength/40, 
                                                        self.wavelength ),
                                  translation[0],
                                  translation[1],
                                  self.pml_bottom_height + self.inlet_offset )    

          unit_cells.append(unit_cell_negative)

        else:                                         # if greater than zero, place brick ID as corresponding cell for lens cut

          # unit_cell_negative = Labyrinthine()
          # unit_cell_negative.configure( waveLength = self.wavelength,
          #                               barLength  = self.unit_cells_config[m][n][1] * self.wavelength, 
          #                               barSpacing = self.unit_cells_config[m][n][2] * self.wavelength, 
          #                               radius = None )
                                               
                                              
          # sketch = parameterize_2D_inner_shape( self.wavelength,
          #                                         self.unit_cells_config[m][n][1] * self.wavelength,
          #                                         self.unit_cells_config[m][n][2] * self.wavelength )
          
          sketch = parameterize_2D_inner_shape_no_radii(  self.wavelength,
                                                          self.unit_cells_config[m][n][1] * self.wavelength,
                                                          self.unit_cells_config[m][n][2] * self.wavelength )
          # geompy.addToStudy( Sketch_1, 'Sketch' )
          
          rotation = [(x, 90)]

          translation = (
            translation_lens_center_origin[0] + self.wavelength/40 + column * ( self.wavelength/2 + self.wavelength/40 ),
            translation_lens_center_origin[1] + self.wavelength/40 +    row * ( self.wavelength/2 + self.wavelength/40 ) + self.wavelength/2,
            self.pml_bottom_height + self.inlet_offset 
          )
            
          # translation = ( translation_shift[0] + translation_x,
          #                 translation_shift[1] + translation_y + self.wavelength/2, 
          
          try:
            unit_cell_negative = sketch_to_volume(  geompy, 
                                                    sketch, 
                                                    self.wavelength /2, 
                                                    rotation, 
                                                    translation )
          except: 
            print("{} {} {}".format(sketch, m, n))

          unit_cells.append(unit_cell_negative)

        column += 1
      column = 0
      row += 1


    #################################

    # Fuse the Lens_Outer (box that will contain all the brics ) with all the bricks  

    lens_fused = geompy.MakeFuseList( [ lens_outer ] + unit_cells, True, True)
    # geompy.addToStudy( lens_fused, 'Fused' )

    group_fused = geompy.CreateGroup( lens_fused, geompy.ShapeType["FACE"] )

    lens_fused_faces = geompy.SubShapeAll( group_fused, geompy.ShapeType["FACE"] )

    #################################

    # Cut the bricks positives from the above fused result 
    lens = geompy.MakeCutList( lens_fused, unit_cells, True)
    # geompy.addToStudy( lens, 'Lens' )

    lens_faces = []
    lens_faces =  geompy.ExtractShapes(lens, geompy.ShapeType["FACE"], True) # generates 1946 faces instead of 54
    # print( '#lensFaces: {}'.format(len(lens_faces)) ) 
    # print( *lens_faces, sep='\n') 

    hemisphere = pml_top = air_outlet = {}

    if self.outlet_offset > 0 and self.set_hemisphere == True:
      
      hemisphere = self.__create_hemisphere__(  radius = self.outlet_offset,
                                                translationDZ = self.pml_bottom_height + self.inlet_offset + self.wavelength )
      
      air = geompy.MakeFuseList( [ air_inlet, hemisphere ] + unit_cells, True, True)

      self.geometry = geompy.MakePartition([pml_bottom, lens, air], [], [], [], geompy.ShapeType["SOLID"], 0, [], 0)
      # geompy.addToStudy( hemisphere, 'hemisphere' )
      # geompy.addToStudy( air, 'air' )

    elif self.set_hemisphere == False:

      air_outlet = geompy.MakeTranslation(  geompy.MakeBoxDXDYDZ( lens_side_x, lens_side_y, self.outlet_offset ),
                                            x_translation_shift, 
                                            y_translation_shift, 
                                            self.pml_bottom_height + self.inlet_offset + self.wavelength )

      pml_top = geompy.MakeTranslation( pml_bottom,
                                        0, 0,
                                        self.pml_bottom_height + self.inlet_offset + self.wavelength + self.outlet_offset )

    # Fuse all the air sections, the bricks positives with air sections at the inlet and outlet 
      if air_inlet != {} and air_outlet != {}:
        air = geompy.MakeFuseList( [ air_inlet, air_outlet ] + unit_cells, True, True)
      elif air_outlet != {}:
        air = geompy.MakeFuseList( [ air_outlet ] + unit_cells, True, True)

      self.geometry = geompy.MakePartition([pml_bottom, pml_top, lens, air], [], [], [], geompy.ShapeType["SOLID"], 0, [], 0)
    
    elif air_inlet:
      air = geompy.MakeFuseList( [ air_inlet ] + unit_cells, True, True)
      self.geometry = geompy.MakePartition([pml_bottom, lens, air], [], [], [], geompy.ShapeType["SOLID"], 0, [], 0)
    else: 
      air = geompy.MakeFuseList( [ ] + unit_cells, True, True)
      self.geometry = geompy.MakePartition([pml_bottom, lens, air], [], [], [], geompy.ShapeType["SOLID"], 0, [], 0)
      # geompy.addToStudy( air, 'Air' )
    geompy.addToStudy( self.geometry, self.name )



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
    print(solids_sorted)

    if hemisphere != {}:
      [ solid_pml_inlet, solid_lens, solid_air ] = solids_sorted
    else:
      [ solid_pml_inlet, solid_lens, solid_air, solid_pml_outlet ] = solids_sorted

    self.groups['solid_pml_inlet'] = solid_pml_inlet
    self.groups['solid_lens'] = solid_lens
    self.groups['solid_air'] = solid_air

    # self.groups['solid_pml_outlet'] = solid_pml_outlet

    # print( "sorted" ) # DEBUG
    # print( geompy.PointCoordinates(geompy.MakeCDG(solid_pml_inlet))[2] )
    # print( geompy.PointCoordinates(geompy.MakeCDG(solid_lens))[2] )
    # print( geompy.PointCoordinates(geompy.MakeCDG(solid_air))[2] )
    # print( geompy.PointCoordinates(geompy.MakeCDG(solid_pml_outlet))[2] )

    #################################
  
    shared_faces_pml_inlet_air = geompy.GetSharedShapesMulti( [ solid_pml_inlet, solid_air ],  geompy.ShapeType['FACE'], False) 
    # shared_faces_pml_outlet_air = geompy.GetSharedShapesMulti( [ solid_pml_outlet, solid_air ],  geompy.ShapeType['FACE'], False) 
    shared_faces_lens_solid_air = geompy.GetSharedShapesMulti( [ solid_lens, solid_air ],  geompy.ShapeType['FACE'], False) 

    group_faces_air_lens = geompy.CreateGroup( self.geometry, geompy.ShapeType["FACE"] )
    geompy.UnionList(group_faces_air_lens, shared_faces_lens_solid_air )
    self.groups['group_faces_air_lens'] = group_faces_air_lens
    geompy.addToStudyInFather( self.geometry, group_faces_air_lens, 'group_faces_air_lens' )

    group_faces_inlet = geompy.CreateGroup( self.geometry, geompy.ShapeType["FACE"])
    geompy.UnionList(group_faces_inlet, shared_faces_pml_inlet_air )
    self.groups['group_faces_inlet'] = group_faces_inlet
    geompy.addToStudyInFather( self.geometry, group_faces_inlet, 'group_faces_inlet' )
    
    # group_faces_outlet = geompy.CreateGroup( self.geometry, geompy.ShapeType["FACE"])
    # geompy.UnionList(group_faces_outlet, shared_faces_pml_outlet_air )
    # self.groups['group_faces_outlet'] = group_faces_outlet
    # geompy.addToStudyInFather( self.geometry, group_faces_outlet, 'group_faces_outlet' )




    # # face_pml_inlet_right = geompy.GetFaceNearPoint(group_faces_pml_inlet,   geompy.MakeVertex(36.592725, -0.108263, 1.2865))

    subshapes_air = geompy.SubShapeAll(solid_air, geompy.ShapeType["FACE"])
    # subshapes_air = geompy.SubShapeAll(air, geompy.ShapeType["FACE"])
    # subshapes_air = geompy.SubShapeAllSortedCentres(air, geompy.ShapeType["FACE"])
    # subshapes_air = geompy.GetSharedShapesMulti(air, geompy.ShapeType['FACE'], False)
    print(subshapes_air)
    print(len(subshapes_air))

    group_faces_air = geompy.CreateGroup( self.geometry, geompy.ShapeType["FACE"])
    geompy.UnionList( group_faces_air, subshapes_air )
    self.groups['group_faces_air'] = group_faces_air
    geompy.addToStudyInFather( self.geometry, group_faces_air, 'group_faces_air' )
      
    # group_faces_air_cut = geompy.CutGroups( group_faces_air, group_faces_air_lens )
    group_faces_air_cut = geompy.CutListOfGroups( [ group_faces_air ],
                                                  [ group_faces_air_lens, group_faces_inlet ] )
                                                  # [ group_faces_air_lens, group_faces_inlet, group_faces_outlet] )

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
    # subshapes_pml_outlet = geompy.SubShapeAll(solid_pml_outlet, geompy.ShapeType["FACE"])

    group_faces_pml_inlet = geompy.CreateGroup( self.geometry, geompy.ShapeType["FACE"])
    geompy.UnionList( group_faces_pml_inlet, subshapes_pml_inlet )
    self.groups['group_faces_pml_inlet'] = group_faces_pml_inlet
    geompy.addToStudyInFather( self.geometry, group_faces_pml_inlet, 'group_faces_pml_inlet' )

    group_faces_outlet = geompy.CreateGroup( self.geometry, geompy.ShapeType["FACE"])
    # geompy.UnionList( group_faces_pml_outlet, subshapes_pml_outlet )
    self.groups['group_faces_outlet'] = group_faces_outlet
    geompy.addToStudyInFather( self.geometry, group_faces_outlet, 'group_faces_outlet' )



#########################################################

    group_faces_hemisphere = geompy.CreateGroup( self.geometry, geompy.ShapeType["FACE"])
    # geompy.UnionList( group_faces_pml_outlet, subshapes_pml_outlet )
    self.groups['group_faces_hemisphere'] = group_faces_hemisphere
    geompy.addToStudyInFather( self.geometry, group_faces_hemisphere, 'group_faces_hemisphere' )



    # group_faces_hemisphere_plane = geompy.CreateGroup( self.geometry, geompy.ShapeType["FACE"])
    # # geompy.UnionList( group_faces_pml_outlet, subshapes_pml_outlet )
    # self.groups['group_faces_hemisphere_plane'] = group_faces_hemisphere_plane
    # geompy.addToStudyInFather( self.geometry, group_faces_hemisphere_plane, 'group_faces_hemisphere_plane' )


##########################################################

    group_faces_pml_outlet = geompy.CreateGroup( self.geometry, geompy.ShapeType["FACE"])
    # geompy.UnionList( group_faces_pml_outlet, subshapes_pml_outlet )
    self.groups['group_faces_pml_outlet'] = group_faces_pml_outlet
    geompy.addToStudyInFather( self.geometry, group_faces_pml_outlet, 'group_faces_pml_outlet' )

    face_pml_inlet_left = geompy.GetFaceNearPoint(group_faces_pml_inlet,    geompy.MakeVertex( -lens_side_x/2, 0, 1.2865))
    # face_air_left_1 = geompy.GetFaceNearPoint(group_faces_air,              geompy.MakeVertex( -lens_side_x/2, 0, 57.761))
    face_air_left_2 = geompy.GetFaceNearPoint(group_faces_air,              geompy.MakeVertex( -lens_side_x/2, 0, 4.717))

    # face_pml_outlet_left = geompy.GetFaceNearPoint(group_faces_pml_outlet,  geompy.MakeVertex( -lens_side_x/2, 0, 101.2865))
    # face_pml_outlet_left = geompy.GetFaceNearPoint(group_faces_pml_outlet,  geompy.MakeVertex( -lens_side_x/2, 0, self.outlet_offset + 2*self.pml_bottom_height + self.inlet_offset + self.wavelength))
    face_outlet_hemisphere = geompy.GetFaceNearPoint(group_faces_air,  geompy.MakeVertex( -lens_side_x/2, 0, self.outlet_offset + 2*self.pml_bottom_height + self.inlet_offset + self.wavelength))
    geompy.addToStudyInFather( self.geometry, face_outlet_hemisphere, 'face_outlet_hemisphere' )
    
    face_outlet_hemisphere_plane = geompy.GetFaceNearPoint(group_faces_air,  geompy.MakeVertex( -lens_side_x/2, self.outlet_offset,  self.pml_bottom_height + self.inlet_offset + self.wavelength ))
    geompy.addToStudyInFather( self.geometry, face_outlet_hemisphere_plane, 'face_outlet_hemisphere_plane' )
    

    group_faces_air_left = geompy.CreateGroup( self.geometry, geompy.ShapeType["FACE"])
    geompy.UnionList( group_faces_air_left, [face_air_left_2, face_pml_inlet_left] )
    # geompy.UnionList( group_faces_air_left, [face_air_left_1, face_air_left_2, face_pml_inlet_left, face_pml_outlet_left] )
    self.groups['group_faces_left'] = group_faces_air_left
    geompy.addToStudyInFather( self.geometry, group_faces_air_left, 'group_faces_left' )

    face_pml_inlet_right = geompy.GetFaceNearPoint(group_faces_pml_inlet,   geompy.MakeVertex( lens_side_x/2, 0, 1.2865))
    # face_air_right_1 = geompy.GetFaceNearPoint(group_faces_air,             geompy.MakeVertex( lens_side_x/2, 0, 57.761))
    face_air_right_2 = geompy.GetFaceNearPoint(group_faces_air,             geompy.MakeVertex( lens_side_x/2, 0, 4.717))
    
    # face_pml_outlet_right = geompy.GetFaceNearPoint(group_faces_pml_outlet, geompy.MakeVertex( lens_side_x/2, 0, 101.2865))
    face_outlet_hemisphere_lens = geompy.GetFaceNearPoint(group_faces_air, geompy.MakeVertex( lens_side_x/2, 0, self.outlet_offset + 2*self.pml_bottom_height))
    geompy.addToStudyInFather( self.geometry, face_outlet_hemisphere_lens, 'face_outlet_hemisphere_lens' )

    # geompy.UnionList( group_faces_hemisphere_plane, [ face_outlet_hemisphere_plane ] )
    geompy.UnionList( group_faces_hemisphere, [ face_outlet_hemisphere ] )
    # geompy.UnionList( group_faces_outlet, [ face_outlet_hemisphere_plane, face_outlet_hemisphere, face_outlet_hemisphere_lens ] )
    # geompy.UnionList( group_faces_outlet, [ face_outlet_hemisphere_plane, face_outlet_hemisphere ] )
    geompy.UnionList( group_faces_outlet, [ face_outlet_hemisphere_plane ] )


    group_faces_air_right = geompy.CreateGroup( self.geometry, geompy.ShapeType["FACE"])
    geompy.UnionList( group_faces_air_right, [face_air_right_2, face_pml_inlet_right ] )
    # geompy.UnionList( group_faces_air_right, [face_air_right_1, face_air_right_2, face_pml_inlet_right, face_pml_outlet_right] )
    self.groups['group_faces_right'] = group_faces_air_right 
    geompy.addToStudyInFather( self.geometry, group_faces_air_right, 'group_faces_right' )

    face_pml_inlet_back = geompy.GetFaceNearPoint(group_faces_pml_inlet,    geompy.MakeVertex(0, lens_side_y/2, 1.2865))
    # face_air_back_1 = geompy.GetFaceNearPoint(group_faces_air,              geompy.MakeVertex(0, lens_side_y/2, 57.761))
    face_air_back_2 = geompy.GetFaceNearPoint(group_faces_air,              geompy.MakeVertex(0, lens_side_y/2, 4.717))
    
    # face_pml_outlet_back = geompy.GetFaceNearPoint(group_faces_pml_outlet,  geompy.MakeVertex(0, lens_side_y/2, 101.2865))
    face_pml_outlet_back = geompy.GetFaceNearPoint(group_faces_air,  geompy.MakeVertex(0, lens_side_y/2, self.outlet_offset + 2*self.pml_bottom_height + self.inlet_offset + self.wavelength ))

    group_faces_air_back = geompy.CreateGroup( self.geometry, geompy.ShapeType["FACE"])
    geompy.UnionList( group_faces_air_back, [face_air_back_2, face_pml_inlet_back ] )
    # geompy.UnionList( group_faces_air_back, [face_air_back_1, face_air_back_2, face_pml_inlet_back, face_pml_outlet_back] )
    self.groups['group_faces_back'] = group_faces_air_back
    geompy.addToStudyInFather( self.geometry, group_faces_air_back, 'group_faces_back' )

    face_pml_inlet_front = geompy.GetFaceNearPoint(group_faces_pml_inlet,   geompy.MakeVertex(0, -lens_side_y/2, 1.2865))
    # face_air_front_1 = geompy.GetFaceNearPoint(group_faces_air,             geompy.MakeVertex(0, -lens_side_y/2, 57.761))
    face_air_front_2 = geompy.GetFaceNearPoint(group_faces_air,             geompy.MakeVertex(0, -lens_side_y/2, 4.717))
    
    # face_pml_outlet_front = geompy.GetFaceNearPoint(group_faces_pml_outlet, geompy.MakeVertex(0, -lens_side_y/2, 101.2865))
    # face_pml_outlet_front = geompy.GetFaceNearPoint(group_faces_pml_outlet, geompy.MakeVertex(0, -lens_side_y/2, 101.2865))

    group_faces_air_front = geompy.CreateGroup( self.geometry, geompy.ShapeType["FACE"])
    geompy.UnionList( group_faces_air_front, [face_air_front_2, face_pml_inlet_front ] )
    # geompy.UnionList( group_faces_air_front, [face_air_front_1, face_air_front_2, face_pml_inlet_front, face_pml_outlet_front] )
    self.groups['group_faces_front'] = group_faces_air_front
    geompy.addToStudyInFather( self.geometry, group_faces_air_front, 'group_faces_front' )

    
    # Group top and bottom walls faces

    group_faces_top_bottom_walls = geompy.CreateGroup( self.geometry, geompy.ShapeType["FACE"])

    shared_faces_pml_inlet = geompy.CreateGroup( self.geometry, geompy.ShapeType["FACE"])
    geompy.UnionList( shared_faces_pml_inlet, 
                      [ group_faces_inlet, 
                        face_pml_inlet_left, 
                        face_pml_inlet_back, 
                        face_pml_inlet_right, 
                        face_pml_inlet_front ] )

    shared_faces_pml_outlet = geompy.CreateGroup( self.geometry, geompy.ShapeType["FACE"])
    # geompy.UnionList( shared_faces_pml_outlet, 
    #                   [ group_faces_outlet, face_pml_outlet_left, face_pml_outlet_back, face_pml_outlet_right, face_pml_outlet_front ] )
    
    # face_pml_outlet_outer = geompy.CutGroups( group_faces_pml_outlet, shared_faces_pml_outlet )
    face_pml_inlet_outer = geompy.CutGroups( group_faces_pml_inlet, shared_faces_pml_inlet )

    geompy.UnionList( group_faces_top_bottom_walls, [ face_pml_inlet_outer ] )
    # geompy.UnionList( group_faces_top_bottom_walls, [ face_pml_inlet_outer, face_pml_outlet_outer ] )
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
    isDone = self.mesh.Compute()  
    
    pml_bottom_mesh = self.mesh.GroupOnGeom( self.groups['solid_pml_inlet'], 'pml_inlet', SMESH.VOLUME)
    brick_mesh = self.mesh.GroupOnGeom( self.groups['solid_lens'], 'lens', SMESH.VOLUME)
    air_mesh = self.mesh.GroupOnGeom( self.groups['solid_air'], 'air', SMESH.VOLUME)

    hemisphere_faces_mesh = self.mesh.GroupOnGeom( self.groups['group_faces_hemisphere'], 'hemisphere', SMESH.FACE)
    outlet_faces_mesh = self.mesh.GroupOnGeom( self.groups['group_faces_outlet'], 'outlet', SMESH.FACE)
    
    self.inlet_face_mesh = self.mesh.GroupOnGeom( self.groups['group_faces_inlet'], 'inlet', SMESH.FACE)
    # faces_air_cut_mesh = Structure_1.GroupOnGeom( group_faces_air_cut, 'air', SMESH.FACE)
    brick_faces_mesh = self.mesh.GroupOnGeom( self.groups['group_faces_air_lens'], 'lens_air', SMESH.FACE)
    faces_lens_cut_mesh = self.mesh.GroupOnGeom( self.groups['group_faces_lens_cut'], 'lens_shell', SMESH.FACE)
    
    mesh_top_bottom = self.mesh.GroupOnGeom( self.groups['group_faces_top_bottom_walls'], 'top_bottom', SMESH.FACE)


    mesh_air_front = self.mesh.GroupOnGeom( self.groups['group_faces_front'], 'front', SMESH.FACE)
    mesh_air_back = self.mesh.GroupOnGeom( self.groups['group_faces_back'], 'back', SMESH.FACE)
    mesh_air_right = self.mesh.GroupOnGeom( self.groups['group_faces_right'], 'right', SMESH.FACE)
    mesh_air_left = self.mesh.GroupOnGeom( self.groups['group_faces_left'], 'left', SMESH.FACE)


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


  def export_complex_pressure_at_inlet( configurator,
                                  path ):
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
        print('ExportDAT() failed. Directory does not exist and could not create it')

      xx, yy, Pf = configurator
      m, n = configurator[0].shape

      try:
          with open(path, 'w') as f:
              f.write(f"{xx[i,j].shape}\n")
              for i in range(m):
                  for j in range(n):
                    f.write(f"{xx[i,j]*10**-3} {yy[i,j]*10**-3} {Pf[i,j].real} {Pf[i,j].imag}\n")
                      # print(xx[i,j], yy[i,j], Pf[i,j])
      except FileNotFoundError:
          print("The file doesn't exist")
      # finally:
          
      return


  def export_inlet_mesh( self, path) : 
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
        print('ExportDAT() failed. Directory does not exist and could not create it')

    # os.chdir(path)

    # print(self.inlet_face_mesh.GetNodeIDs())
    try:
      self.mesh.ExportDAT( path, meshPart = self.inlet_face_mesh, renumber = False ) # ExportDAT requires string as input type, not path!
    except:
      print('ExportDAT() failed. Invalid file name?')