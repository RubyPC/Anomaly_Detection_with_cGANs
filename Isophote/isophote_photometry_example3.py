#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 08:28:07 2023

@author: ruby
"""

# isophote photometry

# first we have to get a galaxy image as output from the network
import astropy
from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np

path = "/Users/ruby/Documents/Python Scripts/Filters/HighRes/"
hdu = fits.open(path+"F115W/30.fits")[0]
data_img = hdu.data


fig = plt.figure(figsize=(12,5))
plt.imshow(data_img)
plt.axis("off")
plt.show()

from photutils.isophote import Ellipse
ellipse = Ellipse(data_img)
isophote_list = ellipse.fit_image(sclip=2., nclip=3)

# build the model
from photutils.isophote import build_ellipse_model

model_img = build_ellipse_model(data_img.shape, isophote_list, fill=np.mean(data_img[0:10, 0:10]))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 10))
#limits = [128, 384]

ax1.imshow(model_img)
ax1.set_title("Model")
#ax1.set_xlim(limits)
#ax1.set_ylim(limits)
ax2.imshow(data_img)
ax2.set_title("Data")
#ax2.set_xlim(limits)
#ax2.set_ylim(limits)

residual = data_img - model_img

fig, ax = plt.subplots(figsize=(5, 5))
ax.imshow(residual)
ax.set_title("Residual")
#%%
# now with elliptical image
hdu2 = fits.open(path+"F115W/89.fits")[0]
data = hdu2.data
# fig = plt.figure(figsize=(12,5))
# plt.imshow(data)
# plt.axis("off")
# plt.show()

from photutils.isophote import Ellipse, EllipseGeometry, build_ellipse_model

g = EllipseGeometry(530., 511, 10., 0.1, 10./180.*np.pi)
g.find_center(data)
ellipse = Ellipse(data, geometry=g)
isolist = ellipse.fit_image()

fill = np.mean(data[20:120, 20:120])
model_image = build_ellipse_model(data.shape, isolist, fill=fill)
residual = data - model_image

fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(15, 10))
ax1.imshow(data)
ax1.set_title('Data')
ax2.imshow(model_image)
ax2.set_title('Model')
ax3.imshow(residual)
ax3.set_title('Residual')
ax4.imshow(residual)
ax4.set_title('Residual')

# overplot a few isophotes on the residual map
iso1 = isolist.get_closest(10.)
iso2 = isolist.get_closest(40.)
iso3 = isolist.get_closest(100.)

x, y = iso1.sampled_coordinates()
plt.plot(x, y, color='white')
x, y = iso2.sampled_coordinates()
plt.plot(x, y, color='white')
x, y = iso3.sampled_coordinates()
plt.plot(x, y, color='white')

# residual
fig, ax = plt.subplots(figsize=(6, 6))
ax.imshow(residual)

# radial profile
plt.figure(figsize=(8, 4))
plt.scatter(isolist.sma**0.25, -2.5*np.log10(isolist.intens))
plt.title('Brightness Profile')
plt.xlabel('sma**1/4')
plt.ylabel('Magnitude')
plt.gca().invert_yaxis()

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

plt.figure(figsize=(10, 5))
plt.figure(2)
#limits = [0., 100., -0.1, 0.1]

plt.subplot(221)
#plt.axis(limits)
plt.errorbar(isolist.sma, isolist.a3, yerr=isolist.a3_err, fmt='o', markersize=4)
plt.xlabel('Semimajor axis length')
plt.ylabel('A3')

plt.subplot(222)
#plt.axis(limits)
plt.errorbar(isolist.sma, isolist.b3, yerr=isolist.b3_err, fmt='o', markersize=4)
plt.xlabel('Semimajor axis length')
plt.ylabel('B3')

plt.subplot(223)
#plt.axis(limits)
plt.errorbar(isolist.sma, isolist.a4, yerr=isolist.a4_err, fmt='o', markersize=4)
plt.xlabel('Semimajor axis length')
plt.ylabel('A4')

plt.subplot(224)
#plt.axis(limits)
plt.errorbar(isolist.sma, isolist.b4, yerr=isolist.b4_err, fmt='o', markersize=4)
plt.xlabel=('Semimajor axis length')
plt.ylabel('B4')

plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.35, wspace=0.35)

           

























