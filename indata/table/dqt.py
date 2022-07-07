"""A dqt is a data quality table which splits an ABT (Analytics Base Table)
into categorical and continuous features which are getting reported on whether
there are missing values, what the minimum and maximum is, what is the mode in
categorical features, etc. It provides insight into the data without the need
to visualize it in the first place"""

import os
import pandas as pd
import numpy as np
from abc import abstractmethod


import indata.dataio.load as load
import indata.utils.checks as checks
import indata.exception.base as exception


#################################################################################################
#                                Interface DataQualityTable                                     #
#################################################################################################

class IFDataQualityTable:
    """Interface for DataQualityTable
    The implementing class needs to implement the method
    create_table since this method is used to generate a DQT
    """

    @abstractmethod
    def create_table(self): # pragma: no cover
        pass


#################################################################################################
#                                    DataQualityTable                                           #
#################################################################################################

class DataQualityTable(IFDataQualityTable):
    """This class will generate a DQT based on the given
    data which is loaded by the DataLoader
    
    Methods
    -------
        print_header_info()
            Prints the features of the data
        create_table(continuous_features: list[str], categorical_features: list[str], store_json_dir: str)
            Creates the DQT, the split into continuous and categorical features bases on the selection of the user,
            e.g. `continuous_features' is a list of feature names which match the name of the column in the data.
            `store_json_dir` is a path to a directory where the table will be stored in json format. 
    """

    def __init__(self, dataloader: load.DataLoader, check_consistency: bool = False):
        """Initializes the DQT instance

        Parameters
        ----------
        dataloader : load.DataLoader
            Is needed in order to load the data as a dataframe
        check_consistency : bool, optional
            If `check_consistency` is True, the DataFrame will be checked for inconsistencies, otherwise the program
            will continue without checking its consistency, the default is set to False
        """
        self.dataframe = self.__check_schema(dataloader.read_csv(), check_consistency)


    def print_header_infos(self) -> None:
        """ Prints the column names of the dataframe and the types of the columns """
        columns    = self.dataframe.columns
        for index in range(len(self.dataframe.loc[0])):
            print(f"{columns[index]}:", type(self.dataframe.loc[0][index]))


    def create_table(self, continuous_features: list[str], categorical_features: list[str], store_json_dir: str) -> tuple[pd.DataFrame, pd.DataFrame]:
        """Creates the DQT and stores it as a json file, two json files
        be generated, one for the continous features and one for the categorical
        features

        Parameters
        ----------
        continuous_features : list[str]
            The list elements should match the name of the respective column name in the dataframe, based on that, 
            the continuous DQT will be generated for those features
        categorical_features : list[str]
            The list elements should match the name of the respective column name in the dataframe, based on that, 
            the categorical DQT will be generated for those features
        store_json_dir : str
            Path to a directory in which the two json files are stored

        Returns
        -------
        tuple[pd.DataFrame, pd.DataFrame]
            Two dataframes which represent the two DQTs are returned, the first
            return argument is the DQT for continuous features, the second one
            for categorical features
        """
        # continuous data
        dqt_cont = None
        if continuous_features:
            data_frame_cont = self.dataframe[continuous_features]
            dqt_cont        = self.__create_continuous_dqt(data_frame_cont = data_frame_cont, continuous_features = continuous_features)
            print("The DQT for the continuous features is:", dqt_cont.head(10))

        # categorical data
        dqt_catg = None
        if categorical_features:
            data_frame_catg = self.dataframe[categorical_features]
            dqt_catg        = self.__create_categorical_dqt(data_frame_catg = data_frame_catg, categorical_features = categorical_features)
            print("The DQT for the categorical features is:", dqt_catg.head(10))

        if not os.path.exists(store_json_dir):
            os.mkdir(store_json_dir) # pragma: no cover

        if continuous_features:
            dqt_cont.to_json(f'{store_json_dir}/dqt_cont.json')
        if categorical_features:
            dqt_catg.to_json(f'{store_json_dir}/dqt_catg.json')

        return dqt_cont, dqt_catg


    def __create_continuous_dqt(self, data_frame_cont: pd.DataFrame, continuous_features: list[str]) -> pd.DataFrame:
        """Creates the DQT for the continuous features

        Parameters
        ----------
        data_frame_cont : pd.DataFrame
            The respective subset of the original dataframe which contains
            only the continuous features
        continuous_features : list[str]
            The list of names of the continuous features

        Returns
        -------
        pd.DataFrame
            The DQT for continuous features
        """
        number_of_rows = len(data_frame_cont.index)
        counts         = data_frame_cont.count().to_dict()
        missing_values = data_frame_cont.isnull().sum() * 100 / number_of_rows
        missing_values = missing_values.to_dict()
        cardinality    = data_frame_cont.nunique(axis = 0).to_dict()
        minima         = data_frame_cont.min(axis = 0).to_dict()
        first_quantile = data_frame_cont.quantile(0.25).to_dict()
        mean           = data_frame_cont.mean(axis = 0).to_dict()
        median         = data_frame_cont.median(axis = 0).to_dict()
        third_quantile = data_frame_cont.quantile(0.75).to_dict()
        maxima         = data_frame_cont.max(axis = 0).to_dict()
        standard_dev   = data_frame_cont.std(axis = 0).to_dict()

        data_dict      = {'Count': counts.values(), 'Miss. %': missing_values.values(), 'Card.': cardinality.values(),
                          'Min': minima.values(), '1st Qrt.': first_quantile.values(), 'mean': mean.values(), 'median': median.values(),
                          '3rd Qrt.': third_quantile.values(), 'Max': maxima.values(), 'Std. Dev.': standard_dev.values()}

        return pd.DataFrame(data = data_dict, index = continuous_features)


    def __create_categorical_dqt(self, data_frame_catg: pd.DataFrame, categorical_features: list[str]) -> pd.DataFrame:
        """Creates the DQT for categorical features

        Parameters
        ----------
        data_frame_catg : pd.DataFrame
            Dataframe which only contains the categorical features
        categorical_features : list[str]
            The names of the categorical features

        Returns
        -------
        pd.DataFrame
            The DQT with the categorical features
        """
        number_of_rows = len(data_frame_catg.index)
        counts         = data_frame_catg.count().to_dict()
        missing_values = data_frame_catg.isnull().sum() * 100 / number_of_rows
        missing_values = missing_values.to_dict()
        cardinality    = data_frame_catg.nunique(axis = 0).to_dict()

        mode           = {}
        mode_freq      = {}
        mode_rel_freq  = {}
        for column in data_frame_catg.columns:
            mode[column]          = data_frame_catg[column].value_counts().index.to_list()[0]
            mode_freq[column]     = data_frame_catg[column].value_counts().iloc[0]
            mode_rel_freq[column] = data_frame_catg[column].value_counts().iloc[0] * 100 / counts[column]

        second_mode          = {}
        second_mode_freq     = {}
        second_mode_rel_freq = {}
        for column in data_frame_catg.columns:
            second_mode[column]          = data_frame_catg[column].value_counts().index.to_list()[1]
            second_mode_freq[column]     = data_frame_catg[column].value_counts().iloc[1]
            second_mode_rel_freq[column] = data_frame_catg[column].value_counts().iloc[1] * 100 / counts[column]

        data_dict = {'Count': counts.values(), 'Miss. %': missing_values.values(), 'Card.': cardinality.values(),
                     'Mode': mode, 'Mode Freq.': mode_freq, 'Mode Freq. %': mode_rel_freq,
                     '2nd Mode': second_mode, '2nd Mode Freq.': second_mode_freq, '2nd Mode Freq. %': second_mode_rel_freq}

        return pd.DataFrame(data = data_dict, index = categorical_features)


    def __check_schema(self, dataframe: pd.DataFrame, check_consistency: bool) -> pd.DataFrame:
        """Checks whether the data is consistent or not with its schema, the schema
        is inferred based on the datatype of the zero-indexed element

        Parameters
        ----------
        dataframe : pd.DataFrame
            DataFrame which needs to be checked whether it is consistent or not
        check_consistency : bool, optional
            If `check_consistency` is True, the DataFrame will be checked for inconsistencies, otherwise the program
            will continue without checking its consistency, the default is set to False

        Returns
        -------
        pd.DataFrame
            A consistent DataFrame is returned when there are no conflicts

        Raises
        ------
            InconsistentData
                When the Data is inconsistent, this error will be raised
            InconsistentDataTypes
                When the data types of each column in a dataframe is not equal, this error
                will be raised
        """

        if check_consistency:
            target_dataframe = dataframe.copy(deep = True)
            target_dataframe.replace(' ', np.nan)

            rows_with_nan_values = target_dataframe[target_dataframe.isna().any(axis = 1)]
            if len(rows_with_nan_values) != 0:
                raise exception.InconsistentData(f"Data seems to be inconsistent!\nThe following rows contain either NaN or missing values:\n{rows_with_nan_values.to_markdown()}")

            for column in dataframe.columns:
                target_dataframe[column] = target_dataframe[column].apply(lambda x: float(x) if checks.isNumeric(x) else x)
                present_data_types       = target_dataframe[column].apply(lambda x: type(x)).unique()
                if len(present_data_types) > 1:
                    inferred_type = type(target_dataframe[column].iloc[0])
                    if np.issubdtype(inferred_type, np.integer):
                        inferred_type = np.integer
                    corrupted_indices = target_dataframe[column][target_dataframe[column].apply(lambda x: not np.issubdtype(type(x), inferred_type))].index.to_list()
                    raise exception.InconsistentDataTypes(f"Column {column} contains multiple data types and is thus inconsistent, it contains the following\
                                                            data types: {present_data_types}! Watch out for the following lines which might cause this inconsistency:\
                                                            {corrupted_indices}")

        return dataframe