import os
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

import itertools as it
import math as math

from scipy.special import comb

def padwidth(N, array):
    '''
    Function to pad zeros to an image and maintain a constant size.
    '''
    return ((int((N - array.shape[0]) / 2), int((N - array.shape[0]) / 2)),
            (int((N - array.shape[1]) / 2), int((N - array.shape[1]) / 2)))

def ASM_fw(f, cell_spacing, target_plane_dist, res_fac, k):
    ''' 
    Forward angular spectrum method
    '''

    f = np.kron(f, np.ones((res_fac, res_fac)))
    
    # Nfft = target_plane_shape[0] # new side length of array
    Nfft = len(f)
    
    kx = 2*np.pi*(np.arange(-Nfft/2,(Nfft)/2)/((cell_spacing/res_fac)*Nfft)) # kx vector
    kx = np.reshape(kx, (1,len(kx))) # shape correctly
    ky = kx
    f_pad = np.pad(f, padwidth(Nfft, np.zeros(f.shape)), # pad to make F the correct size
                          'constant', constant_values = 0) 
    F = np.fft.fft2(f_pad) # 2D FT
    F = np.fft.fftshift(F) # Shift to the centre
    ## Propagate forwards    
    H = np.exp(1j*np.lib.scimath.sqrt(k**2 - kx**2 - (ky**2).T)*target_plane_dist) # propagator function
    Gf = F*H # propagating the signal forward in Fourier space
    gf = np.fft.ifft2(np.fft.ifftshift(Gf)) # IFT & shift to return to real space
    return gf

def ASM_bw(f, cell_spacing, target_plane, k):
    ''' 
    Backward angular spectrum method
    '''
    Nfft = len(f)  # new side length of array
    kx = 2 * np.pi * (np.arange(-Nfft / 2, (Nfft) / 2) / (cell_spacing * Nfft))  # kx vector
    kx = np.reshape(kx, (1, len(kx)))  # shape correctly
    ky = kx
    F = np.fft.fft2(f)  # 2D FT
    F = np.fft.fftshift(F)  # Shift to the centre

    ## Propagate backwards
    H = np.exp(1j * np.lib.scimath.sqrt(k ** 2 - kx ** 2 - (ky ** 2).T) * target_plane)  # propagator function
    Hb = np.conj(H)  # conjugate of propagator will result in backpropagation
    Gb = F * Hb  # propagating backwards from target to lens
    gb = np.fft.ifft2(np.fft.ifftshift(Gb))  # IFT & shift to return to real space
    
    return gb  # return backpropagation


def prop(phasemap, cell_spacing, target_dist, res_fac, k):
    '''
    Propagate a phasemap forward to a parallel plane at a given resolution. 
    
    Returns a complex pressure field.
    '''
    
    aperture = ((phasemap != 0).astype(int))
    lpp = aperture * np.exp(1j * phasemap)
    f = np.kron(lpp, np.ones((res_fac, res_fac)))
    Nfft = f.shape
    
    ## Calculate and shape k vectors
    kx = 2*np.pi*(np.arange(-Nfft[0]/2,(Nfft[0])/2)/((cell_spacing/res_fac)*Nfft[0])).reshape((1, Nfft[0]))
    ky = 2*np.pi*(np.arange(-Nfft[1]/2,(Nfft[1])/2)/((cell_spacing/res_fac)*Nfft[1])).reshape((1, Nfft[1]))
    
    ## Fourier transform
    F = np.fft.fft2(f) # 2D FT
    F = np.fft.fftshift(F) # Shift to the centre
    
    ## Propagate forwards    
    H = np.exp(1j*np.lib.scimath.sqrt(k**2 - kx**2 - (ky**2).T)*target_dist) # propagator function
    Gf = F*H.T # propagating the signal forward in Fourier space
    gf = np.fft.ifft2(np.fft.ifftshift(Gf)) # IFT & shift to return to real space
    return gf
    
    
def target_builder(char_list, font_file, fontsize, im_h):
    from PIL import Image, ImageDraw, ImageFont 
    bg_color = (255, 255, 255) # Image background color (white)
    slice_threshold = 0.05 # sum values in row or column and delete them if below this threshold
    target_images = []
    for count, char in enumerate(char_list):
        fnt = ImageFont.truetype(font_file, fontsize) # Create font object
        w, h = fnt.getsize(str(char))
        im = Image.new('RGB', (w, h), color = bg_color)
        draw = ImageDraw.Draw(im)
        draw.text((0, 0), str(char), font=fnt, fill="black")
    #     im = im.rotate(45)

        target_image = np.array(im)[:,:,:1]
        target_image = np.reshape(target_image[:,:],(target_image.shape[0], target_image.shape[1]))
        target_image = 1 - target_image/255 # normalise

        # remove rows < threshold
        x_del = []
        for i, x in enumerate(np.sum(target_image, axis=1)):
            if x < slice_threshold:
                x_del.append(i)
        target_image = np.delete(target_image, x_del, axis=0)

        # remove columns < threshold
        y_del = []
        for j, y in enumerate(np.sum(target_image, axis=0)):
            if y < slice_threshold:
                y_del.append(j)
        target_image = np.delete(target_image, y_del, axis=1)

        # pad zeros around the characters
        target_dummy = target_image
        w, h = target_dummy.shape[0], target_dummy.shape[1]
        target_image = np.zeros((im_h, im_h))    
        target_image[int((im_h-w)/2): int((im_h+w)/2), int((im_h-h)/2):int((im_h+h)/2)] = target_dummy   
        target_images.append(target_image) # save to list
    return target_images
 
    
