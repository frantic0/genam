
import salome
import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS

import SMESH, SALOMEDS
from salome.smesh import smeshBuilder
from salome.GMSHPlugin import GMSHPluginBuilder


class Brick():
    
    def __init__( self,
                  wavelength,
                  flaplength,
                  flapspacing,
                  translation ):
        
        self.wavelength = wavelength
        self.boxSide = self.wavelength/2 + 2 * self.wavelength/40
        self.wavelength = wavelength
        self.flaplength = flaplength

        if self.flaplength == 0 or self.flapspacing == 0 :
          # brick_inner = geompy.MakeTranslation(
          #                   geompy.MakeBoxDXDYDZ( boxSide - 2 * self.wavelenght/40, 
          #                                         boxSide - 2 * self.wavelenght/40, 
          #                                         self.wavelenght ),
          #                   self.wavelenght/40, 
          #                   self.wavelenght/40,
          #                   pml_bottom_height + air_bottom_height )    

          brick_inner = geompy.MakeTranslation(
                            geompy.MakeBoxDXDYDZ( self.boxSide - 2 * self.wavelength/40, 
                                                  self.boxSide - 2 * self.wavelength/40, 
                                                  self.wavelength ),
                            translation[0],
                            translation[1],
                            translation[2] )    

        else: 

          Sketch_1 = parameterize_2D_inner_shape( self.wavelenght,
                                                  flaplength * self.wavelenght,
                                                  flapspacing * self.wavelenght )

          # geompy.addToStudy( Sketch_1, 'Sketch' )
          rotation = [(x, 90)]
          
          # translation = ( waveLenght/40, waveLenght/40 + waveLenght/2, 6.861)
          # translation_x = self.wavelenght/40 + column * ( self.wavelenght/40 + self.wavelenght/2 )     
          # translation_y = self.wavelenght/40 + row * (self.wavelenght/40 + self.wavelenght/2 )     
          
          # translation = ( translation_shift[0] + translation_x,
          #                 translation_shift[1] + translation_y + self.wavelenght/2, 
          #                 6.861 )
          
          try:
            brick_inner = self.__sketch_to_volume__( geompy, Sketch_1, self.wavelenght /2, rotation, translation)
          except:   
            pass


    def sketch_to_volume(geom_builder, sketch_obj, thickness, rotation=None, translation=None):
      """
      Inputs
      
        sketch: 2d sketch of the object
        thickness: thickness of volume in z axis
        rotation: provide a list of tuples with (axis, angle) as a tuple i.e. (x, 90), in the order you want to rotate in x axis
      
      Returns
        
      sketch_rotation: sketch to 3d object
      
      """
      try:

        sketch_face = geom_builder.MakeFaceWires( [sketch_obj], 1) # make sketch object

        sketch_volume = geom_builder.MakePrismDXDYDZ(sketch_face, 0, 0, thickness) # extrude
        
        temp = sketch_volume
        
        if rotation is not None:
          for (axis, angle) in rotation:
            sketch_rotation = geom_builder.MakeRotation(temp, axis, angle * math.pi / 180.0) # rotate
            temp = sketch_rotation

        if translation is not None:
          sketch_rotation = geom_builder.MakeTranslation(sketch_rotation, translation[0], translation[1], translation[2])
          
        return sketch_rotation

      except:
        print("Error extruding in sketch_to_volume: {} {} {}".format( sketch_obj, thickness ) )

        return None


    def __sketch_to_volume__(sketch_obj, 
                             thickness, 
                             rotation=None, 
                             translation=None):
      """
      Inputs
    
        sketch: 2d sketch of the object
        thickness: thickness of volume in z axis
        rotation: provide a list of tuples with (axis, angle) as a tuple i.e. (x, 90), in the order you want to rotate in x axis
    
      Returns

       sketch_rotation: sketch to 3d object
    
      """
      try:

        sketch_face = geom_builder.MakeFaceWires( [sketch_obj], 1) # make sketch object

        sketch_volume = geom_builder.MakePrismDXDYDZ(sketch_face, 0, 0, thickness) # extrude

        temp = sketch_volume

        if rotation is not None:
          for (axis, angle) in rotation:
            sketch_rotation = geom_builder.MakeRotation(temp, axis, angle * math.pi / 180.0) # rotate
            temp = sketch_rotation

        if translation is not None:
          sketch_rotation = geom_builder.MakeTranslation(sketch_rotation, translation[0], translation[1], translation[2])

        return sketch_rotation

      except:
        print("Error extruding in sketch_to_volume: {} {} {}".format( sketch_obj, thickness ) )

        return None



def sketch_to_volume(geom_builder, sketch_obj, thickness, rotation=None, translation=None):
  """
  Inputs
  
    sketch: 2d sketch of the object
    thickness: thickness of volume in z axis
    rotation: provide a list of tuples with (axis, angle) as a tuple i.e. (x, 90), in the order you want to rotate in x axis
  
  Returns
     
   sketch_rotation: sketch to 3d object
  
  """
  try:

    sketch_face = geom_builder.MakeFaceWires( [sketch_obj], 1) # make sketch object

    sketch_volume = geom_builder.MakePrismDXDYDZ(sketch_face, 0, 0, thickness) # extrude
    
    temp = sketch_volume
    
    if rotation is not None:
      for (axis, angle) in rotation:
        sketch_rotation = geom_builder.MakeRotation(temp, axis, angle * math.pi / 180.0) # rotate
        temp = sketch_rotation

    if translation is not None:
      sketch_rotation = geom_builder.MakeTranslation(sketch_rotation, translation[0], translation[1], translation[2])
      
    return sketch_rotation

  except:
    print("Error extruding in sketch_to_volume: {} {} {}".format( sketch_obj, thickness ) )


