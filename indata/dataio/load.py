"""
DataSet and DataLoader are used to define the data source
and to load the data such that it can be ingested by upstream
classes.
"""

import os
import attrs
import pandas as pd

from abc     import abstractmethod
from pathlib import Path

import indata.dataio.transformer as transform
import indata.exception.base     as exception


#################################################################################################
#                                         DataSet                                               #
#################################################################################################

attrs.define()
class DataSet:
    """
    DataSet stores the metadata about the target file
    """
    path_to_file: Path = attrs.field(factory = Path)

    def __init__(self, path_to_file: Path):
        """
        Parameters
        ---------   
        path_to_file: str
            The `path` to the target file

        Raises
        ------
        PathNotFoundError
            Raised when the path of the the target file does not exists!
        """
        if not os.path.exists(path_to_file):
            raise exception.PathNotFoundError("Given path to file does not exists! Please check it again.")
        self.path_to_file = path_to_file


#################################################################################################
#                                      Interface DataLoader                                     #
#################################################################################################

class IFDataLoader:
    """
    Interface for DataLoader
    
    Methods
    -------
    read_csv()
        Reads the csv file
    """

    @abstractmethod
    def read_csv(self): # pragma: no cover
        pass


#################################################################################################
#                                         DataLoader                                            #
#################################################################################################

@attrs.define()
class DataLoader(IFDataLoader):
    """
    DataLoader is responsible for loading the data inside of the target file

    Methods
    -------
    read_csv()
        Reads the csv file
    """
    dataset: DataSet = attrs.field(factory = DataSet)

    def __init__(self, dataset: DataSet):
        """
        Parameters
        ----------
        dataset: DataSet
            Defines the data source from which the file gets loaded
        """
        self.dataset = dataset


    def read_csv(self, sep: str = ",", lineterminator: str = None, transformer: transform.Transformer = None) -> pd.DataFrame:
        """
        Extracts data out of a csv file and returns a pandas dataframe

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