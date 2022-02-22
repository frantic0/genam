import sys
import salome
import numpy as np
import time, os, shutil
from export_solver_input_file import export_parameterisable_solver_input_file

import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS

def sketch_to_volume(geom_builder, sketch_obj, thickness, rotation=None, translation=None):
  # Inputs
  # 
  #   sketch: 2d sketch of the object
  #   thickness: thickness of volume in z axis
  #   rotation: provide a list of tuples with (axis, angle) as a tuple i.e. (x, 90), in the order you want to rotate in x axis
  #
  # Returns
  #   
  #   sketch_rotation: sketch to 3d object
  
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



def copy_elmer_templates( dirname, start_frequency=40000, end_frequency=41000, step=1000 ): 

  src = r'C:/Users/francisco/Documents/dev/pipeline/solver/'  
  dst = r'C:/Users/francisco/Documents/dev/pipeline/data/' + dirname + '/'

  # print('copy template to dest: ' + dst)

  for fileName in os.listdir(src):
    source = src + fileName
    destination = dst + fileName 
    if os.path.isfile(source):
      shutil.copy(source, destination)
      print('copied', fileName)

  # NOTE: Needs refactor - if optional arguments  
  for frequency in range(start_frequency, end_frequency + step, step):
    export_parameterisable_solver_input_file( dirname, frequency )



def export_elmer(filename):
  """
  Input

    filename: name of the .unv file exported by Salome

  Output

    .unv to *.mesh (Elmer format)
  
  """
  print(filename)
  # os.system(f'cmd /c "dir C:\Users\francisco\Documents\dev\pipeline\data\brick-15"')
  # execute comand and terminate
  # os.chdir(f"C:/Users/francisco/Documents/dev/pipeline/data/{dirname}")
  os.system('cmd /c "ElmerGrid 8 2 {}.unv -autoclean"'.format(filename))  

