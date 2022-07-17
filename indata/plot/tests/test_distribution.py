"""Testing the generation of distribution plots"""

import os
import unittest
import pandas as pd


import indata.dataio.load as load
import indata.table.dqt as dqt
import indata.utils.count as count
import indata.plot.distribution as distribution


class TestDistributionPlots(unittest.TestCase):
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
        """ Testing whether a continuous distribution plot instance is correctly initialised """

        """ PREPARATION """
        data            = self.dataloader.read_csv()
        analytics_table = dqt.DataQualityTable(dataloader = self.dataloader)
        cqt, _          = analytics_table.create_table(continuous_features = ["Feature1", "Feature2", "Feature3", "Feature4"], 
                                                       categorical_features = [], store_json_dir = f"{self.path_to_this_mod}")

        """ EXECUTION """
        cdist    = distribution.ContinuousDistributionPlotter(name = "Feature1", data = data["Feature1"], dqt = cqt)
        act_name = cdist.name
        act_data = cdist.data 
        act_dqt  = cdist.dqt
        act_dir  = cdist.store_dir

        """ VERIFICATION """
        exp_name = "Feature1"
        exp_data = data["Feature1"]
        exp_dqt  = cqt
        exp_dir  = "./"
        
        assert act_name == exp_name
        assert act_dir  == exp_dir
        pd.testing.assert_series_equal(act_data, exp_data)
        pd.testing.assert_frame_equal(act_dqt, exp_dqt)


    def test_initialisation_s02(self):
        """ Testing whether a categorical distribution plot instance is correctly initialised """

        """ PREPARATION """
        data            = self.dataloader.read_csv()
        analytics_table = dqt.DataQualityTable(dataloader = self.dataloader)
        _, cat_qt       = analytics_table.create_table(continuous_features = ["Feature1", "Feature2", "Feature3", "Feature4"], 
                                                       categorical_features = ["Feature5"], store_json_dir = f"{self.path_to_this_mod}")

        """ EXECUTION """
        cdist    = distribution.ContinuousDistributionPlotter(name = "Feature5", data = data["Feature5"], dqt = cat_qt)
        act_name = cdist.name
        act_data = cdist.data 
        act_dqt  = cdist.dqt
        act_dir  = cdist.store_dir

        """ VERIFICATION """
        exp_name = "Feature5"
        exp_data = data["Feature5"]
        exp_dqt  = cat_qt
        exp_dir  = "./"
        
        assert act_name == exp_name
        assert act_dir  == exp_dir
        pd.testing.assert_series_equal(act_data, exp_data)
        pd.testing.assert_frame_equal(act_dqt, exp_dqt)


    def test_successful_plot_s01(self):
        """ Testing whether a continuous distribution plot is successfully created and stored
        in the appointed directory """

        """ PREPARATION """
        data            = self.dataloader.read_csv()
        analytics_table = dqt.DataQualityTable(dataloader = self.dataloader)
        cqt, _          = analytics_table.create_table(continuous_features = ["Feature1", "Feature2", "Feature3", "Feature4"], 
                                                       categorical_features = [], store_json_dir = f"{self.path_to_this_mod}")
        cdist           = distribution.ContinuousDistributionPlotter(name = "Feature1", data = data["Feature1"], dqt = cqt,
                                                                     store_dir = f"{self.path_to_this_mod}/plots")

        """ EXECUTION """
        cdist.plot()

        """ VERIFICATION """
        file_exists = False
        if os.path.exists(f"{self.path_to_this_mod}/plots/continuous/Feature1.html"):
            file_exists = True

        assert file_exists == True

    
    def test_successful_plot_s02(self):
        """ Testing whether a categorical distribution plot is successfully created and stored
        in the appointed directory """

        """ PREPARATION """
        data            = self.dataloader.read_csv()
        analytics_table = dqt.DataQualityTable(dataloader = self.dataloader)
        _, cat_qt       = analytics_table.create_table(continuous_features = ["Feature1", "Feature2", "Feature3", "Feature4"], 
                                                       categorical_features = ["Feature5"], store_json_dir = f"{self.path_to_this_mod}")
        label_hash      = count.Categories.count(data = data["Feature5"].to_numpy())
        cat_dist        = distribution.CategoricalDistributionPlotter(name = "Feature5", data = data["Feature5"], dqt = cat_qt, label_hash = label_hash,
                                                                      store_dir = f"{self.path_to_this_mod}/plots")

        """ EXECUTION """
        cat_dist.plot()

        """ VERIFICATION """
        file_exists = False
        if os.path.exists(f"{self.path_to_this_mod}/plots/categorical/Feature5.html"):
            file_exists = True

        assert file_exists == True


    def tearDown(self):
        """ Delete all the files which have been generated """
        if os.path.exists(f"{self.path_to_this_mod}/plots/continuous/Feature1.html"):
            os.remove(f"{self.path_to_this_mod}/plots/continuous/Feature1.html")
            os.rmdir(f"{self.path_to_this_mod}/plots/continuous/")
            os.rmdir(f"{self.path_to_this_mod}/plots/")

        if os.path.exists(f"{self.path_to_this_mod}/plots/categorical/Feature5.html"):
            os.remove(f"{self.path_to_this_mod}/plots/categorical/Feature5.html")
            os.rmdir(f"{self.path_to_this_mod}/plots/categorical/")
            os.rmdir(f"{self.path_to_this_mod}/plots/")
        
        if os.path.exists(f"{self.path_to_this_mod}/dqt_cont.json"):
            os.remove(f"{self.path_to_this_mod}/dqt_cont.json")

        if os.path.exists(f"{self.path_to_this_mod}/dqt_catg.json"):
            os.remove(f"{self.path_to_this_mod}/dqt_catg.json")