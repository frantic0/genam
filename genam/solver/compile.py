
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

def compile_pressure_reader(path):

  f90_files = [ f for f in os.listdir(path) if ( f.endswith(".f90") ) ]
  os.chdir(path)
  # execute comand and terminate
  if os.name == 'posix':
    os.system( 'elmerf90 -o readComplexPressure.dll readComplexPressure.f90' )  
  elif os.name == 'nt':
    # os.system('cmd /c "dir "'.format(fileName))  
    # os.system('cmd /c "ElmerSolver {}"'.format(fileName))  
    subprocess.call(["elmerf90 -o readComplexPressure.dll readComplexPressure.f90"])
