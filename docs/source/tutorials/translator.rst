
==========
Translator
==========
These examples illustrate how to use lidario.Translator_ to translate point cloud data.

Tif file to Pandas dataframe
----------------------------

Transform raster (**.tif**) file into a pandas.Dataframe.

.. code-block:: python

    import lidario as lio

    # Instantiate a Translator object which take a tif file
    # and return a dataframe.
    translator = lio.Translator("geotiff", "dataframe")

    # Translate the tif file and get the pandas.Dataframe
    point_cloud = translator.translate("/path/to/file.tif")


Rasterio.mask to Numpy array
----------------------------

Transform a rasterio.mask_ into a Numpy array.

.. code-block:: python

    import rasterio
    from rasterio.mask import mask
    import lidario as lio

    # Instantiate a Translator object which take rasterio.mask
    # and return a numpy array.
    translator = lio.Translator("mask", "numpy")

    # Load a raster and create a polygon shape
    reader = rasterio.open("/path/to/file.tif")
    shape = [{'type': 'Polygon', 'coordinates': [[(0, 0),  (0, 10), (10, 10), (0, 0)]]}]

    # Crop the tif file with the shape
    mask_values = rasterio.mask.mask(reader, shapes=shape, crop=True)

    # Translate the mask_values and get the np.array
    point_cloud = translator.translate(mask_values)

Translate to CSV and get metadata
---------------------------------

Transform a raster (**.tif**) file into a CSV without applying the affine geo-transformation, and get the metadata.

.. code-block:: python

    import lidario as lio

    # Instantiate a Translator object which take a tif file,
    # save the point cloud to a CSV and return the metadata.
    translator = lio.Translator("geotiff", "csv", affine_transform=False, metadata=True)

    # With metadata=True, translator return a tuple with
    # the point cloud and the metadata.
    point_cloud, metadata = translator.translate("/path/to/file.tif")

In this case, the point_cloud is None, because we save the values to a CSV file.



.. _lidario.Translator: ../api/translator.html
.. _rasterio.mask: https://rasterio.readthedocs.io/en/latest/api/rasterio.mask.html