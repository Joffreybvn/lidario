
from lidario.io import InputHandler


class MetadataReader:
    """
    Instantiate a MetadataReader object which will handle the metadata
    retrieval from the given input.

    :param input_type: Type of raster data provided: "**geotiff**" or "**mask**".

        - "geotiff": a .tif raster file.
        - "mask", a *rasterio.mask.mask()* result.

    :type input_type: str
    """

    def __init__(self, input_type):

        # Handle the input of files/objects
        self.input_handler = InputHandler(input_type)

    def get_metadata(self, input_values):
        """
        Retrieve and return the metadata from a given "input_values".

        :param input_values: Data values to translate. Depend on the
            Translator's "input_type" parameter:

            - For a "**geotiff**": Takes the path to your .tif file (string).
            - For a "**mask**": Takes the np.array returned by a rasterio.mask.mask() method.

        :return: A dictionary of the metadata.
        :rtype: dict
        """

        return self.input_handler.load(False, input_values)
