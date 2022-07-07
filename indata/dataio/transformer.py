"""Transforms columns of a dataframe with user written callables, such that the user can
manipulate the dataframe straight away"""

import copy
import pandas as pd
from abc import abstractmethod
from typing import Any, Callable
from inspect import signature


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

    Methods
    -------
        transform(dataframe: pd.DataFrame)
            Applied on a column of a parent dataframe which should be modified
            with a callable
    """

    def __init__(self, columns: list[str], funcs: list[Callable], args: list[tuple] = None):
        """Initalises the Transformer

        Parameters
        ----------
        columns : list[str]
            Names of the columns which should be modified
        funcs : list[Callable]
            Functions which are applied on individual columns
        args : list[tuple], optional
            Arguments which will be given to the functions if they need additional arguments, by default None

        Raises
        ------
        exception.DimError
            Raised when the length of `columns` is not equal to the length of `funcs` since
            i-th func will be applied on the i-th column
        """
        if len(columns) != len(funcs):
            raise exception.DimError(f"The length of column and funcs has to match!")
        self.columns = columns
        self.funcs   = funcs
        self.args    = args
        

    def transform(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """Transforms columns in a dataframe according to user specified callables

        Returns
        -------
        pd.DataFrame
            The in-place modified dataframe
        """
        if self.args != None:
            arguments = copy.deepcopy(self.args)
            for index, column in enumerate(self.columns):
                sig                 = signature(self.funcs[index])
                number_of_arguments = len(sig.parameters)
                if number_of_arguments != 1:
                    dataframe[column] = self.funcs[index](dataframe[column], *arguments[0])
                    arguments.pop(0)
                    continue
                dataframe[column] = self.funcs[index](dataframe[column])
            
            return dataframe

        for index, column in enumerate(self.columns):
            dataframe[column] = self.funcs[index](dataframe[column])

        return dataframe


#################################################################################################
#                              Useful Transformer Callables                                     #
#################################################################################################

def impute_mode(x: pd.DataFrame) -> pd.DataFrame:
    """ Imputes the missing values with the mode """
    mode = x.mode().iloc[0]

    return x.fillna(mode)


def impute_mean(x: pd.DataFrame) -> pd.DataFrame:
    """ Imputes the missing values with the mean """
    mean = x.mean()

    return x.fillna(mean)


def impute_median(x: pd.DataFrame) -> pd.DataFrame:
    """ Imputes the missing values with the median """
    median = x.median()

    return x.fillna(median)


def replace_entries(x: pd.DataFrame, target_entry: Any, replace_value: Any):
    """ Replaces target entries with the choosen `replace_value` """
    return x.apply(lambda y: replace_value if y == target_entry else y)