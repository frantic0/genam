#!/usr/bin/env python

###
### This file is generated automatically by SALOME v9.3.0 with dump python functionality
###

from codecs import BufferedIncrementalEncoder
import sys
import salome
import numpy as np
import time, os

# Set file paths for library and tests  
sys.path.insert(0, r'C:/Users/Francisco/Documents/dev/pipeline')
sys.path.insert(0, r'C:/Users/Francisco/Documents/dev/pipeline/genam')
sys.path.insert(0, r'C:/Users/Francisco/Documents/dev/pipeline/tests')
from utility_functions import * 

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

start = time.time()
geompy = geomBuilder.New()
origin = geompy.MakeVertex(0, 0, 0)
x = geompy.MakeVectorDXDYDZ(1, 0, 0)
y = geompy.MakeVectorDXDYDZ(0, 1, 0)
z = geompy.MakeVectorDXDYDZ(0, 0, 1)
pml_bottom = geompy.MakeBoxDXDYDZ(4.288, 4.288, 2.573)
box_1 = geompy.MakeTranslation(geompy.MakeBoxDXDYDZ(4.288, 4.288, 4.288), 0, 0, 2.573)
box_2 = geompy.MakeTranslation(geompy.MakeBoxDXDYDZ(4.288, 4.288, 12.776), 0, 0, 15.522)
pml_top = geompy.MakeTranslation(pml_bottom, 0, 0, 28.298)
brick_outer = geompy.MakeTranslation(geompy.MakeBoxDXDYDZ(4.288, 4.288, 8.661), 0, 0, 6.861)

### Parameters
# l0 = 8.575, wavelength for 40kHz
l0 = 8.66
# bar thickness = l0/20
# brick thickness = l0/40
# innerRadius = 0.217 # inner radius, l0/40
# bs = outerDist/2 + outerRad + innerRad
# bl = outerRad + subLength


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
          
outerRad = 0.866
# outerRad = 0.66
innerRad = 0.2165 # λο / 40


def parameterize_brick( waveLength, barLength, barSpacing ):

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

  wire = geompy.MakeMarker(0, 0, 0, 1, 0, 0, 0, 1, 0)

  return sk.wire(wire)


