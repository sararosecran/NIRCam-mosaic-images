#Finds overlap in exposures. Then creates 100 X 100 pixel location fits files

#ONLY USES EXPOSURE 1-4 AT THE MOMENT

from __future__ import print_function
import matplotlib.pyplot as plt
from astropy.io import fits
import numpy as np

#function reads in file
def read_file(filename):
    try:
        with open(filename, 'r') as file:
            for line in file:
                print(line.rstrip())
    except IOError as e:
        print(e)

fname = raw_input('Fits image name? ')
hdu_list = fits.open(fname)
hdu_list.inf0()

tbdat = hdu_list[0].data
new_size = input('Dimensions of new, smaller fits? ')
tbdat = np.delete(

