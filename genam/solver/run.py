
import sys, os
import subprocess
from threading import Thread
import subprocess

# def call_subprocess(cmd):
#     proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     out, err = proc.communicate()
#     if err:
#         print err

# thread = Thread(target=call_subprocess, args=[cmd])
# thread.start()
# thread.join() # waits for completion.

def run_elmer_solver(path):

  sif_files = [ f for f in os.listdir(path) if ( f.endswith(".sif") ) ]
  # sif_files = [ f for f in os.listdir(path) if ( f.endswith(".sif") and "entities.sif" not in f ) ]
  os.chdir(path)
  # execute comand and terminate
  for filename in sif_files:
    if os.name == 'posix':
      os.system('ElmerSolver {}'.format(filename))  
    elif os.name == 'nt':
      # os.system('cmd /c "dir "'.format(fileName))  
      # os.system('cmd /c "ElmerSolver {}"'.format(fileName))  
      subprocess.call(["ElmerSolver", "{}".format(filename)])


def run_elmer_solver_parallel(path, n):

  # sif_files = [ f for f in os.listdir(path) if ( f.endswith(".sif") and "entities.sif" not in f ) ]
  sif_files = [ f for f in os.listdir(path) if ( f.endswith(".sif") ) ]
  os.chdir(path)
  # execute comand and terminate
  for filename in sif_files:
    if os.name == 'posix':
      os.system('mpirun -np {} ElmerSolver_mpi {}'.format(n, filename))  
    elif os.name == 'nt':
      # os.system('cmd /c "mpirun -np {} ElmerSolver_mpi {}"'.format(n, fileName))  
      subprocess.call(["mpirun", "-np", "{}".format(n), "ElmerSolver_mpi", "{}".format(filename), ])


# dirname = int(sdys.argv[1:][0])
# run_elmer_solver(dirname)