
==========
Quickstart
==========

lidario.Translator_ translate a given data structure (ie: *a raster*), to a point cloud (ie: *a numpy array*).

.. code-block:: python

    import lidario as lio

    # Translate a raster to a numpy point cloud.
    translator = lio.Translator("geotiff", "np")
    point_cloud = translator.translate("/path/to/file.tif")

    # point_cloud: np.array([...])

In this example, we initialize a **Translator** object to convert a geotiff file into a numpy array cloud point. Then, we use this object to effectively convert a tif file.

.. _lidario.Translator: ../api/translator.html