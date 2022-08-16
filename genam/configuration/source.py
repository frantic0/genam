import numpy as np, matplotlib.pyplot as plt, matplotlib.colors, os, sys
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable
# home_path = os.path.abspath(os.getcwd()+"/..")
# print(home_path)
# sys.path.append(home_path)
# sys.path.append(home_path+"/JamesAHardwick")
# from constrained_GS_functions import *
# from functions import *


# ---> physics params <---
c = 343 # m/s
v = 40000 # Hz
lam = c/v # m
# dx_AMM = lam/2
k = 2*np.pi/lam # rads/m

# ---> AMM params <---
dist = .1 # focal length of the board [m] and distance to the AMM
prop_dist = 12*lam # focal length of the AMM [m]
resolution = 10
iterations = 200

m, n = 2,2 # Metasurface size (in units of dx_AMM)


# Transducer piston model
def piston_model_matrix(rxy, rxyz, k, p0=8.02, d=10.5/1000):
    """
    Piston model calculator
    
        Finds the complex pressure propagated by transducers from one plane to another, 
        determined using the PM_pesb function. (see GS-PAT eq.2).
    
    Params:
        rxy = matrix describing Pythagorean distances between each transducer and each evaluation point in x and y
        rxyz = matrix describing Pythagorean distances between each transducer and each evaluation point in x, y and z.
        k = wavenumber
        p0 = (8.02 [Pa]) refernce pressure for Murata transducer measured at a distance of 1m
        d = (10.5/1000 [m]) spacing between Murata transducers in a lev board.
    """
    # 1st order Bessel function
    b = k*(d/2)*(rxy/rxyz)

    # taylor expansion of the bessel function
    tay = (1/2)-(b**2/16)+(b**4/384)-(b**6/18432)+(b**8/1474560)-(b**10/176947200)
    
    return 2*p0*(tay/rxyz)*np.exp(1j*k*rxyz)
    # return 2*(p0/b)*(tay/rxyz)*np.exp(1j*k*rxyz)


def pesb(side_length_x, side_length_y, dist, cell_spacing, tx, ty, tz):

    """pressure_evaluation_space_builder"""
    
    ex = np.arange(-side_length_x/2 + cell_spacing/2, side_length_x/2 + cell_spacing/2, cell_spacing) # x side length vector 
    ey = np.arange(-side_length_y/2 + cell_spacing/2, side_length_y/2 + cell_spacing/2, cell_spacing) # y side length vector
    
    exx, eyy = np.meshgrid(ex, ey)
    # x, y & z vectors for evaluation-plane sample points:
    px, py, pz = exx.flatten(), eyy.flatten(), dist*np.ones_like(exx.flatten())

    
    # Grids to describe the vector distances between each transducer & evaluation plane sample point.
    txv, pxv = np.meshgrid(tx,px)
    tyv, pyv = np.meshgrid(ty,py)
    tzv, pzv = np.meshgrid(tz,pz)
    
    rxyz = np.sqrt((txv-pxv)**2 + (tyv-pyv)**2 + (tzv-pzv)**2)  # Pythagoras for xyz distances
    rxy = np.sqrt((txv-pxv)**2 + (tyv-pyv)**2)                  # Pythagoras for xy distances
    
    return rxyz, rxy


def configurator(   dist,
                    tm = 1,
                    tn = 1,
                    m = 2,
                    n = 2,  
                    p0 = 8.02,                  # tranducer reference pressure [Pa] 
                    dx_tran = 10.5/1000,        # diameter of a transducer [m] (actually they are 10mm in diameter, with a spacing of 0.5mm)
                    ):

    A = 1                                       # amplitude for each transducer to take (max=1, min=0)

    x = np.arange(  ( dx_tran/2 ) * ( 1 - tm ),   # transducer arrangement in x
                    ( dx_tran/2 ) * ( 1 + tm ), 
                    dx_tran ) 

    y = np.arange(  ( dx_tran/2 ) * ( 1 - tn ),
                    ( dx_tran/2 ) * ( 1 + tn ),
                    dx_tran ) # transducer arrangement in y

    xx, yy = np.meshgrid(x, y)

    zz = np.zeros_like(xx) # transducer arrangement in z

    rxyz, rxy = pesb(   m * lam/2, n * lam/2, 
                        dist, 
                        lam/2, 
                        xx, yy, zz )

    H = piston_model_matrix( rxy, rxyz, k, p0, dx_tran ) # propagator

    Pt = A * np.ones( tm * tn ) * np.exp( 1j * np.zeros( tm * tn ) ) # transducer complex pressure

    Pf = np.dot( H, Pt ).reshape( m, n ) # propagate to far field and reshape to array


    print("H:", H.shape)
    print("Pt:", Pt)
    print("Pt shape: ", Pt.shape)
    print(f'Pf: {Pf}')
    print(f'Pf shape: {Pf.shape}')

    # Plotting
    # fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(20, 7))

    # im1 = ax1.imshow(   np.mod( np.angle(Pf), 2*np.pi), 
    #                     cmap= cm.get_cmap('viridis'), 
    #                     vmin=0, 
    #                     vmax=2*np.pi ) # phase

    # divider = make_axes_locatable(ax1)
    # cax1 = divider.append_axes("right", size='5%', pad=.1)

    # # ax1.title.set_text("phasemap")
    # # ax1.set_title("phasemap", fontsize=15)
    # plt.colorbar(im1, cax=cax1)

    # im2 = ax2.imshow(   abs(Pf), 
    #                     cmap=cm.get_cmap('jet') )

    # divider = make_axes_locatable(ax2)
    # cax2 = divider.append_axes("right", size='5%', pad=.1)
    
    # ax2.set_title("propagation", fontsize=15)
    
    # plt.colorbar(im2, cax=cax2)

    # fig.tight_layout()

    # plt.show()

    pass