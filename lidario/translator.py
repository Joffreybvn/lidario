
import numpy as np
from lidario.io import InputHandler, OutputHandler


class Translator:

    def __init__(self, input_type, output_type, affine_transform=True, metadata=False):
        """
        Create a Translator which will handle the translation between
        different input and output types.

        :param input_type: Type of raster provided. Can be:
            - Geotiff: "tif", "tiff", "geotiff"
        :param output_type: Type of point cloud to return. Can be:
            - CSV file: "csv"
            - Numpy array: "numpy", "np", "array"
            - Pandas dataframe: "pandas", "dataframe", "pd", "df"
            - Python dictionary: "dict", "dictionary"
            - Python list: "list"
            - Python tuple: "tuple"
        :param affine_transform: If set to True, apply an affine
            geo-transformation to the translated coordinates. Default: True.
        :param metadata: If set to True, the "translate" function will return
            the metadata of the translated raster with the point cloud.
            Default: False.

        :type input_type: str
        :type output_type: str
        :type affine_transform: bool
        """

        # Handle the input and output files/objects
        self.input_handler = InputHandler(input_type)
        self.output_handler = OutputHandler(output_type)

        # True point cloud has to be geo-transformed
        self.affine_transform = affine_transform
        self.return_metadata = metadata

    def translate(self, input_raster, out_file="output.csv", band=1, decimal=None, transpose=False):
        """
        Translate supported raster into a X, Y, Z point cloud.

        :param input_raster: Raster to translate.
        :param out_file: Name of the CSV file to save the point cloud.
            Provide only if the Translator's "output_type" is "csv".
            Default: "output.csv".
        :param band: Band of the raster to translate. Provide only if the
            Translator's "input_type" is "tif". Default: 1.
        :param decimal: If provided, round the coordinate numbers to the
            given decimal. Default: None.
        :param transpose: Transpose the coordinates. Default: False.

        :return:
        """

        # Load the raster and metadata
        raster, metadata = self.input_handler.load(input_raster, band)

        # Create a (x, y, z) point cloud from raster data
        x, y, z = self.__create_xyz_points(raster, metadata['nodata'])

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
