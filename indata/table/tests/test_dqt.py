"""Testing the generation of the data quality table"""

import os
import sys
import pytest
import unittest
import pandas as pd
from io import StringIO


import indata.exception.base as exception
import indata.dataio.load as load
import indata.table.dqt as dqt


class TestDQT(unittest.TestCase):
    @classmethod
    def setup_class(cls):
        """Setting up the datasets and dataloader since they are needed
        for the dqt instance in order to generate the data quality table
        """
        cls.path_to_this_mod  = os.path.abspath(os.path.dirname(__file__))
        cls.path_to_test_file = os.path.join(cls.path_to_this_mod, "test.csv")
        cls.dataset           = load.DataSet(path_to_file = cls.path_to_test_file)
        cls.dataloader        = load.DataLoader(dataset = cls.dataset)

        cls.path_to_test_file_two = os.path.join(cls.path_to_this_mod, "test2.csv")
        cls.dataset_two           = load.DataSet(path_to_file = cls.path_to_test_file_two)
        cls.dataloader_two        = load.DataLoader(dataset = cls.dataset_two)

        cls.path_to_test_file_three = os.path.join(cls.path_to_this_mod, "test3.csv")
        cls.dataset_three           = load.DataSet(path_to_file = cls.path_to_test_file_three)
        cls.dataloader_three        = load.DataLoader(dataset = cls.dataset_three)


    def test_initialisation_s01(self):
        """ Test the initialisation of the dqt instance """

        """ PREPARATION """

        """ EXECUTION """
        data_quality_table = dqt.DataQualityTable(dataloader = self.dataloader)

        """ VERIFICATION """
        pd.testing.assert_frame_equal(data_quality_table.dataframe, self.dataloader.read_csv())


    def test_dqt_printing_s01(self):
        """Test whether the information about the columns of the dataframe and its associated
        data type is correctly printed out
        """

        """ PREPARATION """
        data_quality_table = dqt.DataQualityTable(dataloader = self.dataloader)

        """ EXECUTION """
        capture_output = StringIO()
        sys.stdout     = capture_output
        data_quality_table.print_header_infos()
        sys.stdout     = sys.__stdout__

        """ VERIFICATION """
        assert capture_output.getvalue() == "m2: <class 'numpy.int64'>\n" + \
                                            "number_of_rooms: <class 'numpy.int64'>\n" + \
                                            "city: <class 'str'>\n" + \
                                            "district: <class 'str'>\n" + \
                                            "price: <class 'numpy.int64'>\n"


    def test_dqt_generation_s01(self):
        """ Test with a dummy test file if the dqt table is correct and valid """

        """ PREPARATION """
        data_quality_table = dqt.DataQualityTable(dataloader = self.dataloader)

        """ EXECUTION """
        act_dqt_cont, act_dqt_catg = data_quality_table.create_table(continuous_features = ["m2", "number_of_rooms", "price"],
                                                                     categorical_features = ["city", "district"],
                                                                     store_json_dir = f"{self.path_to_this_mod}")

        """ VERIFICATION """
        exp_dqt_cont = pd.DataFrame({'Count': [4, 4, 4], 'Miss. %': [0.0, 0.0, 0.0], 'Card.': [4, 4, 3], 'Min': [15, 1, 700], '1st Qrt.': [41.25, 1.75, 1075.0],
                                     'mean': [63.75, 2.5, 1225.0], 'median': [60.0, 2.5, 1350.0], '3rd Qrt.': [82.5, 3.25, 1500.0], 'Max': [120, 4, 1500], 
                                     'Std. Dev.': [43.851073723076226, 1.2909944487358056, 377.4917217635375]},
                                     index = ["m2", "number_of_rooms", "price"])

        exp_dqt_catg = pd.DataFrame({'Count': [4, 4], 'Miss. %': [0.0, 0.0], 'Card.': [3, 4],
                                     'Mode': ["Chicago", "Grandview"], 'Mode Freq.': [2, 1], 'Mode Freq. %': [50.0, 25.0],
                                     '2nd Mode': ["Springfield", "Oak Brook"], '2nd Mode Freq.': [1, 1], '2nd Mode Freq. %': [25.0, 25.0]},
                                     index = ["city", "district"])

        pd.testing.assert_frame_equal(act_dqt_cont, exp_dqt_cont)
        pd.testing.assert_frame_equal(act_dqt_catg, exp_dqt_catg)


    def test_dqt_generation_s02(self):
        """Testing again the correct generation of the data quality table but this time
        with missing values
        """

        """ PREPARATION """
        data_quality_table = dqt.DataQualityTable(dataloader = self.dataloader_two)

        """ EXECUTION """
        act_dqt_cont, act_dqt_catg = data_quality_table.create_table(continuous_features = ["m2", "number_of_rooms", "price"],
                                                                     categorical_features = ["city", "district"],
                                                                     store_json_dir = f"{self.path_to_this_mod}")

        """ VERIFICATION """
        exp_dqt_cont = pd.DataFrame({'Count': [6, 6, 7], 'Miss. %': [14.285714285714285, 14.285714285714285, 0.0], 'Card.': [6, 4, 5], 'Min': [15.0, 1.0, 700.0], '1st Qrt.': [38.75, 2.0, 1200.0],
                                     'mean': [60.833333333333336, 2.5, 1612.7142857142858], 'median': [60.0, 2.5, 1500.0], '3rd Qrt.': [73.75, 3.0, 1990.0], 'Max': [120.0, 4.0, 2709.0],
                                     'Std. Dev.': [36.526246271231685, 1.0488088481701516, 724.9309655145825]},
                                     index = ["m2", "number_of_rooms", "price"])

        exp_dqt_catg = pd.DataFrame({'Count': [6, 7], 'Miss. %': [14.285714285714285, 0.0], 'Card.': [3, 5],
                                     'Mode': ["New York", "Oak Brook"], 'Mode Freq.': [3, 2], 'Mode Freq. %': [50.0, 28.57142857142857],
                                     '2nd Mode': ["Chicago", "Manhatten"], '2nd Mode Freq.': [2, 2], '2nd Mode Freq. %': [33.33333333333333, 28.57142857142857]},
                                     index = ["city", "district"])

        pd.testing.assert_frame_equal(act_dqt_cont, exp_dqt_cont)
        pd.testing.assert_frame_equal(act_dqt_catg, exp_dqt_catg)


    def test_dqt_consistency_check_e01(self):
        """Check if inconsistencies in data can be found, in this check we will check
        for data with missing values and/or values which are NaN
        """

        """ EXECUTION & VERIFICATION """
        with pytest.raises(exception.InconsistentData):
            dqt.DataQualityTable(dataloader = self.dataloader_two, check_consistency = True)

            
    def test_dqt_consistency_check_e02(self):
        """Check if inconsistencies in data can be found, in this check we will check
        for data with inconsistent data types
        """

        """ EXECUTION & VERIFICATION """
        with pytest.raises(exception.InconsistentDataTypes):
            dqt.DataQualityTable(dataloader = self.dataloader_three, check_consistency = True)


    def tearDown(self):
        """ Delete all json files if they were created due to the generation of dqts """
        first_json  = os.path.join(self.path_to_this_mod, "dqt_cont.json")
        if os.path.exists(first_json):
            os.remove(f"{self.path_to_this_mod}/dqt_cont.json")

        second_json = os.path.join(self.path_to_this_mod, "dqt_catg.json")
        if os.path.exists(second_json):
            os.remove(f"{self.path_to_this_mod}/dqt_catg.json")