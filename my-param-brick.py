#!/usr/bin/env python

###
### This file is generated automatically by SALOME v9.3.0 with dump python functionality
###

import sys
import salome
import numpy as np
import time, os
os.chdir(r"C:/Users/Francisco/Documents/dev/elmer-workshop/acoustic-brick")
# os.chdir(r"C:\Users\Francisco\dev\acoustic-brick")
# sys.path.insert(0, "C:\\Users\\Francisco\\dev\\acoustic-brick")
sys.path.insert(0, r'C:/Users/Francisco/Documents/dev/elmer-workshop/acoustic-brick')
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
# bs, inter-bar spacing from = {'b1': 0.216, 'b2': 0.212, 'b3': 0.207, 'b4': 0.189, 'b5': 0.161, 'b6': 0.166, 'b7': 0.171, 'b8': 0.134, 'b9': 0.257, 'b10': 0.234, 'b11': 0.230, 'b12': 0.207, 'b13': 0.203, 'b14': 0.175, 'b15': 0.152}
# bl, bar length = {'b1': 0.062, 'b2': 0.092, 'b3': 0.112, 'b4': 0.132, 'b5': 0.152, 'b6': 0.162, 'b7': 0.171, 'b8': 0.191, 'b9': 0.221, 'b10': 0.241, 'b11': 0.251, 'b12': 0.271, 'b13': 0.281, 'b14': 0.301, 'b15': 0.321}
# outerRadius = {'b1': 0.062, 'b2': 0.092, 'b3': 0.1, 'b4': 0.1, 'b5': 0.1, 'b6': 0.1, 'b7': 0.1, 'b8': 0.1, 'b9': 0.1, 'b10': 0.1, 'b11': 0.1, 'b12': 0.1, 'b13': 0.1, 'b14': 0.1, 'b15': 0.1}
# innerRadius = 0.217 # inner radius, l0/40
# bs = outerDist/2 + outerRad + innerRad
# bl = outerRad + subLength

# barSpacing = 2.57 #  out of bounds
# barSpacing = 2.34 # out of bounds
barSpacing = 2.30 # out of bounds
# barSpacing = 2.165
# barSpacing = 2.12
# barSpacing = 2.07
# barSpacing = 1.89
# barSpacing = 1.61
# barSpacing = 1.71
# barSpacing = 1.0825
# barSpacing = 0.54125

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
          
outerRad = 0.866
# outerRad = 0.66
innerRad = 0.217 # λο / 40
# subLength = 0.533 + barLen['b15']
subLength = 2

# S0 = 1.0910000

def draw_hardcoded_brick(outerRadius):
  ### Make brick sketch
  sk = geompy.Sketcher2D()
  sk.addPoint(0., 1.091) # beggining from bottom left
  # sk.addArcRadiusAbsolute(0.866, 1.9570000, -outerRadius, 0.0000000) # outerRadius 1
  sk.addSegmentAbsolute(1.3990000, 1.9570000) 
  sk.addArcAbsolute(1.3990000, 2.3900000) # innerRadius 1
  sk.addSegmentAbsolute(0.8660000, 2.3900000)
  # sk.addArcRadiusAbsolute(0.0000000, 3.2570000, -outerRadius, 0.0000000) # outerRadius 2
  sk.addSegmentAbsolute(0.0000000, 3.9670000)
  # sk.addArcRadiusAbsolute(0.8660000, 4.8330000, -outerRadius, 0.0000000) # outerRadius 3
  sk.addSegmentAbsolute(1.3990000, 4.8330000)
  # sk.addArcAbsolute(1.3990000, 5.2660000) # innerRadius 2
  sk.addSegmentAbsolute(0.8660000, 5.2660000)
  # sk.addArcRadiusAbsolute(0.0000000, 6.1320000, -outerRadius, 0.0000000) # outerRadius 4
  sk.addSegmentAbsolute(0.0000000, 8.6610000) # top left corner
  sk.addSegmentAbsolute(3.8480000, 8.6610000) # top right corner
  sk.addSegmentAbsolute(3.8480000, 7.5700000)
  # sk.addArcRadiusAbsolute(2.9810000, 6.7040000, -outerRadius, 0.0000000) # outerRadius 5
  sk.addSegmentAbsolute(2.4480000, 6.7040000)
  # sk.addArcAbsolute(2.4480000, 6.2710000) # innerRadius 3
  sk.addSegmentAbsolute(2.9810000, 6.2710000)
  # sk.addArcRadiusAbsolute(3.8480000, 5.4050000, -outerRadius, 0.0000000) # outerRadius 6
  sk.addSegmentAbsolute(3.8480000, 4.6940000)
  # sk.addArcRadiusAbsolute(2.9810000, 3.8280000, -outerRadius, 0.0000000) # outerRadius 7
  sk.addSegmentAbsolute(2.4480000, 3.8280000)
  # sk.addArcAbsolute(2.4480000, 3.3950000) # innerRadius 4
  sk.addSegmentAbsolute(2.9810000, 3.3950000)
  # sk.addArcRadiusAbsolute(3.8480000, 2.5290000, -outerRadius, 0.0000000) # outerRadius 8

  sk.addSegmentAbsolute(3.8480000, 0.0000000) # bottom segment
  sk.addSegmentAbsolute(0.0000000, 0.0000000)
  # sk.addSegmentAbsolute(0.0000000, 1.0910000) 

  wire = geompy.MakeMarker(0, 0, 0, 1, 0, 0, 0, 1, 0)
  return sk.wire(wire)


