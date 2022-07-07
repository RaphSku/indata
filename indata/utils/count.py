"""All counting tools which are utility tools are defined
in this module
"""

import numpy as np
from typing import Tuple


import indata.exception.base as exception


#################################################################################################
#                                    CategoriesCounter                                          #
#################################################################################################

class Categories:
    """All counting operations performed on categorical features
    are subsummed in this class
    
    Methods
    -------
        count(data: list)
            `data` should be 1d-array-like and should contain categorical features,
            `count` will count how many features per feature are in `data`
    """
    def __init__(self): # pragma: no cover
        pass


    @staticmethod
    def count(data: list) -> dict[Tuple[int, str], int]:
        """Counts the number of categorical features which are present
        in `data`

        Parameters
        ----------
        data : 1d-array-like
            `data` contains categorical features 

        Returns
        -------
        dict[Tuple[int, str], int]
            A dictionary is returned whose keys are the categorical
            features and its values are the respective count per feature,
            depending whether the categorical features are numeric or strings,
            the output keys will be numeric or string too

        Raises
        ------
            DimError
                If the dimension of `data` is not `1`, this error will be raised
        """
        if isinstance(data, list):
            data = np.array(data)
            if len(data.shape) != 1:
                raise exception.DimError(f"Data needs to be one-dimensional!")

        hash = {}
        for datapoint in data:
            if datapoint in hash:
                hash[datapoint] += 1
                continue
            hash[datapoint] = 1

        return hash