def Iterative_GS(target_image, iterations, cell_spacing, target_dist, res, k):
    apsize = target_image.shape
    n = apsize[0]
    N = 3*n
    pw = padwidth(N, np.zeros(apsize))
    padded_target = np.pad(target_image, pw, 'constant', constant_values = 0) # Pad with zeros 
    aperture = np.ones(apsize)
    padded_aperture = np.pad(aperture, pw, 'constant', constant_values = 0)
    tpp = padded_target*np.exp(1j*padded_target*np.pi) # initial pressure at target plane
    for it in range(iterations):
        lpp = ASM_bw(tpp, cell_spacing, target_dist, k) # inverse ASM to backpropagate complex pressure to lens-plane
        lpp = padded_aperture*np.exp(1j*np.angle(lpp)*padded_aperture) # isolate over aperture
        tpp = ASM_fw(lpp, cell_spacing, target_dist, res, k) # forward ASM to propagate updated phase as complex pressure to the target-plane
        tpp = padded_target*np.exp(1j*np.angle(tpp)*padded_target) # isolate target area
    lpp = ASM_bw(tpp, cell_spacing, target_dist, k)
    lpp = padded_aperture*np.exp(1j*np.angle(lpp)*padded_aperture) # isolate
    tpp = ASM_fw(lpp, cell_spacing, target_dist, res, k)
    return np.angle(lpp)[pw[0][0]:pw[0][0] + apsize[0], pw[1][0]:pw[1][0] + apsize[1]]


def PMP_Iterative_GS(target_image, incident_surface_pressure, iterations, cell_spacing, target_dist, k):
    apsize = target_image.shape
    n = apsize[0]
    N = 4*n
    pw = padwidth(N, np.zeros(apsize))
    surface_amplitude, surface_phase = abs(incident_surface_pressure), np.angle(incident_surface_pressure)
    aperture = ((surface_amplitude != 0).astype(int))
    
    padded_target = np.pad(target_image, pw, 'constant', constant_values = 0) # Pad with zeros 
    padded_aperture = np.pad(aperture, pw, 'constant', constant_values = 0)
    padded_surface_amplitude = np.pad(surface_amplitude, pw, 'constant', constant_values = 0)
    
    tpp = padded_target*np.exp(1j*padded_target*np.pi) # initial pressure at target plane
    
    for it in range(iterations):
        lpp = ASM_bw(tpp, cell_spacing, target_dist, k) # inverse ASM to backpropagate complex pressure to lens-plane
        lpp = padded_surface_amplitude*np.exp(1j*np.angle(lpp)*padded_aperture) # isolate over aperture
        tpp = ASM_fw(lpp, cell_spacing, target_dist, 1, k) # forward ASM to propagate updated phase as complex pressure to the target-plane
        tpp = padded_target*np.exp(1j*np.angle(tpp)*padded_target) # isolate target area
        
    lpp = ASM_bw(tpp, cell_spacing, target_dist, k)
    lpp = padded_aperture*np.exp(1j*np.angle(lpp)*padded_aperture) # isolate
    tpp = ASM_fw(lpp, cell_spacing, target_dist, 1, k)
    return np.angle(lpp)[pw[0][0]:pw[0][0] + apsize[0], pw[1][0]:pw[1][0] + apsize[1]]
    
# use a rotation matrix to find new x & z-coords for an angled board (y-coords will not change)
def rotate_2d(x_vals, y_vals, theta):
    r = np.array(( (np.cos(np.radians(theta)), -np.sin(np.radians(theta))),
                   (np.sin(np.radians(theta)), np.cos(np.radians(theta))) ))
    v = np.array((x_vals, y_vals))
    return r.dot(v)

# pressure_evaluation_space_builder
def pesb(n, side_length, cell_spacing, angle, x_tcoords, y_tcoords, z_tcoords):
    # rotation matrix, assuming that the board is rotated in the x-z plane.
    x_tcoords, z_tcoords = rotate_2d(x_tcoords, z_tcoords, angle) 
    xx, yy = np.meshgrid(x_tcoords, y_tcoords) # Use meshgrid to create grid versions of x and y coords
    zz = np.array([z_tcoords for i in range(n)]) # create a meshgrid for z without making all of them 3D arrays
    # x, y & z vectors for transducer-plane sample points:
    tx, ty, tz = xx.reshape(n**2), yy.reshape(n**2), zz.reshape(n**2) 
    
    ev = np.arange(-side_length, side_length, cell_spacing) # side length vector for the plane being propagated to
    ex, ey = np.meshgrid(ev,ev)
    # x, y & z vectors for evaluation-plane sample points:
    px, py, pz = ex.reshape(len(ev)**2), ey.reshape(len(ev)**2), np.zeros(len(ev)**2) 
    
    # Grids to describe the vector distances between each transducer & evaluation plane sample point.
    txv, pxv = np.meshgrid(tx,px)
    tyv, pyv = np.meshgrid(ty,py)
    tzv, pzv = np.meshgrid(tz,pz)
    
    rxyz = np.sqrt((txv-pxv)**2 + (tyv-pyv)**2 + (tzv-pzv)**2) # Pythagoras for xyz distances
    rxy = np.sqrt((txv-pxv)**2 + (tyv-pyv)**2) # Pythagoras for xy distances
    return rxyz, rxy

