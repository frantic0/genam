
import sys, os


def run_elmer_solver(dirname):

  print( f"Running elmer solver on directory 'brick-{dirname}'" )

  path = f"C:/Users/francisco/Documents/dev/pipeline/data/brick-{dirname}"
  
  os.chdir(path)

  sif_files = [ f for f in os.listdir() if ( f.endswith(".sif") and "entities.sif" not in f ) ]

  print( sif_files )

  # execute comand and terminate
  for fileName in sif_files:
    os.system('cmd /c "ElmerSolver {}"'.format(fileName))  


dirname = int(sys.argv[1:][0])
run_elmer_solver(dirname)