import numpy as np
# import pandas as pd
import time, os
import random


from utility_functions import * 
from parametric_shape import * 

###
### Salome GEOM and SMESH components
###

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