# Transducer piston model
def piston_model_matrix(rxy, rxyz, k, p0=16.04, d=10.5/1000):
    # 1st order Bessel function
    b = k*(d/2)*(rxy/rxyz)
    # taylor expansion of the bessel function
    tay = (1/2)-(b**2/16)+(b**4/384)-(b**6/18432)+(b**8/1474560)-(b**10/176947200)
    return p0*(tay/rxyz)*np.exp(1j*k*rxyz)

def heightmap_builder(wavelength, discretisation, an_phase_map):
    db = [np.round(i, 4) for i in np.arange(-np.pi, np.pi, (2 * np.pi) / discretisation)]
    dis_phase_map = []
    n = an_phase_map.shape[0]
    for phase in np.array(an_phase_map).reshape(n ** 2):  # reshape into n**2-by-1 vector and cycle through elements
        current = db[0]  # dummy variable set to the first discretised brick phase delay value
        for brickID in db[1:]:  # cycle through analogue phase delays
            if np.abs(phase - current) > np.abs(phase - brickID):  # assign closest discrete brick value
                current = brickID  # redefine dummy variable as closest discrete phase delay
        dis_phase_map.append(np.round(current, 4))  # discretised phase-delay map for each element
    dis_phase_map = np.array(dis_phase_map).reshape((n, n))  # reshape by into n-by-n matrix
    normalised_phasemap = (dis_phase_map + np.round(np.pi, 4)) / (2 * np.round(np.pi, 4))  # normalise between 0 and 1
    phase_delay_map = 1 - normalised_phasemap  # delays phase values are 1 - phase on the surface
    height_map = phase_delay_map * (wavelength / 2)  # convert to height between 0 and wavelength/2 (meters)
    return height_map


def naive_pattern_generator(pattern, elem_shape):
    '''
    generate homogeneous naive phasemaps for a given pattern by naively combining groups of elements and taking the circular mean.
    '''
    naive_pattern = np.zeros(pattern.shape) 
    for row in range(int(pattern.shape[0]/elem_shape[0])):
        for col in range(int(pattern.shape[0]/elem_shape[1])):
            a1, a2, b1, b2 = row*elem_shape[0], (row+1)*elem_shape[0], col*elem_shape[1], (col+1)*elem_shape[1]
            elem_mean = circular_mean(pattern[a1:a2, b1:b2])
            naive_pattern[a1:a2, b1:b2] = np.tile(elem_mean, (elem_shape[0], elem_shape[1])) 
    return naive_pattern


def circular_mean(phases):
    return np.arctan2(np.sum(np.sin(phases)), np.sum(np.cos(phases)))


def image_splitter(patterns, lenslet_size):
    pattern_lenslets = {}  # initialise dictionary
    pattern_key = 0  # key for each pattern
    for pattern in patterns:
        pattern_lenslets[pattern_key] = []
        lenslet_count = int((patterns[0].shape[0]) / lenslet_size)
        for x in range(lenslet_count):
            for y in range(lenslet_count):
                lenslet = pattern[x * lenslet_size:(x + 1) * lenslet_size, y * lenslet_size:(y + 1) * lenslet_size]
                pattern_lenslets[pattern_key].append(lenslet)
        pattern_key += 1
    return pattern_lenslets


def mse_metric(imageA, imageB):
    err = np.sum((imageA - imageB) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    return err


def ssim_metric(imageA, imageB):
    from skimage.metrics import _structural_similarity as ssim
    s = ssim.structural_similarity(imageA, imageB)
    return s
    
    
def image_fattener(image, fatness):
    for i in range(fatness):
        new_image = image.copy()
        for x in range(1, len(image)-1):
            for y in range(1, len(image)-1):
                if image[x,y] == 0:
                    if image[x, y-1] == 1:
                        new_image[x, y] = 1
                    elif image[x-1, y] == 1:
                        new_image[x, y] = 1
                    elif image[x-1, y-1] == 1:
                        new_image[x, y] = 1
                    elif image[x+1, y-1] == 1:
                        new_image[x, y] = 1
                    elif image[x-1, y+1] == 1:
                        new_image[x, y] = 1
                    elif image[x+1, y+1] == 1:
                        new_image[x, y] = 1
                    elif image[x, y+1] == 1:
                        new_image[x, y] = 1
                    elif image[x+1, y] == 1:
                        new_image[x, y] = 1
        image = new_image
    return image