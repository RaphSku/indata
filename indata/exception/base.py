"""Base Exceptions are listed here which all inherit
from the Exception class and do not modify its behavior
"""

class PathNotFoundError(Exception):
    """Should be raised when a path to a file could not be found
    """
    pass


class DimError(Exception):
    """When the dimension of the input does not match the requirements
    """
    pass


class InconsistentData(Exception):
    """When a DataFrame is inconsistent in regard to its schema
    """
    pass


class InconsistentDataTypes(Exception):
    """When data types do not match with each other, an error is thrown,
    especially when dealing with dataframes
    """
    pass