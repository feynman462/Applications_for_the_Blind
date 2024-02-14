import numpy as np
from scipy.ndimage import gaussian_filter, sobel
from scipy import fftpack
from imsim import imsim

def measure_stars(image, i, j, filter_sigma=2.5):  
    smoothed_image = gaussian_filter(image, sigma=filter_sigma)
    fluxes = [smoothed_image[x, y] for x, y in zip(i, j)]
    return np.array(fluxes)

def denoise_image_fft(image, keep_fraction=0.1):
    im_fft = fftpack.fft2(image)
    r, c = im_fft.shape
    im_fft[int(r*keep_fraction):int(r*(1-keep_fraction))] = 0
    im_fft[:, int(c*keep_fraction):int(c*(1-keep_fraction))] = 0
    im_new = fftpack.ifft2(im_fft).real
    return im_new

def denoise_image_gaussian(image, sigma=4):
    return gaussian_filter(image, sigma)

def apply_sobel_filter(image):
    resx = sobel(image, axis=0, mode='constant')
    resy = sobel(image, axis=1, mode='constant')
    return -np.hypot(resx, resy)

def calibrate_image(image, bias, flat):
    calibrated_image = image.copy()
    calibrated_image -= bias
    calibrated_image /= flat
    return calibrated_image

if _name_ == "_main_":
    image, x, y = imsim()
    fluxes = measure_stars(image, x, y)
    print("I measured", fluxes)  

imsim.py
import numpy as np
from scipy.ndimage import gaussian_filter

def imsim():
    sx,sy = 1024,1024

    # start with read-noise
    im = 10.*np.random.randn(sx,sy)

    m_min,m_max = 9.,20.27
    N = int( (0.25/100.)*( 2*( np.exp(0.5*m_max)-np.exp(0.5*m_min) ) ) )

    cn = np.random.rand(N)
    m = 2*np.log( np.exp(0.5*m_min) + cn*( np.exp(0.5*m_max)-np.exp(0.5*m_min) ) )

    x = 10+(np.random.rand(N)*(sx-20)).astype('int16')
    y = 10+(np.random.rand(N)*(sy-20)).astype('int16')
    cts = 10*np.sqrt(1.1e3)*10**(-0.4*(m-m_max))*np.sqrt(4*np.pi)*2

    im_s = np.zeros((sx,sy),dtype='float32')
    for i in range(N):
        im_s[x[i],y[i]] += cts[i]

    return gaussian_filter(im_s,2.) + np.sqrt(im_s+1.e3)*np.random.ra