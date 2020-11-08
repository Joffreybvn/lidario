
==============
MetadataReader
==============
These examples illustrate how to use lidario.MetadataReader_ to get the metadata of a raster.

Get metadata from tif file
--------------------------

Retrieve the metadata from a raster (**.tif**) file.

.. code-block:: python

    import lidario as lio

    # Instantiate a MetadataReader object which will
    # take a tif file
    reader = lio.MetadataReader("tif")

    # Get the metadata of a given tif file
    metadata = reader.get_metadata("./tests/assets/1.tif")

Get metadata from Rasterio.mask
-------------------------------

Retrieve the metadata from a rasterio.mask_.

.. code-block:: python

    import rasterio
    from rasterio.mask import mask
    import lidario as lio

    # Instantiate a MetadataReader object which will
    # take a rasterio.mask
    reader = lio.MetadataReader("mask")

    # Load a raster and create a polygon shape
    reader = rasterio.open("/path/to/file.tif")
    shape = [{'type': 'Polygon', 'coordinates': [[(0, 0),  (0, 10), (10, 10), (0, 0)]]}]

    # Crop the tif file with the shape
    mask_values = rasterio.mask.mask(reader, shapes=shape, crop=True)

    # Translate the mask_values and get the np.array
    metadata = reader.get_metadata(mask_values)

.. _lidario.MetadataReader: ../api/metadata.html
.. _rasterio.mask: https://rasterio.readthedocs.io/en/latest/api/rasterio.mask.html