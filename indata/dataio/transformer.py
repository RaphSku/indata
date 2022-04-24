"""Transforms columns of a dataframe with user written callables, such that the user can
manipulate the dataframe straight away"""

import pandas as pd
from abc import abstractmethod
from typing import Callable


import indata.exception.base as exception


#################################################################################################
#                                  Interface Transformer                                        #
#################################################################################################

class IFTransformer:
    """Interface for the Transformer
    The transform method is used on a set of dataframe columns in order to apply
    modifications
    """

    @abstractmethod
    def transform(self): # pragma: no cover
        pass


#################################################################################################
#                                         Transformer                                           #
#################################################################################################

class Transformer(IFTransformer):
    """Transformer which does in-place modification of dataframes according
    to specified transformer properties

    Parameters
    ----------
        columns : list[str]
            Name of the columns which should be modified
        funcs : list[Callable]
            The functions which should be applied on the target columns

    Raises
    ------
        DimError
            Raises when the length of `columns` and `funcs` is not equal
    """

    def __init__(self, columns: list[str], funcs: list[Callable]):
        if len(columns) != len(funcs):
            raise exception.DimError(f"The length of column and funcs has to match!")
        self.columns = columns
        self.funcs   = funcs
        

    def transform(self, dataframe) -> pd.DataFrame:
        """Transforms columns in a dataframe according to user specified callables

        Returns
        -------
        pd.DataFrame
            The in-place modified dataframe
        """
        for index, column in enumerate(self.columns):
            dataframe[column] = self.funcs[index](dataframe[column])

        return dataframe