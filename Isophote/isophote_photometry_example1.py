#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 09:38:20 2023

@author: ruby
"""

import astropy
from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np

path = "/Users/ruby/Documents/Python Scripts/Filters/HighRes/"
hdu = fits.open(path+"F115W/47.fits")[0]
data_img = hdu.data


fig = plt.figure(figsize=(12,5))
plt.imshow(data_img)
plt.axis("off")
plt.show()

from photutils.isophote import Ellipse

ellipse = Ellipse(data_img)
isolist = ellipse.fit_image()
isolist.to_table()
print(type(isolist))

#%%
isophote = ellipse.fit_isophote(sma=20.)
isophote.to_table()
type(isophote)

from photutils.isophote import EllipseGeometry

# define the geometry parameters here
x0 = 45.    # center position
y0 = 45.    # center position
sma = 20.   # semimajor axis length in pixels
eps = 0.2   # ellipticity

# position angle is defined in radians, counterclockwise from the x-axis
# (rotating towards the y-axis).
pa = 35./180. * np.pi # use 35 degrees as a first guess

g = EllipseGeometry(x0, y0, sma, eps, pa)

# custom geometry is passed to the ellipse constructor
ellipse = Ellipse(data_img, geometry=g)

# make the fit
isophote = ellipse.fit_isophote(sma=20.)
print(isophote)

#%%
from photutils.isophote import EllipseSample, EllipseFitter

sample = EllipseSample(data_img, 7., geometry=g)
fitter = EllipseFitter(sample)
isophote = fitter.fit()
print(isophote)

isophote.sample.values.shape

# angles in radians
isophote.sample.values[0]
# polar radii in pixels
isophote.sample.values[1]
# intensities
isophote.sample.values[2]

#%%
plt.rcParams['image.origin'] = 'lower'


plt.figure(figsize=(8, 4))
plt.scatter(isolist.sma**0.25, -2.5*np.log10(isolist.intens))
plt.title('Brightness Profile')
plt.xlabel('sma')
plt.ylabel('Magnitude')
plt.gca().invert_yaxis()

#%%
plt.figure(figsize=(10, 5))
plt.figure(1)

plt.subplot(221)
plt.errorbar(isolist.sma, isolist.eps, yerr=isolist.ellip_err, fmt='o', markersize=4)
plt.xlabel('Semimajor axis length')
plt.ylabel('Ellipticity')

plt.subplot(222)
plt.errorbar(isolist.sma, isolist.pa/np.pi*180., yerr=isolist.pa_err/np.pi*80., fmt='o', markersize=4)
plt.xlabel('Semimajor axis length')
plt.ylabel('PA (deg)')

plt.subplot(223)
plt.errorbar(isolist.sma, isolist.x0, yerr=isolist.x0_err, fmt='o', markersize=4)
plt.xlabel('Semimajor axis length')
plt.ylabel('X0')

plt.subplot(224)
plt.errorbar(isolist.sma, isolist.y0, yerr=isolist.y0_err, fmt='o', markersize=4)
plt.xlabel('Semimajor axis length')
plt.ylabel('Y0')

plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.35, wspace=0.35)

#%%
fig, ax = plt.subplots(figsize=(8, 8))
ax.imshow(data_img)

# this method on an IsophoteList instance will retrieve the isophote
# that has the closest 'sma' from the passed argument
iso = isolist.get_closest(40.)
print('Closest SMA = {:f}'.format(iso.sma))

# this method on an Isophote instance returns the (x, y)-coordinates
# of the sampled points in the image
x, y = iso.sampled_coordinates()
plt.plot(x, y, color='white')

#%%
plt.figure(figsize=(10, 3))
plt.plot(iso.sample.values[0]/np.pi*180., iso.sample.values[2])
plt.ylabel('Intensity')
plt.xlabel('Angle (deg)')
plt.show()
           










