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


    self.pml_bottom_height = 0

    self.source_config = source_config

    pass




  def __create_hemisphere__(  self, radius = 17.322, translationDZ = 16.2 ):
    '''
    Create hemisphere for wave diffusion from the outlet to the farfield

    '''    
    sphere_inner = geompy.MakeSphereR(radius)
    sphere_outer = geompy.MakeSphereR(radius + self.pml_bottom_height)
    # box_cut = geompy.MakeBoxDXDYDZ(40, 40, 20)
    box_cut = geompy.MakeBoxDXDYDZ((radius + self.pml_bottom_height)*2, (radius + self.pml_bottom_height)*2, radius + self.pml_bottom_height)
    # self.geompy.TranslateDXDYDZ(box_cut, -20, -20, -20)
    self.geompy.TranslateDXDYDZ(box_cut, -(radius + self.pml_bottom_height),
                                         -(radius + self.pml_bottom_height), 
                                         -(radius + self.pml_bottom_height) )
                                         
    partition_spheres = geompy.MakePartition([ sphere_inner, sphere_outer ], [], [], [], geompy.ShapeType["SOLID"], 0, [], 0)
    cut_spheres = geompy.MakeCutList(partition_spheres, [box_cut], True)
    hemisphere = geompy.TranslateDXDYDZ(cut_spheres, 0, 0, translationDZ)
    
    geompy.addToStudy( sphere_inner, 'sphere_inner' )
    geompy.addToStudy( sphere_outer, 'sphere_outer' )
    # geompy.addToStudy( box_cut, 'box_cut' )
    geompy.addToStudy( partition_spheres, 'partition_spheres' )
    geompy.addToStudy( cut_spheres, 'cut_spheres' )
    
    return hemisphere


  def __create_resample_target__(  self, radius = 17.322, translationDZ = 16.2 ):
    '''
    Create hemisphere for wave diffusion from the outlet to the farfield

    '''    

    box_cut = geompy.MakeBoxDXDYDZ(40, 40, 20)
    self.geompy.TranslateDXDYDZ(box_cut, -20, -20, translationDZ)

    geompy.addToStudy( box_cut, 'box_cut' )

    
    # return hemisphere
    return box_cut

  def __process_unit_cells_grid__( self, translation_shift ):
    """
    Assembles list of unit cells framed in a 2D grid according to the metasurface configuration


    """

    unit_cells = list()

    row = 0
    column = 0

    unit_cell_container_size = self.wavelength/2 + 2 * self.wavelength/40

