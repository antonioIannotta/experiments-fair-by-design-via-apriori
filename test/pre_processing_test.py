import unittest
import pandas as pd
from fairness.pre_processing import *


class PreProcessingTest(unittest.TestCase):

    def test_fix_protected_attributes_1(self):
        genre_series = pd.Series([2, 3, 3, 2, 3, 3])
        salary_series = pd.Series([20, 30, 20, 20, 30, 40])

        test_dataframe = pd.DataFrame({
            'Genre': genre_series,
            'Salary': salary_series
        })

        protected_attributes = ['Genre']

        result = fix_protected_attributes(test_dataframe, protected_attributes)
        self.assertEquals(result['Genre'].values.tolist(), [0, 1, 1, 0, 1, 1])

    def test_fix_protected_attributes_2(self):
        genre_series = pd.Series([2, 3, 4, 2, 4, 3])
        salary_series = pd.Series([20, 30, 20, 20, 30, 40])

        test_dataframe = pd.DataFrame({
            'Genre': genre_series,
            'Salary': salary_series
        })

        protected_attributes = ['Genre']

        result = fix_protected_attributes(test_dataframe, protected_attributes)
        self.assertEquals(result['Genre'].values.tolist(), [0, 0, 1, 0, 1, 0])