def parameterize_brick_len(outerRadius, barLength):
  ### Make brick sketch
  sk = geompy.Sketcher2D()
  sk.addPoint(0., 1.091) # beggining from bottom left

  sk.addArcRadiusAbsolute(0.866, 1.9570000, -outerRadius, 0.0000000) # outerRadius 1
  sk.addSegmentAbsolute(0.866 + barLength, 1.9570000) 
  
  sk.addArcAbsolute(0.866 + barLength, 2.3900000) # innerRadius 1
  sk.addSegmentAbsolute(0.8660000, 2.3900000)
  
  sk.addArcRadiusAbsolute(0.0000000, 3.2570000, -outerRadius, 0.0000000) # outerRadius 2
  sk.addSegmentAbsolute(0.0000000, 3.9670000)
  
  sk.addArcRadiusAbsolute(0.8660000, 4.8330000, -outerRadius, 0.0000000) # outerRadius 3
  sk.addSegmentAbsolute(0.866 + barLength, 4.8330000)
  
  sk.addArcAbsolute(0.866 + barLength, 5.2660000) # innerRadius 2
  sk.addSegmentAbsolute(0.8660000, 5.2660000)
  
  sk.addArcRadiusAbsolute(0.0000000, 6.1320000, -outerRadius, 0.0000000) # outerRadius 4
  
  sk.addSegmentAbsolute(0.0000000, 8.6610000) # top left corner
  sk.addSegmentAbsolute(3.8480000, 8.6610000) # top right corner
  sk.addSegmentAbsolute(3.8480000, 7.5700000)
  
  sk.addArcRadiusAbsolute(2.9810000, 6.7040000, -outerRadius, 0.0000000) # outerRadius 5
  sk.addSegmentAbsolute(2.981 - barLength, 6.7040000)
  
  sk.addArcAbsolute(2.981 - barLength, 6.2710000) # innerRadius 3
  sk.addSegmentAbsolute(2.9810000, 6.2710000)
  
  sk.addArcRadiusAbsolute(3.8480000, 5.4050000, -outerRadius, 0.0000000) # outerRadius 6
  sk.addSegmentAbsolute(3.8480000, 4.6940000)
  
  sk.addArcRadiusAbsolute(2.9810000, 3.8280000, -outerRadius, 0.0000000) # outerRadius 7
  sk.addSegmentAbsolute(2.981 - barLength, 3.8280000)
  
  sk.addArcAbsolute(2.981 - barLength, 3.3950000) # innerRadius 4
  sk.addSegmentAbsolute(2.9810000, 3.3950000)
  
  sk.addArcRadiusAbsolute(3.8480000, 2.5290000, -outerRadius, 0.0000000) # outerRadius 8

  sk.addSegmentAbsolute(3.8480000, 0.0000000) # bottom segment
  sk.addSegmentAbsolute(0.0000000, 0.0000000)
  sk.addSegmentAbsolute(0.0000000, 1.0910000) 

  wire = geompy.MakeMarker(0, 0, 0, 1, 0, 0, 0, 1, 0)
  return sk.wire(wire)

