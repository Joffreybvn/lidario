
import pandas as pd
import numpy as np
from plyfile import PlyData, PlyElement
from typing import Callable, Iterable


class OutputHandler:

    def __init__(self, output_type):
        self.saver: Callable = self.__create_saver(output_type)

    def save(self, x, y, z, out_file, out_format, transpose):
        """
        Execute the save function.
        """
        return self.saver(x, y, z, out_file=out_file, out_format=out_format,
                          transpose=transpose)

    def __create_saver(self, output_type) -> Callable:
        """
        Associate the right saver function to the "save" function of
        this class. This function is executed during the initialization
        phase.

        :param output_type: Type of point cloud to return. See
            "Translator" init() function for more details.
        :type: output_type: str

        :return: The save function associated with the given "output_type".
        """

        savers = {
            # Files
            "csv": self.__save_csv,
            "ply": self.__save_ply,

            # Pandas dataframe
            "dataframe": self.__save_dataframe,
            "pandas": self.__save_dataframe,
            "pd": self.__save_dataframe,
            "df": self.__save_dataframe,

            # Numpy array
            "numpy": self.__save_numpy,
            "np": self.__save_numpy,
            "array": self.__save_numpy,

            # Dictionary
            "dictionary": self.__save_dictionary,
            "dict": self.__save_dictionary,

            # Other Python data structures
            "list": self.__save_list,
            "tuple": self.__save_tuple
        }

        return savers[output_type]

    # File savings
    # -------------------------------------------------------------------------

    def __save_csv(self, x, y, z, transpose=False, out_file="output", **kwargs) -> None:
        """
        Create a CSV file from a given x, y, z point cloud.

        :return: None
        """

        # Create a pandas dataframe and save it to CSV
        out_file += ".csv"
        self.__save_dataframe(x, y, z, transpose).to_csv(out_file, index=False)

    def __save_ply(self, x, y, z, out_file="output", out_format="binary", **kwargs) -> None:
        """
        Create a .ply file from a given x, y, z point cloud.

        :return: None
        """

        def to_tuples(array: np.array) -> Iterable:
            """Return an iterable of tuple frm a given (n, 3) np.array"""
            shape = array.shape[0]

            for i in range(shape):
                yield tuple(array[i])

        # Create a numpy array and set a custom dtype
        raw_array = self.__save_numpy(x, y, z)

        # Transform it with a custom dtype
        np_array = np.fromiter(
            to_tuples(raw_array),
            dtype=[('x', 'f4'), ('y', 'f4'), ('z', 'f4')]
        )

        # Instantiate a PlyElement with the numpy array
        out_file += ".ply"
        ply = PlyElement.describe(np_array, out_file)

        # If out_type is "ascii", write a text file
        if out_format == "ascii":
            PlyData([ply], text=True).write(out_file)

        # Else, write a binary file
        else:
            PlyData([ply]).write(out_file)

    # Python data structure savings
    # -------------------------------------------------------------------------

    def __save_dictionary(self, x, y, z, transpose=False, **kwargs) -> dict:
        """
        Create a dictionary of points, from a previously created
        pandas dataframe. This function can be very slow.

        :return: A dictionary of the point cloud.
        :rtype: dict
        """

        # Return a dictionary of x, y and z
        return self.__save_dataframe(x, y, z, transpose).to_dict()

    def __save_list(self, x, y, z, transpose=False, **kwargs) -> list:
        """
        Create a (n, 3) np.array and convert it into a pure Python list of
        points [x, y, z]. If "transpose" is set to True, return a list of
        len = 3, with all x, y and z values stored separately.

        :return: A list of points [[x, y, z], ...]
        :rtype: list
        """

        # Create a numpy array and transform it into a list
        return self.__save_numpy(x, y, z, transpose).tolist()

    def __save_tuple(self, x, y, z, transpose=False, **kwargs) -> tuple:
        """
        Create a (n, 3) np.array and convert it into a pure Python tuple of
        points (x, y, z). If "transpose" is set to True, return a tuple of
        len = 3, with all x, y and z values stored separately.

        :return: A tuple of points ((x, y, z), ...)
        :rtype: tuple
        """

        # Create a numpy array and transform it into a tuple
        # https://www.geeksforgeeks.org/python-convert-list-of-lists-to-tuple-of-tuples/
        return tuple(map(tuple, self.__save_numpy(x, y, z, transpose)))

    # C-based data structure savings
    # -------------------------------------------------------------------------

    def __save_dataframe(self, x, y, z, transpose=False, **kwargs) -> pd.DataFrame:
        """
        Create a (n, 3) pandas dataframe of the points. By default,
        each point [x, y, z] is written on a new row. If transpose is
        set to True, points are written on columns.

        :return: A pandas dataframe of the point cloud.
        :rtype: pd.DataFrame
        """

        # Get a numpy array of [x, y, z]
        data = self.__save_numpy(x, y, z, transpose)

        # If transpose, set each [x, y, z] point on columns (horizontally)
        if transpose:
            return pd.DataFrame(data=data, index=['x', 'y', 'z'])

        # If not, set each [x, y, z] point on rows (vertically)
        return pd.DataFrame(data=data, columns=['x', 'y', 'z'])

    @staticmethod
    def __save_numpy(x, y, z, transpose=False, **kwargs) -> np.array:
        """
        Create a numpy array of shape (n, 3), filled with x, y and z.
        If "transpose" is set to True, return a numpy array of shape (3, n).

        :return: np.array matrix of shape (n, 3).
        :rtype: np.array
        """

        # Create a numpy array of shape (n, 3) with x, y, z
        np_array = np.column_stack((x, y, z))

        # If True, transpose the array to (3, n)
        if transpose:
            np_array = np.transpose(np_array)

        return np_array
