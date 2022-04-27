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

    # evpsl = ( elem_num/4 ) * wavelength # evaluation plane side length
    plane_length = lambda x : wavelength * x / 4 

    dx = wavelength/2 # [m]

    aperture_size = ( int( 2* plane_length(m) /dx ), int( 2* plane_length(n) /dx ) ) # aperture size (number of unit cells) 

    x_vec = np.arange(-( aperture_size[0]/2 - 0.5 ) * dx, ( aperture_size[0]/2 + 0.5) * dx, dx)
    y_vec = np.arange(-( aperture_size[1]/2 - 0.5 ) * dx, ( aperture_size[1]/2 + 0.5) * dx, dx)

    xx, yy = np.meshgrid(x_vec, y_vec)

    travel_distance_array = np.sqrt( xx**2 + yy**2 + focal_length**2 ) # matrix of distances from centre of each elem to focus

    total_phase_array = -travel_distance_array * k # total change in phase of waves as they travel this distance.

    return np.remainder(total_phase_array, 2*np.pi) # normalise phase to 0-2π [rads] to perform focusing, assuming incident plane wave



fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(7,7))

im = ax.imshow( calculate_focus_lens_phase_distribution(16, 4, 0.1) )

plt.colorbar(im)
plt.show()