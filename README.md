# Lidario

[![Generic badge](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8%20%7C%203.9-blue)](https://www.python.org/downloads/release/python-380/) [![Travis CI](https://travis-ci.com/Joffreybvn/lidario.svg?branch=master)](https://travis-ci.com/github/Joffreybvn/lidario) [![Documentation Status](https://readthedocs.org/projects/lidario/badge/?version=latest)](https://lidario.readthedocs.io/en/latest/?badge=latest)

High-level python library to manipulate LIDAR raster and point cloud.


### Installing
Install and update using pip:

```Shell
pip install lidario
```

Lidario depends on Rasterio, which depend on many other Python and C libraries. In case of problem, please refer to the [Rasterio installation instructions](https://rasterio.readthedocs.io/en/latest/installation.html).

### Quick start

**lidario.Translator** transform a given data structure (ie: *a raster*), to a point cloud (ie: *a numpy array*).

```Python
import lidario as lio

# Translate a raster to a numpy point cloud.
translator = lio.Translator("geotiff", "np")
point_cloud = translator.translate("/path/to/file.tif")

# point_cloud: np.array([...])
```

In this example, we initialize a **Translator** object to convert a *geotiff* file into a *numpy array* cloud point.
Then, we use this object to effectively convert a *tif* file.

### Going further
Transform Rasterio mask and GeoTiff files into numpy array, pandas dataframe, CSV, PLY, and many other format:

Read the [documentation on ReadTheDocs.io](https://lidario.readthedocs.io/).

## About the author
**Joffrey Bienvenu**, Machine Learning student @ [Becode](https://becode.org/).
 - Website: https://joffreybvn.be
 - Twitter: [@joffreybvn](https://twitter.com/Joffreybvn)  
 - Github: https://github.com/Joffreybvn 