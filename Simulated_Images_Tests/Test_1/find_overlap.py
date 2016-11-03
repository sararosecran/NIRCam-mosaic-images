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

#function finds x coordinate where exposure is in encompasing box
def translation_x(tbdatx_array,i):
    x = x_low - tbdatx_array[i][0][0]
    return x

#function finds x coordinate where exposure is in encompasing box
def translation_y(tbdaty_array,i):
    y = y_low - tbdaty_array[i][0][0]
    return y

#function creates 100X100 array and writes new fits for x pixel locations
def new_fits_x(fname,x,fwrite):
    hdu_list = fits.open(fname)
    tbdat = hdu_list[0].data
#    print("original tbdat")
#    print(tbdat)
#    print(np.shape(tbdat))
    minimum = x
#    print("minimum")
#    print(minimum)
    
#    print("tbdat in 0,0 reference")
#    print(tbdat + minimum)
    where_delete = np.where(tbdat<(minimum+tbdat))
#    print("where_delete")
#    print(where_delete)
    maximum = 100 + minimum #size of minifits
    tbdat = tbdat.ravel()
#    print(tbdat)
    tbdat_x_crop = []
    tbdat_x_cropr = []
    if(len(where_delete) != 0):
        for i in range(len(tbdat)):
            if (tbdat[i] > (minimum+tbdat[0])) and (tbdat[i] < (maximum+tbdat[0])):
                tbdat_x_crop.append(tbdat[i])
    tbdat_x_crop = np.delete(tbdat_x_crop,list(range(10000,len(tbdat_x_crop))),0)
#    print(len(tbdat_x_crop))
    tbdat_x_crop = np.reshape(tbdat_x_crop,(100,100))
    tbdat_final = np.asarray(tbdat_x_crop) #turns in numpy array
    hdu = fits.PrimaryHDU(tbdat_final)
    hdu.writeto(fwrite)

#function creates 100X100 array and writes new fits for y pixel locations
def new_fits_y(fname,y,fwrite):
    hdu_list = fits.open(fname)
    tbdat = hdu_list[0].data
#    print("original tbdat")
#    print(tbdat)
#    print(np.shape(tbdat))
    minimum = y
#    print("minimum")
#    print(minimum)
#    print("tbdat in 0,0 reference")
#    print(tbdat + minimum)
    where_delete = np.where(tbdat<(minimum+tbdat))
#    print("where_delete")
#    print(where_delete)
    maximum = 100 + minimum #size of minifits
    tbdat = tbdat.ravel()
#    print(tbdat)
    tbdat_y_crop = []
    tbdat_y_cropr = []
    if(len(where_delete) != 0):
        for i in range(len(tbdat)):
            if (tbdat[i] > (minimum+tbdat[0])) and (tbdat[i] < (maximum+tbdat[0])):
                tbdat_y_crop.append(tbdat[i])
    tbdat_y_crop = np.reshape(tbdat_y_crop,(100,2048))
#    print(len(tbdat_y_crop[0]))
    tbdat_y_crop = np.delete(tbdat_y_crop,list(range(100,len(tbdat_y_crop[0]))),1)
#    print(tbdat_y_crop)
#    print(np.shape(tbdat_y_crop))
    tbdat_final = np.asarray(tbdat_y_crop) #turns in numpy array
    hdu = fits.PrimaryHDU(tbdat_final)
    hdu.writeto(fwrite)



#puts all fits into np arrays
hdux_array = ['hdu_list_x1', 'hdu_list_x2', 'hdu_list_x3', 'hdu_list_x4', 'hdu_list_x5', 'hdu_list_x6', 'hdu_list_x7' , 'hdu_list_x8']
hduy_array = ['hdu_list_y1', 'hdu_list_y2', 'hdu_list_y3', 'hdu_list_y4', 'hdu_list_y5', 'hdu_list_y6', 'hdu_list_y7' , 'hdu_list_y8']
filex_array = ['x.01.fits', 'x.02.fits', 'x.03.fits', 'x.04.fits', 'x.05.fits', 'x.06.fits', 'x.07.fits', 'x.08.fits']
filey_array = ['y.01.fits', 'y.02.fits', 'y.03.fits', 'y.04.fits', 'y.05.fits', 'y.06.fits', 'y.07.fits', 'y.08.fits']
tbdatx_array = ['tbdat_x1','tbdat_x2','tbdat_x3','tbdat_x4','tbdat_x5','tbdat_x6','tbdat_x7','tbdat_x8']
tbdaty_array = ['tbdat_y1','tbdat_y2','tbdat_y3','tbdat_y4','tbdat_y5','tbdat_y6','tbdat_y7','tbdat_y8']


for i in range(0,8):
    hdux_array[i] = fits.open(filex_array[i])
    hduy_array[i] = fits.open(filey_array[i])
    tbdatx_array[i] = hdux_array[i][0].data
    tbdaty_array[i] = hduy_array[i][0].data
    print("x[0][0], y[0][0]:", tbdatx_array[i][0][0], tbdaty_array[i][0][0]) #prints x(0) & y(0)


