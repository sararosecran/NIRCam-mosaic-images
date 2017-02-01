#SEP test for F090W filter
import numpy as np
import sep
from astropy.io import fits
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from sorting_routines import sorted_reverse_index

def write_file(filename, sort_ob, sort_x, sort_y):
	print(len(sort_x))
	with open(filename, 'w') as f:
		for i in range(len(sort_x)):
			string = str(sort_x[i]) + "\t" + str(sort_y[i]) + "\t" + str(sort_ob[i]) + "\n"
			f.write(string)

#imports fits and puts into numpy array, also gives zero point
def load_fits(filename):
	hdu_list = fits.open(filename, do_not_scale_image_data=True)
	tbdat = hdu_list[0].data
	tbdat = tbdat.byteswap().newbyteorder()
	zero_point = hdu_list[0].header['ABMAG']
	return tbdat, zero_point


#subtracts background from image
def subtraction(tbdat):
	bkg_rms = bkg.rms()	#background noise as 2d array
	tbdat_sub = tbdat - bkg #subtract background
	return tbdat_sub

#perform the extraction
def extraction(tbdat_sub, bkg):
	objects = sep.extract(tbdat_sub, sigma = 5.0, err = bkg.globalrms)
	return objects

#
def kron_info(objects, tbdat_sub):
	kronrad, kronflag = sep.kron_radius(tbdat_sub, objects['x'], objects['y'], objects['a'], objects['b'], objects['theta'], r=6.0)
	return kronrad, kronflag


#Finds flux, flux error, and extraction flags
def find_flux(tbdat_sub, objects, kronrad, kronflag):
	flux, fluxerr, flag = sep.sum_ellipse(tbdat_sub, objects['x'], objects['y'], objects['a'], objects['b'], objects['theta'], pho_auto_A = (2.5*kronrad), err = bkg.globalrms, subpix=1)
	flag |=kronflag #combines all flags
	r_min = 1.75 #minimum diameter = 3.5
	use_circle = kronrad * np.sqrt(a * b) < r_min
	cflux, cfluxerr, cflag = sep.sum_circle(tbdat_sub, objects['x'][use_circle], objects['y'][use_circle], r_min, subpix=1)
	flux[use_circle] = cflux
	fluxerr[use_circle] = cfluxerr
	flag[use_circle] = cflag
	r, rflag = sep.flux_radius(data, x, y, 6.0*objects['a'], rmax = 0.5, normflux = flux, subpix =5)
	sig = 2.0 / (2.35*r) # r from sep.flux_radius() above, with fluxfrac = 0.5
	xwin, ywin, wflag = sep.winpos(tbdat_sub, objects['x'], objects['y'], sig)
	return flux, fluxerr, flag, r, xwin, ywin

#convert extraction flux to magnitude
def magnitude(flux, zero_point):
	-2.5*np.log10(flux) + zero_point

#read in cat and put cat into arrays
def read_cat(filename):
	f = open(filename, "r")
	line = f.readlines()
	f.close()
	num_cat = np.array([])
	ra_cat = np.array([])
	dec_cat = np.array([])
	mag_cat = np.array([])
	z_cat = np.array([])
	s_cat = np.array([])
	for i in range(len(line)):
		num_cat = np.append(num_cat, int(line[i].split()[0]))
		ra_cat = np.append(ra_cat, float(line[i].split()[1]))
		dec_cat = np.append(dec_cat, float(line[i].split()[2]))
		mag_cat = np.append(mag_cat, float(line[i].split()[3]))
		z_cat = np.append(z_cat, float(line[i].split()[4]))
		s_cat = np.append(s_cat, float(line[i].split()[9]))
	return num_cat, ra_cat, dec_cat, mag_cat, z_cat, s_cat

#convert ra and dec from exposures to pixel location
def world_exp(filename, objects):
	hdu_list = fits.open(filename)
	w = wcs.WCS(hdu_list[0].header)
	hdu_list.close()
    wrd = w.wcs_pix2world(objects['x'], objects['y'], np.zeros(len(objects['x'])), 0) #double check this!!!!!
	ra = wrd[][0]
    dec = wrd[][1]
	return ra, dec






#fname = raw_input('Fits filename? ')
#tbdat, zero_point = load_fits(fname)
#bkg = sep.Background(tbdat) #measures background
#tbdat_sub = subtraction(tbdat, bkg)
#objects = extraction(tbdat_sub, bkg)
#print('number of sources', len(objects['x']))
#kronrad, kronflag = kron_info(objects, tbdat_sub)
#flux, fluxerr, flag, r, xwin, ywin= find_flux(tbdat_sub, objects, kronrad, kronflag,)
#mag = magnitude(flux, zp)
num_cat, ra_cat, dec_cat, mag_cat, z, s = read_cat('candels_with_fake_mag.cat')
ra, dec = world_exp(fname, objects)









#write_file("sep_extraction_1.5sig.txt", sort_ob, sort_x, sort_y)





#prints souces in flux decreasing order with corresponding x & y coordinates (highest 500 flux)
print("flux, x, y")
index = sorted_reverse_index(flux)
for j in range(500):
	k = index[j]
	print flux[k], "\t", objects['x'][k], "\t", objects['y'][k]


#plot ellipses around sources
fig, ax = plt.subplots()
m = np.mean(tbdat_sub)
s = np.std(tbdat_sub)
plt.imshow(tbdat_sub, interpolation = 'nearest', cmap = 'gray', origin = 'upper', vmin =0.096707389 , vmax =0.20136729)

for i in range(len(objects)):
	e = Ellipse(xy=(objects['x'][i], objects['y'][i]), width = 6*objects['a'][i], height = 6*objects['b'][i], angle = objects['theta'][i]*180.0/np.pi)
	e.set_facecolor('none')
	e.set_edgecolor('red')
	ax.add_artist(e) #google this....

#plt.show()