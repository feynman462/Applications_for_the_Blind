

main.py

import numpy as np
from scipy.ndimage import gaussian_filter, label, binary_opening

def imsim():
    sx, sy = 1024, 1024

    im = 10. * np.random.randn(sx, sy)

    m_min, m_max = 9., 20.27
    N = int((0.25 / 100.) * (2 * (np.exp(0.5 * m_max) - np.exp(0.5 * m_min))))

    cn = np.random.rand(N)
    m = 2 * np.log(np.exp(0.5 * m_min) + cn * (np.exp(0.5 * m_max) - np.exp(0.5 * m_min)))

    x = 10 + (np.random.rand(N) * (sx - 20)).astype('int16')
    y = 10 + (np.random.rand(N) * (sy - 20)).astype('int16')
    cts = 10 * np.sqrt(1.1e3) * 10 ** (-0.4 * (m - m_max)) * np.sqrt(4 * np.pi) * 2

    im_s = np.zeros((sx, sy), dtype='float32')
    for i in range(N):
        im_s[x[i], y[i]] += cts[i]

    return gaussian_filter(im_s, 2.) + np.sqrt(im_s + 1.e3) * np.random.randn(sx, sy)


def find_stars(image):
    sigma_value = 1  
    smoothed_image = gaussian_filter(image, sigma=sigma_value)

    local_thresh = 50

    stars = smoothed_image > local_thresh

    struct_elem = np.ones((2, 2))  # Further reduced size
    stars = binary_opening(stars, structure=struct_elem)

    labeled, num_features = label(stars)
    final_i, final_j = [], []

    for feature in range(1, num_features + 1):
        y, x = np.where(labeled == feature)

        if len(x) > 0 and len(y) > 0:
            centroid_x = int(np.mean(x))
            centroid_y = int(np.mean(y))

            x_min = max(centroid_x - 1, 0)
            x_max = min(centroid_x + 2, image.shape[1])
            y_min = max(centroid_y - 1, 0)
            y_max = min(centroid_y + 2, image.shape[0])

            local_max = np.max(smoothed_image[y_min:y_max, x_min:x_max])
            if smoothed_image[centroid_y, centroid_x] >= local_max * 0.7:
                final_i.append(centroid_y)
                final_j.append(centroid_x)

    return np.array(final_i), np.array(final_j)


if _name_ == '_main_':
    image = imsim()
    i, j = find_stars(image)
    print("I found {:d} stars!".format(len(i)))

imsim.py

import numpy as np
from scipy.ndimage import *

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

    return gaussian_filter(im_s,2.) + np.sqrt(im_s+1.e3)*np.ra