def parameterize_brick_no_radii( waveLength, barLength, barSpacing ):

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

  # sk.addArcRadiusAbsolute( OR, S0 + OR, -OR, 0.0000000) # outerRadius 1
  sk.addSegmentAbsolute( 0.0000000, S0 + OR ) # outerRadius 1

  # sk.addSegmentAbsolute( OR + barLength, S0 + OR) # Horizontal Segment Bottom
  sk.addSegmentAbsolute( OR + barLength + barTip, S0 + OR) # Horizontal Segment Bottom
  
  # sk.addArcAbsolute( OR + barLength, S0 + OR + IR) # innerRadius 1
  sk.addSegmentAbsolute( OR + barLength + barTip, S0 + OR + IR) # innerRadius 1

  # sk.addSegmentAbsolute( OR, S0 + OR + IR) # Horizontal Segment Top
  sk.addSegmentAbsolute( 0.0000000, S0 + OR + IR) # Horizontal Segment Top
  
  # # sk.addArcRadiusAbsolute( 0.0000000, S0 + Bh, -OR, 0.0000000) # outerRadius 2
  sk.addSegmentAbsolute( 0.0000000, S0 + Bh ) # outerRadius 2

  sk.addSegmentAbsolute( 0.0000000, S0 + Bh + S1) # In-between flaps vertical segment LEFT


  # # FLAP 2

  # sk.addArcRadiusAbsolute( OR, S0 + Bh + S1 + OR, -OR, 0.0000000) # outerRadius 3
  sk.addSegmentAbsolute( 0.0000000, S0 + Bh + S1 + OR) # outerRadius 3
  
  sk.addSegmentAbsolute( OR + barLength + barTip, S0 + Bh + S1 + OR) # Horizontal Segment Bottom
  
  # sk.addArcAbsolute( OR + barLength, S0 + Bh + S1 + OR + IR) # innerRadius 2
  sk.addSegmentAbsolute( OR + barLength + barTip, S0 + Bh + S1 + OR + IR) # innerRadius 2

  sk.addSegmentAbsolute( 0.0000000, S0 + Bh + S1 + OR + IR) # Horizontal Segment Top

  # sk.addArcRadiusAbsolute( 0.0000000, S0 + S1 + 2 * Bh, -OR, 0.0000000) # outerRadius 4
  sk.addSegmentAbsolute( 0.0000000, S0 + S1 + 2 * Bh) # outerRadius 4
  

  sk.addSegmentAbsolute( 0.0000000, waveLength ) # top left corner



  sk.addSegmentAbsolute( waveLength/2, waveLength) # top right corner


  if(S0!=0):
    sk.addSegmentAbsolute( waveLength/2, waveLength - S0)

  # # FLAP 3  
  
  # sk.addArcRadiusAbsolute( waveLength/2 - OR, waveLength - S0 - OR, -OR, 0.0000000) # outerRadius 5   ----
  sk.addSegmentAbsolute( waveLength/2, waveLength - S0 - OR) # outerRadius 5   ----

  sk.addSegmentAbsolute( waveLength/2 - OR - barLength - barTip, waveLength - S0 - OR) # Horizontal Segment Top    ----
  
  # sk.addArcAbsolute( waveLength/2 - barLength, waveLength - S0 - OR - IR) # innerRadius 3            ----
  sk.addSegmentAbsolute( waveLength/2 - OR - barLength - barTip, waveLength - S0 - OR - IR) # innerRadius 3            ----

  # sk.addSegmentAbsolute( waveLength/2 - OR, waveLength - S0 - OR - IR) # Horizontal Segment Bottom       ----
  sk.addSegmentAbsolute( waveLength/2, waveLength - S0 - OR - IR) # Horizontal Segment Bottom       ----
  
  # sk.addArcRadiusAbsolute( waveLength/2, waveLength - S0 - Bh, -OR, 0.0000000) # outerRadius 6       ----
  sk.addSegmentAbsolute( waveLength/2, waveLength - S0 - Bh) # outerRadius 6       ----
 


  sk.addSegmentAbsolute( waveLength/2, waveLength - S0 - Bh - S1)  # In-between flaps vertical segment RIGHT 

  # FLAP 4

  # sk.addArcRadiusAbsolute( waveLength/2 - OR, waveLength - S0 - Bh - S1 - OR, -OR, 0.0000000) # outerRadius 7   ----
  sk.addSegmentAbsolute( waveLength/2, waveLength - S0 - Bh - S1 - OR) # outerRadius 7   ----

  sk.addSegmentAbsolute( waveLength/2 - OR - barLength - barTip, waveLength - S0 - Bh - S1 - OR) # Horizontal Segment Top    ----
  
  # sk.addArcAbsolute( waveLength/2 - OR - barLength, waveLength - S0 - Bh - S1 - OR - IR) # innerRadius 4            ----
  sk.addSegmentAbsolute( waveLength/2 - OR - barLength - barTip, waveLength - S0 - Bh - S1 - OR - IR) # innerRadius 4            ----

  sk.addSegmentAbsolute( waveLength/2, waveLength - S0 - Bh - S1 - OR - IR) # Horizontal Segment Bottom    ----
  
  # sk.addArcRadiusAbsolute( waveLength/2, waveLength - S0 - Bh - S1 - Bh, -OR, 0.0000000) # outerRadius 8
  sk.addSegmentAbsolute( waveLength/2, waveLength - S0 - Bh - S1 - Bh) # outerRadius 8

  sk.addSegmentAbsolute( waveLength/2, 0.0000000) # bottom segment

  sk.addSegmentAbsolute(0.0000000, 0.0000000)
  
  if(S0!=0):
    sk.addSegmentAbsolute(0.0000000, S0) 

  wire = geompy.MakeMarker(0, 0, 0, 1, 0, 0, 0, 1, 0)

  return sk.wire(wire)



def sketch_brick(brickID):

  barLength = list(barLen.values())[brickID - 1] * l0
  barSpacing = list(barSpa.values())[brickID -1] * l0

  geompy.addToStudy( parameterize_brick( l0, barLength, barSpacing ), 'Sketch' + str(brickID) )
  geompy.addToStudy( parameterize_brick_no_radii( l0, barLength, barSpacing ), 'Sketch' + str(brickID) )



def draw_bricks():

  geompy.addToStudy( x, 'x' )
  geompy.addToStudy( y, 'y' )
  geompy.addToStudy( z, 'z' )

  for bID in range(1, 16): 
    barLength = list(barLen.values())[bID - 1] * l0   # bl * l0
    barSpacing = list(barSpa.values())[bID - 1] * l0  # bs * l0
    Sketch = parameterize_brick( l0, barLength, barSpacing )
    geompy.addToStudy( Sketch, 'Sketch' + str(bID) )

sketch_brick(15)
# draw_bricks()