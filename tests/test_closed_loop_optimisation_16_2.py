import os, sys  
import numpy as np

sys.path.append(os.getcwd())        # To extract the current working directory and appended to the path

from matrices.quantized_16_2 import quantized_matrix_16_2
from compute_lens_optimisation_objective import compute_lens_optimisation_objective
from genam.optimisation.ga import geneticalgorithm as ga

## Bounds of variables ## eg.: for real: varbound=np.array([[2,10]]*3) 
size_lens_row = 16
size_lens_column = 2
size_lens1 = size_lens_row*size_lens_column

varbound = np.array([[0,15]]*(size_lens1))

def objective_function(X):
 
   # define quantized matrix 
   quantized_mat = np.array([np.zeros(size_lens_column).astype(int)]*size_lens_row)
   count1 = 0
   for i in range (0,size_lens_row):
      for j in range(0,size_lens_column):
         quantized_mat[i,j] = X[count1]
         count1 = count1 + 1
      
   optimisation_target, optimisation_target_pressure = compute_lens_optimisation_objective(quantized_matrix_16_2)

   # Penalty function for constraint 
   pen_f = 0 
   if X[1] + X[2] < 2:
      pen_f = 10e5
   else:
      pen_f = 0
      
   Obj_f = 1

   return -Obj_f + pen_f                    # for maximum --ve


## Initializing parameters
#### f : objective function to minimize (for maximization insert -ve sign in the definition or 1/f)
#### dimension: no of variables 
#### variable type : Real(real), integer(int), binary (0,1)-correction made inside
####                 mixed (both real and integer): for this also supply variable_type_mixed
####                 e.g, for 1 real and 2 int : vartype=np.array([['real'],['int'],['int']])

model = ga( function = objective_function,  
            dimension = (size_lens1),
            variable_type = 'int',
            variable_boundaries = varbound )

## execute GA
model.run()   



# final variables_after optimization (model.best_function, model.best_variable, model.final_pop)
xval = model.best_variable
fval = model.best_function
final_pop = model.final_pop
convergence=model.report


def const(xval):
   c11 = xval[0] + xval[1]
   
   if c11 > 2:
      print("constraint satisfied")
   else:
      print("constraint NOT satisfied")   

   return c11

c1 = const(xval)

#np.savetxt('variable.txt',xval,fval,f1)
#np.savetxt('final_pop.csv', [final_pop], delimiter=',', fmt='%d')





