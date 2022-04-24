"""Testing the functionality of DataSet and DataLoader"""

import os
import pytest
import pandas as pd


import indata.dataio.load as load
import indata.dataio.transformer as transform
import indata.exception.base as exception


class TestDataSet:
    @pytest.fixture()
    def setup(self):
        """ Yields the path to the source directory of this testing module """

        yield os.path.abspath(os.path.dirname(__file__))


    def test_initialisation_s01(self, setup):
        """Dataset Initialisation test, if the attributes
        of Dataset are set properly
        """

        """ PREPARATION """
        path    = os.path.join(setup, "test.csv")

        """ EXECUTION """
        dataset = load.DataSet(path_to_file = path)

        """ VERIFICATION """
        assert path == dataset.path_to_file


    def test_initialisation_e01(self):
        """Dataset Initialisation test, if error is raised
        in case user provides an invalid path
        """

        """ EXECUTION & VERIFICATION """
        with pytest.raises(exception.PathNotFoundError):
            dataset = load.DataSet(path_to_file = "./fail.csv")



class TestDataLoader:
    @classmethod
    def setup_class(cls):
        """Class setup for setting the path to the target file and the dataset 
        which will be used by the DataLoader 
        """
        path        = os.path.join(os.path.abspath(os.path.dirname(__file__)), "test.csv")
        cls.dataset = load.DataSet(path_to_file = path)


    def test_initialisation_s01(self):
        """ Test if the attributes of DataLoader are set correctly """

        """ EXECUTION """
        data_loader = load.DataLoader(dataset = self.dataset)
        
        """ VERIFICATION """
        assert self.dataset == data_loader.dataset


    def test_reading_s01(self):
        """ Test if csv file is read correctly by the DataLoader """

        """ PREPARATION """
        data_loader = load.DataLoader(dataset = self.dataset)

        """ EXECUTION """
        data_frame  = data_loader.read_csv()
        expected_df = pd.DataFrame({'Item1': [1, 4], 'Item2': [2, 5], 'Item3': [3, 2]})

        """ VERIFICATION """
        pd.testing.assert_frame_equal(expected_df, data_frame)


    def test_transformer_s01(self):
        """ Test if transformer correctly modifies the dataframe """

        """ PREPARATION """
        def callable_one(x: pd.DataFrame):
            return x.apply(lambda y: 0 if y > 2 else y)

        def callable_two(x: pd.DataFrame):
            return x.apply(lambda y: x.min() if y < 4 else y)

        data_loader = load.DataLoader(dataset = self.dataset)
        transformer = transform.Transformer(columns = ["Item1", "Item3"], funcs = [callable_one, callable_two])

        """ EXECUTION """
        act_data_frame  = data_loader.read_csv(transformer = transformer)

        """ VERIFICATION """
        exp_data_frame  = pd.DataFrame({'Item1': [1, 0], 'Item2': [2, 5], 'Item3': [2, 2]})
        
        pd.testing.assert_frame_equal(act_data_frame, exp_data_frame)