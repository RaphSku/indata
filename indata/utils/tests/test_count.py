"""Testing the functionality of the counting tools"""

import pytest 


import indata.utils.count as count
import indata.exception.base as exception


class TestCountingCategories:
    @classmethod
    def setup_class(cls):
        """ Setup of test data """
        cls.test_data_one = ["dog", "ant", "bee", "ant", "cat", "dog", "ant"]
        cls.test_data_two = [0, 1, 0, 1, 1, 0]


    def test_counting_s01(self):
        """Test whether the dictionaries have the same set of keys and the same
        values
        """

        """ EXECUTION """
        act_result_one = count.Categories.count(data = self.test_data_one)
        exp_result_one = {'dog': 2, 'ant': 3, 'bee': 1, 'cat': 1}

        act_result_two = count.Categories.count(data = self.test_data_two)
        exp_result_two = {0: 3, 1: 3}

        """ VERIFICATION """
        assert act_result_one == exp_result_one
        assert act_result_two == exp_result_two


    def test_counting_e01(self):
        """Test whether an error is raised when the wrong dimension of data
        is given by the user
        """

        """ PREPARATION """
        test_data = [["dog", "ant"], ["ant", "cat"]]

        """ EXECUTION & VERIFICATION """
        with pytest.raises(exception.DimError):
            count.Categories.count(data = test_data)