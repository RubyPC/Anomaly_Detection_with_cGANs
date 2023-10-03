# Anomaly Detection with cGANs
[![DOI](https://zenodo.org/badge/690453944.svg)](https://zenodo.org/badge/latestdoi/690453944)
This repository contains notebooks for extracting sources from JWST NIRcam imaging data, performing aperture photometry and isophotal photometry and the source code for the cGAN. Each notebook gives a walk through and detailed explanation of how to use the code provided.
\
The data is public domain JWST data as part of the CEERS survey, the [Cosmic Evolution Early Release Survey (CEERS) data realease 0.5](https://ceers.github.io) can be found on the CEERS website [here](https://ceers.github.io/dr05.html). 
\
Data can be downloaded from the above link.

## Data Preparation for the cGAN
After downloading the CEERS DR0.5, the images for each filter are opened for inspection. The images are cropped into two regions from Module A of the NIRcam imaging field. This is covered in:

> Crop_PSF_Match.ipynb

This is followed by matching the PSF of the images to that of the F444W filter by convolving with pre-calculated kernels that can be downloaded from [here](https://www.astro.princeton.edu/~draine/Kernels/Kernels_JWST/Kernels_fits_Files/Hi_Resolution/).

To prepare the data for the cGAN, source detection and extraction is used on the PSF-matched images. To do this, follow:

> Source_Detection_Extraction.ipynb

This will generate files for each waveband with a *'.fits'* extension containing individual galaxy images. The sources are extracted as 90x90 pixel cutouts ready to load into a Dataset folder for the cGAN.

## The Network
<img width="560" alt="image" src="https://github.com/RubyPC/Anomaly_Detection_with_cGANs/assets/106536925/cf6becbd-7dd4-4ae7-87d6-39ab19fa8e7a">

To use the cGAN, follow:

> cGANs_Astro.ipynb

The data fed to the cGAN is loaded from each individual waveband file. An example of file structure is shown below.
\
<img width="472" alt="Dataset-layout" src="https://github.com/RubyPC/cGANs_in_astronomy/assets/106536925/99a173b6-2802-4867-bc4d-2755acb77dfb">

## Results after Training
The cGAN predicts the long wavelength channel of the objects such that we can extract photometry and reliably construct an SED. Below shows examples of results produced by the network, each with residual images showing the difference between the prediction of the cGAN and the ground truth.
![Residual-Prediction](https://github.com/RubyPC/Anomaly_Detection_with_cGANs/assets/106536925/8a39dc67-a245-421b-beec-ad540a8e58ed)
<img width="700" alt="Residual" src="https://github.com/RubyPC/Anomaly_Detection_with_cGANs/assets/106536925/37885644-f52d-442e-a392-83c27a1828d6">

## Some Useful Links
* [JWST User Documentation](https://jwst-docs.stsci.edu/)
* [JWST NIRcam Imaging Information](https://jwst-docs.stsci.edu/jwst-near-infrared-camera)

### References
* [CEERS](https://ceers.github.io)
* [Image-to-Image Translation with conditionl Adversarial Networks](https://doi.org/10.48550/arXiv.1611.07004)
* [Generative Adversarial Networks](https://doi.org/10.48550/arXiv.1406.2661)
