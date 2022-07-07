"""The module load contains the classes of DataSet and
DataLoader which are responsible for the correct loading
of the target file
"""

import os
import pandas as pd
from abc import abstractmethod


import indata.exception.base as exception
import indata.dataio.transformer as transform


#################################################################################################
#                                   Interface DataSet                                           #
#################################################################################################

class IFDataSet:
    """ Interface of DataSet """
    pass


#################################################################################################
#                                         DataSet                                               #
#################################################################################################

class DataSet(IFDataSet):
    """DataSet stores the metadata about the target file
    
    Parameters
    ----------
        path_to_file: str
            The `path` to the target file

    Raises
    ------
        PathNotFoundError
            Raised when the path of the the target file does not exists!
    """

    def __init__(self, path_to_file: str):
        if not os.path.exists(path_to_file):
            raise exception.PathNotFoundError("Given path to file does not exists! Please check it again.")
        self.path_to_file = path_to_file


#################################################################################################
#                                   Interface DataLoader                                        #
#################################################################################################

class IFDataLoader:
    """Interface for DataLoader
    This interface requires the implementing classes to implement a 
    read_csv method
    """

    @abstractmethod
    def read_csv(self): # pragma: no cover
        pass


#################################################################################################
#                                         DataLoader                                            #
#################################################################################################

class DataLoader(IFDataLoader):
    """DataLoader is responsible for loading the data inside of the target file

    Methods
    -------
        read_csv(sep: str = ",", lineterminator: str = None)
            Extracts the data out of a csv file and returns a pandas dataframe
    """

    def __init__(self, dataset: DataSet):
        """The DataSet holds the information about the target file and its needed
        in order to extract the data out of it

        Parameters
        ----------
        dataset : DataSet
            `dataset` contains all the necessary information in order to read
            the target file
        """
        self.dataset = dataset


    def read_csv(self, sep: str = ",", lineterminator: str = None, transformer: transform.Transformer = None) -> pd.DataFrame:
        """Extracts data out of a csv file and returns a pandas dataframe

        Parameters
        ----------
        sep : str, optional
            Seperator which is used for the csv file, by default ","
        lineterminator : str, optional
            Indicates when a line is terminated inside of the csv file, by default None
        transformer : transform.Transformer, optional
            Transforms dataframes in-place depending on specified columns and which callable
            to apply on the column

        Returns
        -------
        pd.DataFrame
            A pandas dataframe
        """
        dataframe = pd.read_csv(self.dataset.path_to_file, sep = sep, lineterminator = lineterminator)
        if isinstance(transformer, transform.Transformer):
            dataframe = transformer.transform(dataframe)

        return dataframe