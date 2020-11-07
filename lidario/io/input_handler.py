
import rasterio


class InputHandler:

    def __init__(self, input_type):
        self.loader = self.__create_loader(input_type)

    def load(self, input_raster, band):
        return self.loader(input_raster, band)

    def __create_loader(self, input_type):

        loaders = {
            "tif": self.__load_tif,
            "tiff": self.__load_tif,
            "geotiff": self.__load_tif
        }

        return loaders[input_type]

    @staticmethod
    def __load_tif(*args):
        """
        Load a tif file with rasterio, return

        :param kwargs: dictionary of keywords arguments. It must have:
            - "file_path" (str): the path of the tif file.
        :type kwargs: dict

        :return: a rasterio DatasetReader object.
        """
        file_path = args[0]
        band = args[1]

        # Open the tiff file
        reader = rasterio.open(file_path)

        # Get the raster and the metadata
        raster = reader.read(band)
        metadata = reader.meta

        return raster, metadata
