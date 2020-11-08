
import rasterio
import numpy as np


class InputHandler:

    def __init__(self, input_type):
        self.loader = self.__create_loader(input_type)

    def load(self, raster, input_values, band=None):
        """

        :param raster: If True, return a tuple of (raster, metadata).
            If False, return only the metadata.
        """
        return self.loader(raster=raster,
                           input_raster=input_values,
                           rasterio_mask=input_values,
                           band=band)

    def __create_loader(self, input_type):

        loaders = {

            # Tif files
            "tif": self.__load_tif,
            "tiff": self.__load_tif,
            "geotiff": self.__load_tif,

            # Rasterio mask
            "mask": self.__load_rasterio_mask,
        }

        return loaders[input_type]

    @staticmethod
    def __load_tif(raster=True, input_raster=None, band=1, **kwargs):
        """
        Load a tif file with rasterio, return

        :param kwargs: dictionary of keywords arguments. It must have:
            - "file_path" (str): the path of the tif file.
        :type kwargs: dict

        :return: a rasterio DatasetReader object.
        """

        # Open the tiff file
        reader = rasterio.open(input_raster)

        # Get the metadata
        metadata = reader.meta

        # Set -9999 as default if nodata is None
        if metadata['nodata'] is None:
            metadata['nodata'] = -9999

        # If raster, return a tuple of (raster, metadata)
        if raster:
            return reader.read(band), metadata

        return metadata

    @staticmethod
    def __load_rasterio_mask(raster=True, rasterio_mask=None, **kwargs):

        # Retrieve the image and the affine transformation
        out_image, transform = rasterio_mask

        # Create a metadata object
        metadata = {'nodata': -9999, 'transform': transform}

        # If raster, return a tuple of (raster, metadata)
        if raster:
            return np.squeeze(out_image), metadata

        return metadata
