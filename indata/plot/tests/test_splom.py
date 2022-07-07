"""Testing the generation of SPLOMS"""

import os
import unittest
import pandas as pd


import indata.dataio.load as load
import indata.plot.splom as splom


class TestSPLOM(unittest.TestCase):
    @classmethod
    def setup_class(cls):
        """Setting up the dataset and dataloader from which the SPLOM should be 
        created
        """
        cls.path_to_this_mod  = os.path.abspath(os.path.dirname(__file__))
        cls.path_to_test_file = os.path.join(cls.path_to_this_mod, "test.csv")
        cls.dataset           = load.DataSet(path_to_file = cls.path_to_test_file)
        cls.dataloader        = load.DataLoader(dataset = cls.dataset)


    def test_initialisation_s01(self):
        """ Testing whether a SPLOM instance is correctly initialised """

        """ PREPARATION """
        data     = self.dataloader.read_csv()

        """ EXECUTION """
        spm      = splom.SPLOM(name = "SPLOM Test", continuous_data = data[["Feature1", "Feature2", "Feature3"]])
        act_name = spm.name
        act_data = spm.continuous_data 

        """ VERIFICATION """
        exp_name = "SPLOM Test"
        exp_data = data[["Feature1", "Feature2", "Feature3"]]

        assert act_name == exp_name
        pd.testing.assert_frame_equal(act_data, exp_data)


    def test_successful_plot_s01(self):
        """ Testing whether a SPLOM is successfully created and stored
        in the appointed directory """

        """ PREPARATION """
        data = self.dataloader.read_csv()
        spm  = splom.SPLOM(name = "SPLOM Test", continuous_data = data[["Feature1", "Feature2", "Feature3"]])

        """ EXECUTION """
        spm.plot(store_dir = f"{self.path_to_this_mod}/plots")

        """ VERIFICATION """
        file_exists = False
        if os.path.exists(f"{self.path_to_this_mod}/plots/splom/SPLOM Test.html"):
            file_exists = True

        assert file_exists == True


    def tearDown(self):
        """ Delete all the files which have been generated """
        if os.path.exists(f"{self.path_to_this_mod}/plots/splom/SPLOM Test.html"):
            os.remove(f"{self.path_to_this_mod}/plots/splom/SPLOM Test.html")
            os.rmdir(f"{self.path_to_this_mod}/plots/splom/")
            os.rmdir(f"{self.path_to_this_mod}/plots/")