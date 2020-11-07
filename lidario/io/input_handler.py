
import rasterio
import numpy as np


class InputHandler:

    def __init__(self, input_type):
        self.loader = self.__create_loader(input_type)

    def load(self, input_values, band):
        return self.loader(input_raster=input_values,
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
    def __load_tif(input_raster=None, band=1, **kwargs):
        """
        Load a tif file with rasterio, return

        :param kwargs: dictionary of keywords arguments. It must have:
            - "file_path" (str): the path of the tif file.
        :type kwargs: dict

        :return: a rasterio DatasetReader object.
        """

        # Open the tiff file
        reader = rasterio.open(input_raster)

        # Get the raster and the metadata
        raster = reader.read(band)
        metadata = reader.meta

        return raster, metadata

    @staticmethod
    def __load_rasterio_mask(rasterio_mask=None, **kwargs):

        # Retrieve the image and the affine transformation
        out_image, transform = rasterio_mask

        # Remove any useless dimension
        raster = np.squeeze(out_image)

        return raster, {'nodata': -9999, 'transform': transform}