# Sketch = parameterize_brick_len(outerRad, subLength)
# Sketch = parameterize_brick_spacing(outerRad, subLength, barSpacing )


def parameterize_brick_v1(outerRadius, barLength, barSpacing):

  ### Make brick sketch
  sk = geompy.Sketcher2D()

  # Bar height - constant 
  ORy = 0.866         # outer radius height
  IRy = 0.433         # inner radius height
  Bh = 2 * ORy + IRy  # bar height 


  
  S0 = l0 - ( 3 * barSpacing + Bh ) # For Bh = 2.165, S0 = 0

  S1 = 2 * barSpacing - Bh - S0 

  # sk.addPoint(0., 1.091) # beggining from bottom left
  sk.addPoint(0., S0) # beggining from bottom left

  # sk.addArcRadiusAbsolute(0.866, 1.9570000, -outerRadius, 0.0000000) # outerRadius 1
  sk.addArcRadiusAbsolute(0.866, S0 + ORy, -outerRadius, 0.0000000) # outerRadius 1

  # sk.addSegmentAbsolute(0.866 + barLength, 1.9570000) 
  sk.addSegmentAbsolute(0.866 + barLength, S0 + ORy) 
  
  # sk.addArcAbsolute(0.866 + barLength, 2.3900000) # innerRadius 1
  sk.addArcAbsolute(0.866 + barLength, S0 + ORy + IRy) # innerRadius 1

  # sk.addSegmentAbsolute(0.8660000, 2.3900000)
  sk.addSegmentAbsolute(0.8660000, S0 + ORy + IRy)
  
  # sk.addArcRadiusAbsolute(0.0000000, 3.2570000, -outerRadius, 0.0000000) # outerRadius 2
  sk.addArcRadiusAbsolute(0.0000000, S0 + Bh, -outerRadius, 0.0000000) # outerRadius 2


  
  # sk.addSegmentAbsolute(0.0000000, 3.9670000)
  sk.addSegmentAbsolute(0.0000000, S0 + Bh + S1) # In-between flaps vertical segment LEFT


  # sk.addArcRadiusAbsolute(0.8660000, 4.8330000, -outerRadius, 0.0000000) # outerRadius 3
  sk.addArcRadiusAbsolute(0.8660000, S0 + Bh + S1 + ORy, -outerRadius, 0.0000000) # outerRadius 3
  
  # # sk.addSegmentAbsolute(0.866 + barLength, 4.8330000)
  sk.addSegmentAbsolute(0.866 + barLength, S0 + Bh + S1 + ORy)
  
  # # sk.addArcAbsolute(0.866 + barLength, 5.2660000) innerRadius 2
  sk.addArcAbsolute(0.866 + barLength, S0 + Bh + S1 + ORy + IRy) # innerRadius 2

  # # sk.addSegmentAbsolute(0.8660000, 5.2660000)
  sk.addSegmentAbsolute(0.8660000, S0 + Bh + S1 + ORy + IRy)

  # # sk.addArcRadiusAbsolute(0.0000000, 6.1320000, -outerRadius, 0.0000000) # outerRadius 4
  sk.addArcRadiusAbsolute(0.0000000, S0 + S1 + 2 * Bh, -outerRadius, 0.0000000) # outerRadius 4
  
  # # sk.addSegmentAbsolute(0.0000000, 8.6610000) # top left corner
  sk.addSegmentAbsolute(0.0000000, l0 ) # top left corner




  # sk.addSegmentAbsolute(3.8480000, 8.6610000) # top right corner
  sk.addSegmentAbsolute(3.8480000, l0) # top right corner

  if(S0!=0):
  # sk.addSegmentAbsolute(3.8480000, 7.5700000)
    sk.addSegmentAbsolute(3.8480000, l0 - S0)
  
  # sk.addArcRadiusAbsolute(2.9810000, 6.7040000, -outerRadius, 0.0000000) # outerRadius 5
  sk.addArcRadiusAbsolute(2.9810000, l0 - S0 - ORy, -outerRadius, 0.0000000) # outerRadius 5

  # sk.addSegmentAbsolute(2.981 - barLength, 6.7040000)
  sk.addSegmentAbsolute(2.981 - barLength, l0 - S0 - ORy)
  
  # sk.addArcAbsolute(2.981 - barLength, 6.2710000) # innerRadius 3
  sk.addArcAbsolute(2.981 - barLength, l0 - S0 - ORy - IRy) # innerRadius 3

  # sk.addSegmentAbsolute(2.9810000, 6.2710000)
  sk.addSegmentAbsolute(2.9810000, l0 - S0 - ORy - IRy)
  
  # sk.addArcRadiusAbsolute(3.8480000, 5.4050000, -outerRadius, 0.0000000) # outerRadius 6
  sk.addArcRadiusAbsolute(3.8480000, l0 - S0 - Bh, -outerRadius, 0.0000000) # outerRadius 6
 



  # sk.addSegmentAbsolute(3.8480000, 4.6940000)
  sk.addSegmentAbsolute(3.8480000, l0 - S0 - Bh - S1)  # In-between flaps vertical segment RIGHT


  # sk.addArcRadiusAbsolute(2.9810000, 3.8280000, -outerRadius, 0.0000000) # outerRadius 7
  sk.addArcRadiusAbsolute(2.9810000, l0 - S0 - Bh - S1 - ORy, -outerRadius, 0.0000000) # outerRadius 7

  # sk.addSegmentAbsolute(2.981 - barLength, 3.8280000)
  sk.addSegmentAbsolute(2.981 - barLength, l0 - S0 - Bh - S1 - ORy)
  
  # sk.addArcAbsolute(2.981 - barLength, 3.3950000) # innerRadius 4
  sk.addArcAbsolute(2.981 - barLength, l0 - S0 - Bh - S1 - ORy - IRy) # innerRadius 4

  # sk.addSegmentAbsolute(2.9810000, 3.3950000)
  sk.addSegmentAbsolute(2.9810000, l0 - S0 - Bh - S1 - ORy - IRy)
  
  # sk.addArcRadiusAbsolute(3.8480000, 2.5290000, -outerRadius, 0.0000000) # outerRadius 8
  sk.addArcRadiusAbsolute(3.8480000, l0 - S0 - Bh - S1 - Bh, -outerRadius, 0.0000000) # outerRadius 8

  sk.addSegmentAbsolute(3.8480000, 0.0000000) # bottom segment

  sk.addSegmentAbsolute(0.0000000, 0.0000000)
  
  if(S0!=0):
    sk.addSegmentAbsolute(0.0000000, S0) 

  wire = geompy.MakeMarker(0, 0, 0, 1, 0, 0, 0, 1, 0)
  # print(Bh)
  return sk.wire(wire)

