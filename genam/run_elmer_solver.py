
import sys, os


def run_elmer_solver(path):

  user_defined_path = os.path.splitext(path)[0]

  sif_files = [ f for f in os.listdir(user_defined_path) if ( f.endswith(".sif") and "entities.sif" not in f ) ]

  print( sif_files )

  # execute comand and terminate
  for fileName in sif_files:
    if os.name == 'posix':
      os.system('ElmerSolver {}'.format(fileName))  
    elif os.name == 'nt':
      os.system('cmd /c "ElmerSolver {}"'.format(fileName))  



def run_elmer_solver_parallel(path, n):

  user_defined_path = os.path.splitext(path)[0]

  sif_files = [ f for f in os.listdir(user_defined_path) if ( f.endswith(".sif") and "entities.sif" not in f ) ]

  print( sif_files )

  # execute comand and terminate
  for fileName in sif_files:
    if os.name == 'posix':
      os.system('mpirun -np {} ElmerSolver_mpi {}'.format(n, fileName))  
    elif os.name == 'nt':
      os.system('cmd /c "mpirun -np {} ElmerSolver_mpi {}"'.format(n, fileName))  



# dirname = int(sys.argv[1:][0])
# run_elmer_solver(dirname)