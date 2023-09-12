import unittest

import pandas as pd

from fairness.proxy.proxy_detection import check_values_type_for_attribute


class CheckValueTypeTest(unittest.TestCase):

    def test_discrete_values(self):
        dataset = pd.DataFrame({
            'A': pd.Series([1, 2, 3, 4, 5, 6, 7]),
            'B': pd.Series([0.5, 0.6, 6.1, 7.4, 8.9, 9.0])
        })

        self.assertEquals('Discrete', check_values_type_for_attribute(dataset, 'A'))

    def test_continuous_values(self):
        dataset = pd.DataFrame({
            'A': pd.Series([1, 2, 3, 4, 5, 6, 7]),
            'B': pd.Series([0.5, 0.6, 6.1, 7.4, 8.9, 9.0])
        })

        self.assertEquals('Continuous', check_values_type_for_attribute(dataset, 'B'))
