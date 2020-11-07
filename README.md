# Lidario

[![Generic badge](https://img.shields.io/badge/python-2.7%20%7C%203.6%20%7C%203.7%20%7C%203.8%20%7C%203.9-blue)](https://www.python.org/downloads/release/python-380/)

High-level python utilities to manipulate LIDAR raster and point cloud.


### Installing
Install and update using pip:

```Shell
pip install lidario
```

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

## About the author
**Joffrey Bienvenu**, Machine Learning student @ [Becode](https://becode.org/).
 - Website: https://joffreybvn.be
 - Github: https://github.com/Joffreybvn 