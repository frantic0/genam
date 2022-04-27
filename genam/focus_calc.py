import numpy as np
import matplotlib.pyplot as plt

def calculate_focus_lens_phase_distribution(m, n, focal_length = 0.1):
    '''
        focal_length (SI meters)


    '''
    
    c = 343 # m/s
    f = 40000 # Hz
    wavelength = c/f # m
    k = 2*np.pi/wavelength # wave number (rads/m)

    xx, yy = np.meshgrid(
                        np.arange( -( m/2 - 0.5 ) * wavelength/2, ( m/2 + 0.5 ) * wavelength/2, wavelength/2 ),
                        np.arange( -( n/2 - 0.5 ) * wavelength/2, ( n/2 + 0.5 ) * wavelength/2, wavelength/2 )
                        )
    print(xx)
    print(yy)
    
    travel_distances = np.sqrt( xx**2 + yy**2 + focal_length**2 ) # matrix of distances from centre of each elem to focus
    print(travel_distances)

    total_phases = -travel_distances * k # total change in phase of waves as they travel this distance.

    return np.remainder(total_phases, 2*np.pi) # normalise phase to 0-2π [rads] to perform focusing, assuming incident plane wave



fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(7,7))

im = ax.imshow( calculate_focus_lens_phase_distribution(16, 2, 0.1) )

plt.colorbar(im)
plt.show()