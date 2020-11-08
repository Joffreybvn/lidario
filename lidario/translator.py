
import numpy as np
from lidario.io import InputHandler, OutputHandler


class Translator:
    """
    Instantiate a Translator object which will handle the translation between
    given input and desired output type.

    :param input_type: Type of raster data provided: "**geotiff**" or "**mask**".

        - "geotiff": a .tif raster file.
        - "mask", a *rasterio.mask.mask()* result.

    :param output_type: Type of point cloud data to return: "**csv**",
        "**numpy**", "**pandas**", "**dictionary**", "**list**", "**tuple**".

        - "csv": a CSV file.
        - "numpy": a Numpy array. Alternatives: "np", "array".
        - "dataframe": A Pandas dataframe: Alternatives: "pandas", "pd", "df".
        - "dictionary": A pure Python dictionary: Alternative: "dict".
        - "list" a pure Python list.
        - "tuple": a pure Python tuple.

    :param affine_transform: If True (default), apply an affine
        geo-transformation to the translated coordinates.
    :param metadata: If True, the "translate" method will return a tuple
        with the point cloud and the metadata. If False (default), it will
        only return the point cloud.

    :type input_type: str
    :type output_type: str
    :type affine_transform: bool, optional
    :type metadata: bool, optional
    """

    def __init__(self, input_type, output_type, affine_transform=True, metadata=False):

        # Handle the input and output files/objects
        self.input_handler = InputHandler(input_type)
        self.output_handler = OutputHandler(output_type)

        # True point cloud has to be geo-transformed
        self.affine_transform = affine_transform
        self.return_metadata = metadata

    def translate(self, input_values, out_file="output.csv", no_data=None, decimal=None, transpose=False, band=1):
        """
        Translate a given "input_values" into a X, Y, Z point cloud.

        :param input_values: Data values to translate. Depend on the
            Translator's "input_type" parameter:

            - For a "**geotiff**": Takes the path to your .tif file (string).
            - For a "**mask**": Takes the np.array returned by a rasterio.mask.mask() method.

        :param out_file: Pathname of the CSV file to save the point cloud.
            Used only if the Translator's "output_type" is "csv". Optional,
            default: "output.csv".

        :param no_data: Value to exclude from the translation.

            - For a "**geotiff**": By default, use the nodata value stored in the tif file. If this value is missing, use -9999.
            - For a "**mask**": By default, use -9999.

        :param band: Band of the raster to translate. Used only if Translator's
            "input_values" is "geotiff". Default: 1.
        :param decimal: Round the coordinate numbers to the given decimal.
            Default: None.
        :param transpose: If True, transpose the coordinates. Default: False.

        :type input_values: str or np.array
        :type out_file: str, optional
        :type no_data: int, optional
        :type decimal: int, optional
        :type transpose: bool, optional
        :type band: bool, optional

        :return: The translated point cloud, typed as specified. If
            Translator's "output_type" is set to "csv", return None instead
            and save the CSV file. If Translator's "metadata" is set to True,
            return a tuple with the point cloud and the metadata.
        """

        # Load the raster and metadata
        raster, metadata = self.input_handler.load(True, input_values, band)

        if no_data is None:
            no_data = metadata['nodata']

        # Create a (x, y, z) point cloud from raster data
        x, y, z = self.__create_xyz_points(raster, no_data)

        # Geo-transform the coordinates
        if self.affine_transform:
            x, y = self.__affine_geo_transformation(x, y, metadata['transform'])

        # Round the numbers
        if decimal is not None:
            x, y, z = self.__round(x, y, z, decimal)

        # Save the point cloud
        point_cloud = self.output_handler.save(x, y, z, out_file, transpose)

        # If "self.return_metadata" is True, return the metadata
        if self.return_metadata:
            return point_cloud, metadata

        # If not, return only the point cloud
        return point_cloud

    @staticmethod
    def __create_xyz_points(raster, no_data=-9999):
        """
        Infer x, y, z points from raster data.

        :param raster: Raster data as numpy array.
        :param no_data: No data value of the raster.

        :type raster: np.array
        :type no_data: int

        :return: Tuple of np.array containing the point cloud: (x, y, z).
        :rtype tuple
        """
        y, x = np.where(raster != no_data)
        z = np.extract(raster != no_data, raster)

        return x, y, z

    @staticmethod
    def __affine_geo_transformation(x, y, gtr):
        """
        Create affine geo-transformed x and y.

        An affine transformation preserves collinearity and ratios of
        distances. It replace the point cloud into their original
        space of coordinates.

        :param x: X-array of coordinates.
        :param y: Y-array of coordinates.
        :param gtr: Affine geo-transformation data.

        :return: gtr_x, gtr_y, the geo-transformed x and y, as np.array.
        :rtype tuple
        """

        # https://gdal.org/user/raster_data_model.html#affine-geotransform
        # Affine transformation rewritten for rasterio:
        gtr_x = gtr[2] + (x + 0.5) * gtr[0] + (y + 0.5) * gtr[1]
        gtr_y = gtr[5] + (x + 0.5) * gtr[3] + (y + 0.5) * gtr[4]

        return gtr_x, gtr_y

    @staticmethod
    def __round(x, y, z, decimal):

        return np.around(x, decimal),\
               np.around(y, decimal),\
               np.around(z, decimal)
