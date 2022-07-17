"""Testing the generation of boxplots"""

import os
import unittest
import pandas as pd


import indata.dataio.load as load
import indata.plot.boxplot as boxplot


class TestBoxplot(unittest.TestCase):
    @classmethod
    def setup_class(cls):
        """Setting up the dataset and dataloader from which the boxplots should be 
        created
        """
        cls.path_to_this_mod  = os.path.abspath(os.path.dirname(__file__))
        cls.path_to_test_file = os.path.join(cls.path_to_this_mod, "test.csv")
        cls.dataset           = load.DataSet(path_to_file = cls.path_to_test_file)
        cls.dataloader        = load.DataLoader(dataset = cls.dataset)


    def test_initialisation_s01(self):
        """ Testing whether a boxplot instance is correctly initialised """

        """ PREPARATION """
        data     = self.dataloader.read_csv()

        """ EXECUTION """
        box      = boxplot.BoxPlot(name = "Boxplot Test", data = data["Feature2"])
        act_name = box.name
        act_data = box.data 
        act_dir  = box.store_dir

        """ VERIFICATION """
        exp_name = "Boxplot Test"
        exp_data = data["Feature2"]
        exp_dir  = "./"
        
        assert act_name == exp_name
        assert act_dir  == exp_dir
        pd.testing.assert_series_equal(act_data, exp_data)


    def test_successful_plot_s01(self):
        """ Testing whether a boxplot is successfully created and stored
        in the appointed directory """

        """ PREPARATION """
        data = self.dataloader.read_csv()
        box  = boxplot.BoxPlot(name = "Boxplot Test", data = data["Feature2"], store_dir = f"{self.path_to_this_mod}/plots")

        """ EXECUTION """
        box.plot()

        """ VERIFICATION """
        file_exists = False
        if os.path.exists(f"{self.path_to_this_mod}/plots/boxplots/Boxplot Test.html"):
            file_exists = True

        assert file_exists == True


    def tearDown(self):
        """ Delete all the files which have been generated """
        if os.path.exists(f"{self.path_to_this_mod}/plots/boxplots/Boxplot Test.html"):
            os.remove(f"{self.path_to_this_mod}/plots/boxplots/Boxplot Test.html")
            os.rmdir(f"{self.path_to_this_mod}/plots/boxplots/")
            os.rmdir(f"{self.path_to_this_mod}/plots/")