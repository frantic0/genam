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
sys.path.insert(0, r'C:/Users/Francisco/Documents/dev/pipeline')
sys.path.insert(0, r'C:/Users/Francisco/Documents/dev/pipeline/genam')
sys.path.insert(0, r'C:/Users/Francisco/Documents/dev/pipeline/tests')

# sys.path.insert(0, r'/home/bernardo/genam/')
# sys.path.insert(0, r'/home/bernardo/genam/genam/')
# sys.path.insert(0, r'/home/bernardo/genam/tests/')

from genam.optimisation.ga import geneticalgorithm as ga
from compute_lens_optimisation_objective import compute_lens_optimisation_objective


if sys.argv == None:
   size_lens_row, size_lens_column = 2, 2
else: 
   print( 'args', sys.argv )
   size_lens_row, size_lens_column = sys.argv[2], sys.argv[3]
   
size_lens = size_lens_row * size_lens_column

## Bounds of variables ## eg.: for real: varbound=np.array([[2,10]]*3) 
varbound = np.array([[0,15]]*(size_lens))
lens_iteration = 0

def objective_function(X):
  
   global lens_iteration 

   # define quantized matrix 
   quantized_mat = np.array([np.zeros(size_lens_column).astype(int)]*size_lens_row)
   idx = 0
   for i in range (0, size_lens_row):
      for j in range(0, size_lens_column):
         quantized_mat[i,j] = X[idx]
         idx += 1
      
   lens_iteration += 1

   optimisation_target, optimisation_target_pressure = compute_lens_optimisation_objective(quantized_mat, lens_iteration)

   return -( optimisation_target_pressure )             # for maximum --ve


## Initializing parameters
#### f : objective function to minimize (for maximization insert -ve sign in the definition or 1/f)
#### dimension: no of variables 
#### variable type : Real(real), integer(int), binary (0,1)-correction made inside
####                 mixed (both real and integer): for this also supply variable_type_mixed
####                 e.g, for 1 real and 2 int : vartype=np.array([['real'],['int'],['int']])

model = ga( function = objective_function,  
            dimension = ( size_lens),
            variable_type = 'int',
            variable_boundaries = varbound )

## execute GA
model.run()   



# final variables_after optimization (model.best_function, model.best_variable, model.final_pop)
xval = model.best_variable
fval = model.best_function
final_pop = model.final_pop
convergence=model.report


#def const(xval):
#   c11 = xval[0] + xval[1]
#   
#   if c11 > 2:
#      print("constraint satisfied")
#   else:
#      print("constraint NOT satisfied")   
#
#   return c11
#
#c1 = const(xval)

#np.savetxt('variable.txt',xval,fval,f1)
#np.savetxt('final_pop.csv', [final_pop], delimiter=',', fmt='%d')