x_low = tbdatx_array[2][0][0]
x_high = tbdatx_array[0][0][0] + 100
y_low = tbdaty_array[3][0][0]
y_high = tbdaty_array[0][0][0] + 100
print("x & y where all exposures exist:",x_low,y_low,) # For 4 exposures this is the corner of the square that all exposure cover.


exp1_adjust = []
exp2_adjust = []
exp3_adjust = []
exp4_adjust = []
exp1_adjust.append(x_low)
exp1_adjust.append(y_low)
exp2_adjust.append(translation_x(tbdatx_array,1))
exp2_adjust.append(translation_y(tbdaty_array,1))
exp3_adjust.append(translation_x(tbdatx_array,2))
exp3_adjust.append(translation_y(tbdaty_array,2))
exp4_adjust.append(translation_x(tbdatx_array,3))
exp4_adjust.append(translation_y(tbdaty_array,3))
print(exp1_adjust,exp2_adjust,exp3_adjust,exp4_adjust) #Pixel location for each exposure where start box encompased by all exposures


fits_string_array_x = []
fits_write_array_x = []
for k in range(1,5):
    fits_string_x = "x.0" + str(k) + ".fits"
    fits_string_array_x.append(fits_string_x) #creates array of all original pixel x locations filenames
    fits_write_string_x = "x.0" + str(k) + "_100.fits"
    fits_write_array_x.append(fits_write_string_x) #creates array of new pixel x locations filenames
fits_string_array_y = []
fits_write_array_y = []
for k in range(1,5):
    fits_string_y = "y.0" + str(k) + ".fits"
    fits_string_array_y.append(fits_string_y) #creates array of all original pixel y locations filenames
    fits_write_string_y = "y.0" + str(k) + "_100.fits"
    fits_write_array_y.append(fits_write_string_y) #creates array of new pixel y locations filenames
x_array = [exp1_adjust[0],exp2_adjust[0],exp3_adjust[0],exp4_adjust[0]]
y_array = [exp1_adjust[1],exp2_adjust[1],exp3_adjust[1],exp4_adjust[1]]
all_x_pixels = []
all_y_pixels = []
for j in range(0,4):
    fname_x = fits_string_array_x[j]
    fwrite_x = fits_write_array_x[j]
    fname_y = fits_string_array_y[j]
    fwrite_y = fits_write_array_y[j]
    x = x_array[j]
    y = y_array[j]
    new_fits_x(fname_x,x,fwrite_x) #writes new 100 X 100 fits and starts pixel output locations
    new_fits_y(fname_y,y,fwrite_y) #writes new 100 X 100 fits and starts pixel output locations)


hdu_list1 = fits.open('x.01_100.fits')
tbdat1 = hdu_list1[0].data
tbdat1 = tbdat1.flatten()
hdu_list2 = fits.open('x.02_100.fits')
tbdat2 = hdu_list2[0].data
tbdat2 = tbdat2.flatten()
hdu_list3 = fits.open('x.03_100.fits')
tbdat3 = hdu_list3[0].data
tbdat3 = tbdat3.flatten()
hdu_list4 = fits.open('x.04_100.fits')
tbdat4 = hdu_list4[0].data
tbdat4 = tbdat4.flatten()
print(tbdat1)

tbdat_12 = np.append(tbdat1,tbdat2)
tbdat_123 = np.append(tbdat12,tbdat3)
tbdat_1234 = np.append(tbdat123,tbdat4)
tbdat_1234 = np.sort(tbdat1234)
print(tbdat_1234)
print(len(tbdat_1234))

tbdat_final = np.reshape(tbdat_1234,(200,200))
tbdat_final = np.rot90(tbdat_final)

print(tbdat_final)
fname = 'x_out_100.fits'
hdu = fits.PrimaryHDU(tbdat_final)
hdu.writeto(fname)

hdu_list1 = fits.open('y.01_100.fits')
tbdat1 = hdu_list1[0].data
tbdat1 = tbdat1.flatten()
hdu_list2 = fits.open('y.02_100.fits')
tbdat2 = hdu_list2[0].data
tbdat2 = tbdat2.flatten()
hdu_list3 = fits.open('y.03_100.fits')
tbdat3 = hdu_list3[0].data
tbdat3 = tbdat3.flatten()
hdu_list4 = fits.open('y.04_100.fits')
tbdat4 = hdu_list4[0].data
tbdat4 = tbdat4.flatten()
print(tbdat1)

tbdat_12 = np.append(tbdat1,tbdat2)
tbdat_123 = np.append(tbdat12,tbdat3)
tbdat_1234 = np.append(tbdat123,tbdat4)
tbdat_1234 = np.sort(tbdat1234)
print(tbdat_1234)
print(len(tbdat_1234))

tbdat_final = np.reshape(tbdat_1234,(200,200))

print(tbdat_final)
fname = 'y_out_100.fits'
hdu = fits.PrimaryHDU(tbdat_final)
hdu.writeto(fname)
