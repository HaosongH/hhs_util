from file_util import *
from spectral import *
import numpy as np
from spectral.io import envi
from scipy.signal import savgol_filter
# Change HDR file into an image array with 69 bands 

def read_hdr_file(file):
    # return np.array(scipy.signal.savgol_filter(open_image(file).load(),5,2))
    return np.array(open_image(file).load())
