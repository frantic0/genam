import numpy as np, matplotlib.pyplot as plt, matplotlib.colors, matplotlib.cm as cm, os, sys
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable
  

# Transducer piston model
def piston_model_matrix( rxy, rxyz, k, p0 = 8.02, d = 10.5/1000 ):
  """ 
  Piston model calculator
  
  Finds the complex pressure propagated by transducers from one plane to another, 
  sdetermined using the PM_pesb function. (see GS-PAT eq.2).
  
  Args:
    rxy: matrix describing Pythagorean distances between each transducer and each evaluation point in x and y
    rxyz: matrix describing Pythagorean distances between each transducer and each evaluation point in x, y and z.
    k: wavenumber
    p0: (8.02 [Pa]) refernce pressure for Murata transducer measured at a distance of 1m
    d: (10.5/1000 [m]) spacing between Murata transducers in a lev board.
  """
  # 1st order Bessel function
  b = k*(d/2)*(rxy/rxyz)
  # taylor expansion of the bessel function
  tay = (1/2)-(b**2/16)+(b**4/384)-(b**6/18432)+(b**8/1474560)-(b**10/176947200)
  
  return 2*p0*(tay/rxyz)*np.exp(1j*k*rxyz)
  # return 2*(p0/b)*(tay/rxyz)*np.exp(1j*k*rxyz)



    

def transducer_grid( pitch,         # inter-element spacing or pitch between adjacent transducer
                     transducers_m, 
                     transducers_n 
                    ) -> tuple[ np.ndarray, np.ndarray, np.ndarray ]:
                    

  tx = np.arange(          # transducer arrangement in x 
          pitch * (-transducers_m + 1 ) /2, 
          pitch * ( transducers_m + 1 ) /2, 
          pitch ) 
          
  ty = np.arange(          # transducer arrangement in y 
          pitch * (-transducers_n + 1 ) /2, 
          pitch * ( transducers_n + 1 ) /2, 
          pitch ) 
  
  txx, tyy = np.meshgrid(tx, ty)
  tzz = np.zeros_like(txx)  # transducer arrangement in z 
  return txx, tyy, tzz



def inlet_grid( unit_cell_size,
                side_length_x, 
                side_length_y, 
                sparse = False,
                indexing = 'xy' ) -> list[ np.ndarray ]:

  """
  
  
  """

  x = np.arange(   # x side length vector 
          unit_cell_size * (-side_length_x + 1)/2, 
          unit_cell_size * ( side_length_x + 1)/2, 
          unit_cell_size ) 
  
  y = np.arange(   # y side length vector
          unit_cell_size * (-side_length_y + 1)/2, 
          unit_cell_size * ( side_length_y + 1)/2, 
          unit_cell_size )
  
  return np.meshgrid( x, y, sparse = sparse, indexing = indexing )



def transducer_inlet_grid(  transducer_grid,
                            inlet_grid,
                            dist ) -> tuple:
  """
  
  """
  txx, tyy, tzz = transducer_grid
  exx, eyy = inlet_grid

  # x, y & z vectors for evaluation-plane sample points:
  px, py = exx.flatten(), eyy.flatten(),
  pz = dist * np.ones_like( exx.flatten() )
  
  txv, pxv = np.meshgrid( txx, px )
  tyv, pyv = np.meshgrid( tyy, py )
  tzv, pzv = np.meshgrid( tzz, pz )    

  rxyz = np.sqrt( (txv-pxv)**2 + (tyv-pyv)**2 + (tzv-pzv)**2 )  # Pythagoras for xyz distances
  rxy  = np.sqrt( (txv-pxv)**2 + (tyv-pyv)**2 )                 # Pythagoras for xy distances
  
  return rxyz, rxy