def parameterize_brick(outerRadius, barLength, barSpacing):

  ### Make brick sketch
  sk = geompy.Sketcher2D()

  # Bar height - constant 
  ORy = 0.866         # outer radius height - 
  IRy = 0.433         # inner radius height - l0/20
  Bh = 2 * ORy + IRy  # bar height 

  # S0 = l0 - ( 3 * barSpacing + Bh ) # For Bh = 2.165, S0 = 0
  # S0 = l0 - ( l0/2 + ( l0/2 - ( 3 * barSpacing/2 ) + Bh/2 ) )
  S0 = l0 - ( l0/2 + 3* barSpacing/2 + Bh/2 ) 

  S1 = 2 * barSpacing - Bh

  sk.addPoint(0., S0) # beggining from bottom left


  sk.addArcRadiusAbsolute(0.866, S0 + ORy, -outerRadius, 0.0000000) # outerRadius 1

  sk.addSegmentAbsolute(0.866 + barLength, S0 + ORy) 
  
  sk.addArcAbsolute(0.866 + barLength, S0 + ORy + IRy) # innerRadius 1

  sk.addSegmentAbsolute(0.8660000, S0 + ORy + IRy)
  
  sk.addArcRadiusAbsolute(0.0000000, S0 + Bh, -outerRadius, 0.0000000) # outerRadius 2


  sk.addSegmentAbsolute(0.0000000, S0 + Bh + S1) # In-between flaps vertical segment LEFT


  sk.addArcRadiusAbsolute(0.8660000, S0 + Bh + S1 + ORy, -outerRadius, 0.0000000) # outerRadius 3
  
  sk.addSegmentAbsolute(0.866 + barLength, S0 + Bh + S1 + ORy)
  
  sk.addArcAbsolute(0.866 + barLength, S0 + Bh + S1 + ORy + IRy) # innerRadius 2

  sk.addSegmentAbsolute(0.8660000, S0 + Bh + S1 + ORy + IRy)

  sk.addArcRadiusAbsolute(0.0000000, S0 + S1 + 2 * Bh, -outerRadius, 0.0000000) # outerRadius 4
  

  sk.addSegmentAbsolute(0.0000000, l0 ) # top left corner



  sk.addSegmentAbsolute(3.8480000, l0) # top right corner


  if(S0!=0):
    sk.addSegmentAbsolute(3.8480000, l0 - S0)
  
  sk.addArcRadiusAbsolute(2.9810000, l0 - S0 - ORy, -outerRadius, 0.0000000) # outerRadius 5

  sk.addSegmentAbsolute(2.981 - barLength, l0 - S0 - ORy)
  
  sk.addArcAbsolute(2.981 - barLength, l0 - S0 - ORy - IRy) # innerRadius 3

  sk.addSegmentAbsolute(2.9810000, l0 - S0 - ORy - IRy)
  
  sk.addArcRadiusAbsolute(3.8480000, l0 - S0 - Bh, -outerRadius, 0.0000000) # outerRadius 6
 


  sk.addSegmentAbsolute(3.8480000, l0 - S0 - Bh - S1)  # In-between flaps vertical segment RIGHT

  sk.addArcRadiusAbsolute(2.9810000, l0 - S0 - Bh - S1 - ORy, -outerRadius, 0.0000000) # outerRadius 7

  sk.addSegmentAbsolute(2.981 - barLength, l0 - S0 - Bh - S1 - ORy)
  
  sk.addArcAbsolute(2.981 - barLength, l0 - S0 - Bh - S1 - ORy - IRy) # innerRadius 4

  sk.addSegmentAbsolute(2.9810000, l0 - S0 - Bh - S1 - ORy - IRy)
  
  sk.addArcRadiusAbsolute(3.8480000, l0 - S0 - Bh - S1 - Bh, -outerRadius, 0.0000000) # outerRadius 8

  sk.addSegmentAbsolute(3.8480000, 0.0000000) # bottom segment

  sk.addSegmentAbsolute(0.0000000, 0.0000000)
  
  if(S0!=0):
    sk.addSegmentAbsolute(0.0000000, S0) 

  wire = geompy.MakeMarker(0, 0, 0, 1, 0, 0, 0, 1, 0)
  # print(Bh)
  return sk.wire(wire)



def draw_brick(brickID):

  barLength = list(barLen.values())[brickID - 1] * 10
  barSpacing = list(barSpa.values())[brickID -1] * 10

  Sketch = parameterize_brick( outerRad, barLength, barSpacing )


  geompy.addToStudy( x, 'x' )
  geompy.addToStudy( y, 'y' )
  geompy.addToStudy( z, 'z' )
  geompy.addToStudy( Sketch, 'Sketch' )



def draw_bricks():

  geompy.addToStudy( x, 'x' )
  geompy.addToStudy( y, 'y' )
  geompy.addToStudy( z, 'z' )

  for bID in range(1, 16): 
    barLength = list(barLen.values())[bID-1] * l0   # bl * l0
    barSpacing = list(barSpa.values())[bID-1] * l0  # bs * l0
    Sketch = parameterize_brick( outerRad, barLength, barSpacing )
    geompy.addToStudy( Sketch, 'Sketch' + str(bID) )


# draw_brick(6)
draw_bricks()