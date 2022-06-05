'''
This is the main file to execute GA
'''

import os, sys  
import numpy as np

### Salome GEOM and SMESH components
import salome
salome.salome_init()

### Path for Salome

# Set file paths for library and tests  
# sys.path.insert(0, r'C:/Users/Francisco/Documents/dev/pipeline')
# sys.path.insert(0, r'C:/Users/Francisco/Documents/dev/pipeline/genam')
# sys.path.insert(0, r'C:/Users/Francisco/Documents/dev/pipeline/tests')

sys.path.insert(0, r'/SAN/uclic/ammdgop/genam/')
sys.path.insert(0, r'/SAN/uclic/ammdgop/genam/genam/')
sys.path.insert(0, r'/SAN/uclic/ammdgop/genam/tests/')

from genam.optimisation.simulated_annealing import simulated_annealing
from compute_lens_optimisation_objective import compute_lens_optimisation_objective


if sys.argv == None:
   size_lens_row, size_lens_column = 2, 2
else: 
   print( 'args', sys.argv )
   size_lens_row, size_lens_column = int(sys.argv[1]), int(sys.argv[2])
   
size_lens = size_lens_row * size_lens_column

bounds = np.array( [[0,15]] * size_lens )
lens_iteration = 0

def objective(X):
  
   global lens_iteration 

   # define quantized matrix 
   quantized_mat = np.array( [np.zeros(size_lens_column).astype(int)] * size_lens_row )
   idx = 0
   for i in range (0, size_lens_row):
      for j in range(0, size_lens_column):
         quantized_mat[i,j] = X[idx]
         idx += 1
      
   lens_iteration += 1

   _, optimisation_target_pressure = compute_lens_optimisation_objective(quantized_mat, lens_iteration)

   return -(optimisation_target_pressure)


bounds = np.asarray([[-5.0, 5.0]])
n_iterations = 1000
step_size = 0.1
initial_temperature = 10

best, score, scores = simulated_annealing(objective, bounds, n_iterations, step_size, initial_temperature)