#    for m in range( 0, self.m ):                    # Y row index
#      for n in range( 0, self.n ):                  # X column index
    for m in range( self.m-1, -1, -1 ):                    # Y row index
      for n in range( self.n-1, -1, -1 ):                  # X column index

        unit_cell_negative = {}

        # y_translation_shift =  -( self.wavelength/40 + self.m * ( self.wavelength/2 + self.wavelength/40 )) / 2 
        # x_translation_shift =  -( self.wavelength/40 + self.n * ( self.wavelength/2 + self.wavelength/40 )) / 2
      
        if self.unit_cells_config[m][n][0] < 0:         # if NEGATIVE number, unit will be blocked, do not add unit cell negative for lens cut
          pass

        elif self.unit_cells_config[m][n][0] == 0:      # if ZERO, add empty unit cell for lens cut
          
          translation = (
            translation_shift[0] + self.wavelength/40 + column * ( self.wavelength/2 + self.wavelength/40 ),
            translation_shift[1] + self.wavelength/40 +    row * ( self.wavelength/2 + self.wavelength/40 ),
            0 )     
    
          unit_cell_negative = geompy.MakeTranslation(
                                  geompy.MakeBoxDXDYDZ( unit_cell_container_size - 2 * self.wavelength/40, 
                                                        unit_cell_container_size - 2 * self.wavelength/40, 
                                                        self.wavelength ),
                                  translation[0],
                                  translation[1],
                                  self.pml_bottom_height + self.inlet_offset )    

          unit_cells.append( unit_cell_negative )


        else:                                         # if greater than zero, set brick ID as template for corresponding cell for lens cut

          # TODO unit_cell_negative = Labyrinthine()
          
          sketch = parameterize_2D_inner_shape_no_radii(  self.wavelength,
                                                          self.unit_cells_config[m][n][1] * self.wavelength,
                                                          self.unit_cells_config[m][n][2] * self.wavelength )
          # geompy.addToStudy( Sketch_1, 'Sketch' )
          
          rotation = [(x, 90)]

          translation = (
            translation_shift[0] + self.wavelength/40 + column * ( self.wavelength/2 + self.wavelength/40 ),
            translation_shift[1] + self.wavelength/40 +    row * ( self.wavelength/2 + self.wavelength/40 ) + self.wavelength/2,
            self.pml_bottom_height + self.inlet_offset 
          )
            
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

    return unit_cells 






  def process_geometry(self):
    """
    
    """
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

    # geompy.addToStudy( pml_bottom, 'pml_bottom' )

    # translation = ( 0, 0, 0 )

    x_translation_shift =  -( self.wavelength/40 + self.n * ( self.wavelength/2 + self.wavelength/40 )) / 2 
    y_translation_shift =  -( self.wavelength/40 + self.m * ( self.wavelength/2 + self.wavelength/40 )) / 2
   
    # translation_lens_center_origin = ( 
    #                 -( self.wavelength/40 + self.n * ( self.wavelength/2 + self.wavelength/40 )) / 2,
    #                 -( self.wavelength/40 + self.m * ( self.wavelength/2 + self.wavelength/40 )) / 2,
    #                 0
    #               )

    # pml_bottom = {}
    # if self.pml_bottom_height > 0:
    #   pml_bottom = geompy.MakeTranslation( geompy.MakeBoxDXDYDZ( lens_side_x, lens_side_y, self.pml_bottom_height),
    #                                         x_translation_shift, 
    #                                         y_translation_shift,
    #                                         0 )
    #################################
    
    # DEBUG

    # lens = geompy.MakeTranslation(  geompy.MakeBoxDXDYDZ( lens_side_x, lens_side_y, self.wavelength ),
                                          # x_translation_shift, 
                                          # y_translation_shift,
                                          # # 0 )
                                          # self.pml_bottom_height + self.inlet_offset )


    # geompy.addToStudy( lens_outer, 'lens_outer' )

    #################################
    

    air_inlet = {}

    if self.inlet_offset > 0:
      air_inlet = geompy.MakeTranslation( geompy.MakeBoxDXDYDZ( lens_side_x, lens_side_y, self.inlet_offset ),
                                          x_translation_shift, 
                                          y_translation_shift,
                                          self.pml_bottom_height )
      # geompy.addToStudy( air_inlet, 'air_inlet' )
    
   
    # unit_cells = self.__process_unit_cells_grid__( ( x_translation_shift, y_translation_shift ) )

    #################################

    # Fuse the Lens_Outer (box that will contain all the brics ) with all the bricks  

    # geompy.addToStudy( lens_fused, 'Fused' )

    # group_fused = geompy.CreateGroup( lens_fused, geompy.ShapeType["FACE"] )

    # lens_fused_faces = geompy.SubShapeAll( group_fused, geompy.ShapeType["FACE"] )

    #################################

    # Cut the bricks positives from the above fused result 
    # lens = geompy.MakeCutList( lens_fused, unit_cells, True)
    # geompy.addToStudy( lens, 'Lens' )

    # lens_faces = []
    # lens_faces =  geompy.ExtractShapes(lens, geompy.ShapeType["FACE"], True) # generates 1946 faces instead of 54
    # # print( '#lensFaces: {}'.format(len(lens_faces)) ) 
    # print( *lens_faces, sep='\n') 

    # hemisphere = pml_top = air_outlet = {}


    air = self.__create_resample_target__(  radius = self.outlet_offset,
                                                translationDZ = self.pml_bottom_height + self.inlet_offset + self.wavelength )
      
      # air_outlet = geompy.MakeTranslation(  geompy.MakeBoxDXDYDZ( lens_side_x, lens_side_y, self.outlet_offset ),
      #                                       x_translation_shift, 
      #                                       y_translation_shift, 
      #                                       self.pml_bottom_height + self.inlet_offset + self.wavelength )

      # geompy.addToStudy( hemisphere, 'hemisphere' )

      # pml_top = geompy.MakeTra
      # nslation( pml_bottom,
      #                                   0, 0,
      #                                   self.pml_bottom_height + self.inlet_offset + self.wavelength + self.outlet_offset )


    # lens = geompy.MakeFuseList( [ lens, air ], True, True)

    self.geometry = geompy.MakePartition([air], [], [], [], geompy.ShapeType["SOLID"], 0, [], 0)
    # self.geometry = geompy.MakePartition([lens, air], [], [], [], geompy.ShapeType["SOLID"], 0, [], 0)
    
    geompy.addToStudy( self.geometry, 'geometry' )
    return
  
  # def flatten(t):
  #   return [item for sublist in t for item in sublist]

  
  def __set_mesh_strategy__(  self, 
                              algo = smeshBuilder.NETGEN_1D2D3D ) :
    """
    
    """

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
      Param_3D.SetMinSize( 1 )
      Param_3D.SetMaxSize( 8 )
      # Param_3D.SetOrder( 2 )
      # Set output format - 2: unv
      # Param_3D.SetFormat( 2 )

    return



  # TODO : validate inputs & add exceptions
  def process_mesh( self,
                    algo = smeshBuilder.NETGEN_1D2D3D ) :
                    
    self.mesh = self.smesh.Mesh(self.geometry)
    
    self.__set_mesh_strategy__( algo )
    
    # Add meshing groups
    isDone = self.mesh.Compute()  
    
    if self.set_PML:
      pml_bottom_mesh = self.mesh.GroupOnGeom( self.groups['solid_pml_inlet'], 'pml_inlet', SMESH.VOLUME)
      mesh_top_bottom = self.mesh.GroupOnGeom( self.groups['group_faces_top_bottom_walls'], 'top_bottom', SMESH.FACE)

    brick_mesh = self.mesh.GroupOnGeom( self.groups['solid_lens'], 'lens', SMESH.VOLUME)
    air_mesh = self.mesh.GroupOnGeom( self.groups['solid_air'], 'air', SMESH.VOLUME)

    # hemisphere_faces_mesh = self.mesh.GroupOnGeom( self.groups['group_faces_hemisphere'], 'hemisphere', SMESH.FACE)
    outlet_faces_mesh = self.mesh.GroupOnGeom( self.groups['group_faces_outlet'], 'outlet', SMESH.FACE)
    
    # faces_air_cut_mesh = Structure_1.GroupOnGeom( group_faces_air_cut, 'air', SMESH.FACE)
    brick_faces_mesh = self.mesh.GroupOnGeom( self.groups['group_faces_air_lens'], 'lens_air', SMESH.FACE)
    faces_lens_cut_mesh = self.mesh.GroupOnGeom( self.groups['group_faces_lens_cut'], 'lens_shell', SMESH.FACE)
    
    self.inlet_face_mesh = self.mesh.GroupOnGeom( self.groups['group_faces_inlet'], 'inlet', SMESH.FACE)

    if self.inlet_offset > 0.001:
      mesh_air_front = self.mesh.GroupOnGeom( self.groups['group_faces_front'], 'front', SMESH.FACE)
      mesh_air_back = self.mesh.GroupOnGeom( self.groups['group_faces_back'], 'back', SMESH.FACE)
      mesh_air_right = self.mesh.GroupOnGeom( self.groups['group_faces_right'], 'right', SMESH.FACE)
      mesh_air_left = self.mesh.GroupOnGeom( self.groups['group_faces_left'], 'left', SMESH.FACE)
    
    return


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


  def export_complex_pressure_at_inlet( self, configurator, path ):
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

    xx, yy, Pf = configurator.xx, configurator.yy, configurator.Pf
    m, n = configurator.m, configurator.n
    
    try:
      with open(path, 'w') as f:

        f.write(f"{ configurator.wavelength/2 } { m } { n }\n") # write first line to enable parsing of the file the f90 module 
            
        for i in range(m):
          for j in range(n):
            # f.write(f"{xx[i,j]*1e-2} {yy[i,j]*1e-2} {Pf[i,j].real} {Pf[i,j].imag}\n")
            f.write(f"{ xx[i,j] } { yy[i,j] } { Pf[i,j].real } { Pf[i,j].imag }\n")
            print(xx[i,j], yy[i,j], Pf[i,j])
    except FileNotFoundError:
      print("The file doesn't exist!")          
    
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