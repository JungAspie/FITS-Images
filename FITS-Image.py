import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline

from astropy.io import fits

from astropy.utils.data import download_file
image_file = download_file("http://data.astropy.org/tutorials/FITS-images/HorseHead.fits", cache=True)

hdu_list = fits.open(image_file)
hdu_list.info()

image_data = hdu_list[0].data

print(type(image_data))
print(image_data.shape)

hdu_list.close()

image_data = fits.getdata(image_file)

print(type(image_data))
print(image_data.shape)

plt.imshow(image_data, cmap="gray")
plt.colorbar()

print("Min:", np.min(image_data))
print("Max:", np.max(image_data))
print("Mean:", np.mean(image_data))
print("Stdev:", np.std(image_data))

print(type(image_data.flatten()))
print(image_data.flatten().shape)

histogram = plt.hist(image_data.flatten(), bins="auto")

from matplotlib.colors import LogNorm

plt.imshow(image_data, cmap="gray", norm=LogNorm())

cbar = plt.colorbar(ticks=[5.e3, 1.e4, 2.e4])
cbar.ax.set_yticklabels(["5,000", "10,000", "20,000"])

base_url = "http://data.astropy.org/tutorials/FITS-images/M13_blue_{0:04d}.fits"

image_list = [download_file(base_url.format(n), cache=True)
             for n in range(1, 5+1)]
image_concat = [fits.getdata(image) for image in image_list]

final_image = np.zeros(shape=image_concat[0].shape)

for image in image_concat:
    final_image += image

image_hist = plt.hist(final_image.flatten(), bins="auto")

plt.imshow(final_image, cmap="gray", vmin=2E3, vmax=3E3)
plt.colorbar()

outfile = "stacked_M13_blue.fits"

hdu = fits.PrimaryHDU(final_image)
hdu.writeto(outfile, overwrite=True)

