import unittest
import pandas as pd
from fairness.fairness_metric.disparate_impact import return_privileged_unprivileged_protected_attribute_value


class PrivUnprivValueTest(unittest.TestCase):

    def test_privileged_value(self):
        genre_series = pd.Series([0, 1, 0, 0, 1, 0, 0])
        salary_series = pd.Series([10, 20, 20, 20, 10, 20, 10])

        test_dataframe = pd.DataFrame({
            'Genre': genre_series,
            'Salary': salary_series
        })

        value = return_privileged_unprivileged_protected_attribute_value(test_dataframe, 'Genre', 'unprivileged')
        self.assertEquals(value, 1)
        value = return_privileged_unprivileged_protected_attribute_value(test_dataframe, 'Genre', 'privileged')
        self.assertEquals(value, 0)
