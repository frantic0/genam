import numpy as np, matplotlib.pyplot as plt, matplotlib.colors, matplotlib.cm as cm, os, sys
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable



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


def inlet_grid( unit_cell_size,
                side_length_x, 
                side_length_y ):

    ex = np.arange(   # x side length vector 
        unit_cell_size * (-side_length_x + 1)/2, 
        unit_cell_size * ( side_length_x + 1)/2, 
        unit_cell_size ) 
    

    ey = np.arange(   # y side length vector
        unit_cell_size * (-side_length_y + 1)/2, 
        unit_cell_size * ( side_length_y + 1)/2, 
        unit_cell_size )
    
    exx, eyy = np.meshgrid(ex, ey)

    return exx, eyy


def transducer_grid( pitch, # inter-element spacing or pitch between adjacent transducer
                     transducers_m, 
                     transducers_n ):

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


def transducer_inlet_grid(  transducer_grid,
                            inlet_grid,
                            dist ):

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

def plotter( Pf ):

    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(20, 7))

    im1 = ax1.imshow(   # phase
            np.mod( np.angle(Pf), 2*np.pi), 
            cmap = cm.get_cmap('viridis'), 
            vmin = 0, 
            vmax = 2*np.pi ) 

    divider = make_axes_locatable(ax1)
    cax1 = divider.append_axes("right", size='5%', pad=.1)

    # ax1.title.set_text("phasemap")
    # ax1.set_title("phasemap", fontsize=15)
    plt.colorbar(im1, cax=cax1)

    im2 = ax2.imshow(   
            abs(Pf), 
            cmap=cm.get_cmap('jet') )

    divider = make_axes_locatable(ax2)
    cax2 = divider.append_axes("right", size='5%', pad=.1)
    
    ax2.set_title("propagation", fontsize=15)
    
    plt.colorbar(im2, cax=cax2)

    fig.tight_layout()

    plt.show()

def write_complex_pressure_inlet_( configurator,

                                  path ):


    exx, eyy,  Pf =  configurator

    for m in m = 2,
                    n = 2,  


    pass

def configurator(   dist,
                    tm = 1,
                    tn = 1,
                    m = 2,
                    n = 2,  
                    p0 = 8.02,                  # tranducer reference pressure [Pa] 
                    pitch = 10.5/1000 ):        # inter-element spacing or pitch between adjacent transducer [m] 
                                                # ( diameter of a transducer 10mm + spacing of 0.5mm )

    A = 1                                       # amplitude for each transducer to take (max=1, min=0)

    rxyz, rxy = transducer_inlet_grid( 
                    transducer_grid( pitch, tm, tn ),
                    inlet_grid( lam/2, m, n ), 
                    dist
                    )

    H = piston_model_matrix( rxy, rxyz, k, p0, pitch ) # propagator

    Pt = A * np.ones( tm * tn ) * np.exp( 1j * np.zeros( tm * tn ) ) # transducer complex pressure

    Pf = np.dot( H, Pt ).reshape( m, n ) # propagate to far field and reshape to array

    # print("H:", H.shape)
    # print("Pt:", Pt)
    # print("Pt shape: ", Pt.shape)
    # print(f'Pf: {Pf}')
    # print(f'Pf shape: {Pf.shape}')

    exx, eyy = inlet_grid( lam/2, m, n )

    return exx.flatten(), eyy.flatten(), Pf.flatten()
   