def parameterize_2D_inner_shape( waveLength, barLength, barSpacing ):
  """
  Draws a labyrynthine brick  

    Inputs
  
    sketch: 2d sketch of the object
    thickness: thickness of volume in z axis
    rotation: provide a list of tuples with (axis, angle) as a tuple i.e. (x, 90), in the order you want to rotate in x axis
  
  Returns

    a sketcher2D wire (set of edges)  
  """

  try:

    ### Make brick sketch
    sk = geompy.Sketcher2D()

    # Bar height - constant 
    OR = waveLength/10         # outer radius height - 
    IR = waveLength/20         # inner radius height - l0/20
    Bh = 2 * OR + IR  # bar height 

    S0 = waveLength - ( waveLength/2 + 3*barSpacing/2 + Bh/2 ) 

    S1 = 2 * barSpacing - Bh

    barTip = waveLength/40

    sk.addPoint(0., S0) # begin from bottom left


    # FLAP 1

    sk.addArcRadiusAbsolute( OR, S0 + OR, -OR, 0.0000000) # outerRadius 1

    sk.addSegmentAbsolute( OR + barLength, S0 + OR) # Horizontal Segment Bottom
    
    sk.addArcAbsolute( OR + barLength, S0 + OR + IR) # innerRadius 1

    sk.addSegmentAbsolute( OR, S0 + OR + IR) # Horizontal Segment Top
    
    sk.addArcRadiusAbsolute( 0.0000000, S0 + Bh, -OR, 0.0000000) # outerRadius 2

    sk.addSegmentAbsolute( 0.0000000, S0 + Bh + S1) # In-between flaps vertical segment LEFT


    # FLAP 2

    sk.addArcRadiusAbsolute( OR, S0 + Bh + S1 + OR, -OR, 0.0000000) # outerRadius 3
    
    sk.addSegmentAbsolute( OR + barLength, S0 + Bh + S1 + OR) # Horizontal Segment Bottom
    
    sk.addArcAbsolute( OR + barLength, S0 + Bh + S1 + OR + IR) # innerRadius 2

    sk.addSegmentAbsolute( OR, S0 + Bh + S1 + OR + IR) # Horizontal Segment Top

    sk.addArcRadiusAbsolute( 0.0000000, S0 + S1 + 2 * Bh, -OR, 0.0000000) # outerRadius 4

    sk.addSegmentAbsolute( 0.0000000, waveLength ) # top left corner

    sk.addSegmentAbsolute( waveLength/2, waveLength) # top right corner


    if(S0!=0):
      sk.addSegmentAbsolute( waveLength/2, waveLength - S0)

    # FLAP 3  
    
    sk.addArcRadiusAbsolute( waveLength/2 - OR, waveLength - S0 - OR, -OR, 0.0000000) # outerRadius 5   ----

    sk.addSegmentAbsolute( waveLength/2 - OR - barLength, waveLength - S0 - OR) # Horizontal Segment Top    ----
    
    sk.addArcAbsolute( waveLength/2 - OR - barLength, waveLength - S0 - OR - IR) # innerRadius 3            ----

    sk.addSegmentAbsolute( waveLength/2 - OR, waveLength - S0 - OR - IR) # Horizontal Segment Top       ----
    
    sk.addArcRadiusAbsolute( waveLength/2, waveLength - S0 - Bh, -OR, 0.0000000) # outerRadius 6       ----
  


    sk.addSegmentAbsolute( waveLength/2, waveLength - S0 - Bh - S1)  # In-between flaps vertical segment RIGHT 

    # FLAP 4

    sk.addArcRadiusAbsolute( waveLength/2 - OR, waveLength - S0 - Bh - S1 - OR, -OR, 0.0000000) # outerRadius 7   ----

    sk.addSegmentAbsolute( waveLength/2 - OR - barLength, waveLength - S0 - Bh - S1 - OR) # Horizontal Segment Top    ----
    
    sk.addArcAbsolute( waveLength/2 - OR - barLength, waveLength - S0 - Bh - S1 - OR - IR) # innerRadius 4            ----

    sk.addSegmentAbsolute( waveLength/2 - OR, waveLength - S0 - Bh - S1 - OR - IR) # Horizontal Segment Bottom    ----
    
    sk.addArcRadiusAbsolute( waveLength/2, waveLength - S0 - Bh - S1 - Bh, -OR, 0.0000000) # outerRadius 8

    sk.addSegmentAbsolute( waveLength/2, 0.0000000) # bottom segment

    sk.addSegmentAbsolute(0.0000000, 0.0000000)
    
    if(S0!=0):
      sk.addSegmentAbsolute(0.0000000, S0) 

    wire = geompy.MakeMarker(0, 0, 0, 
                            1, 0, 0, 
                            0, 1, 0)

    return sk.wire(wire)
  
  except:

    print("Error drawing 2Dsketch: {} {} {}".format( waveLength, barLength, barSpacing ) )

    return None


