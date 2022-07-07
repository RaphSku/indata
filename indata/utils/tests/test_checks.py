"""Testing the functionality of the checking tools"""

import pytest 


import indata.utils.checks as checks


class TestChecking:
    @classmethod
    def setup_class(cls):
        """ Setup of test data """
        pass


    def test_checking_s01(self):
        """Test whether strings are recognised as numeric or not with a few examples
        """

        """ PREPARATION """
        first_example  = "Hey, Cindy"
        second_example = "247"
        third_example  = "575.427"
        fourth_example = "274.2471.247"

        """ EXECUTION """
        act_first_result  = checks.isNumeric(first_example)
        act_second_result = checks.isNumeric(second_example)
        act_third_result  = checks.isNumeric(third_example)
        act_fourth_result = checks.isNumeric(fourth_example)

        """ VERIFICATION """
        assert act_first_result  == False
        assert act_second_result == True
        assert act_third_result  == True
        assert act_fourth_result == False


    def test_checking_e01(self):
        """Test whether an error is raised when the input is not a string
        """

        """ PREPARATION """
        example = 247.92

        """ EXEUCTION & VERIFICATION """
        with pytest.raises(TypeError):
            checks.isNumeric(example)