def plotter( Pf ) -> None:

  fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(20, 7))
  
  im1 = ax1.imshow(   # phase
          np.mod( np.angle(Pf), 2*np.pi), 
          cmap = cm.get_cmap('viridis'), 
          vmin = 0, 
          vmax = 2*np.pi ) 
  
  divider = make_axes_locatable(ax1)
  cax1 = divider.append_axes("right", size='5%', pad=.1)
  ax1.set_title("phasemap", fontsize=15)
  plt.colorbar(im1, cax=cax1)
  
  im2 = ax2.imshow( abs(Pf), cmap=cm.get_cmap('jet') )
  divider = make_axes_locatable(ax2)
  cax2 = divider.append_axes("right", size='5%', pad=.1)
  ax2.set_title("propagation", fontsize=15)
  plt.colorbar(im2, cax=cax2)
  fig.tight_layout()
  plt.show()



def write_complex_pressure_inlet( configurator, path ) -> None:

  xx, yy, Pf = configurator.xx, configurator.yy, configurator.Pf
  m, n = configurator.m, configurator.n
  
  try:
      with open(path, 'w') as f:
          f.write(f"{ m } { n }\n") # write first line to enable parsing of the file the f90 module 
          # f.write(f"{ configurator.wavelength/2 } { m } { n }\n") # write first line to enable parsing of the file the f90 module 
          
          for i in range(m):
              for j in range(n):
                  # f.write(f"{xx[i,j]*1e-2} {yy[i,j]*1e-2} {Pf[i,j].real} {Pf[i,j].imag}\n")
                  f.write(f"{ xx[i,j] } { yy[i,j] } { Pf[i,j].real } { Pf[i,j].imag }\n")
                  print(xx[i,j], yy[i,j], Pf[i,j])
  
  except FileNotFoundError:
      print("The file doesn't exist!")
  # finally:
      
  return

class configurator:

  def __init__( self,
                dist,
                tm = 1,
                tn = 1,
                m = 2,
                n = 2,  
                p0 = 8.02,                  # tranducer reference pressure [Pa] 
                pitch = 10.5/1000,          # inter-element spacing or pitch between adjacent transducer [m], ( diameter of a transducer 10 mm + spacing of 0.5mm ) 
                A = 1,                      # amplitude for each transducer to take (max=1, min=0)
                wavelength = 343/40000 ):
    """
    Source configurator


    Args:
      p0: tranducer reference pressure [Pa] 
      pitch: inter-element spacing or pitch between adjacent transducer [m], ( diameter of a transducer 10 mm + spacing of 0.5mm ) 
      A: amplitude for each transducer to take (max=1, min=0)
    """       
                                          
    self.dist = dist
    self.tm = tm
    self.tn = tn
    self.m  = m
    self.n  = n  
    self.p0 = p0                  
    self.pitch = pitch          
    self.A = A  
    self.wavelength = wavelength                
    self.k = 2*np.pi/wavelength # rads/m

    self.Pf = {}
    self.xx = {}
    self.yy = {}
    
    self.__propagate__()
    

  def __propagate__( self ) :

    rxyz, rxy = transducer_inlet_grid( 
                    transducer_grid( self.pitch, self.tm, self.tn ),
                    inlet_grid( self.wavelength/2, self.m, self.n ), 
                    self.dist )

    H = piston_model_matrix( rxy, rxyz, self.k, self.p0, self.pitch ) # propagator

    phases = np.zeros( self.tm * self.tn ) # all transducer PHASES set to zero

    amplitudes = self.A * np.ones( self.tm * self.tn ) # all transducer AMPLITUDES set to A

    Pt = amplitudes * np.ones( self.tm * self.tn ) * np.exp( 1j * phases ) # transducer complex pressure

    self.Pf = np.dot( H, Pt ).reshape( self.n, self.m ) # propagate to far field and reshape to array

    # meshgrid with matrix indexing with inputs of length M and N, 
    # the outputs are of shape (N, M) for ‘xy’ indexing and (M, N) for ‘ij’ indexing.
    self.xx, self.yy = inlet_grid( self.wavelength/2, self.m, self.n, sparse=False, indexing='ij' )


   