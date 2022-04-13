
import configparser
import sys
import salome
import numpy as np
# import pandas as pd
import time, os
import random


salome.salome_init()
import salome_notebook
notebook = salome_notebook.NoteBook()

sys.path.insert(0, r'C:/Users/francisco/Documents/dev/pipeline/genam')

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


class Brick():
    def __init__(self,
                 wavelength,
                 flatlength,
                 flapwidth,
                 translation ):
        
        self.wavelength


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
                            translation[0],
                            translation[1],
                            translation[2] )    



        else: 

          Sketch_1 = parameterize_2D_inner_shape( self.wavelenght,
                                                  self.unit_cells_config[m][n][1] * self.wavelenght,
                                                  self.unit_cells_config[m][n][2] * self.wavelenght )

          # geompy.addToStudy( Sketch_1, 'Sketch' )
          rotation = [(x, 90)]
          
          # translation = ( waveLenght/40, waveLenght/40 + waveLenght/2, 6.861)
          # translation_x = self.wavelenght/40 + column * ( self.wavelenght/40 + self.wavelenght/2 )     
          # translation_y = self.wavelenght/40 + row * (self.wavelenght/40 + self.wavelenght/2 )     
          
          # translation = ( translation_shift[0] + translation_x,
          #                 translation_shift[1] + translation_y + self.wavelenght/2, 
          #                 6.861 )
          
          try:
            brick_inner = sketch_to_volume( geompy, Sketch_1, self.wavelenght /2, rotation, translation)

        pass


