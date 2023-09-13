import unittest
import pandas as pd
from fairness.fairness_metric.fairness_evaluation import DisparateImpact


class ReturnDisparateImpactTest(unittest.TestCase):

    def test_return_disparate_impact_1(self):
        disparate_impact = DisparateImpact()
        genre_series = pd.Series([0, 1, 0, 0, 1, 0, 0])
        salary_series = pd.Series([10, 20, 20, 20, 10, 20, 10])

        test_dataframe = pd.DataFrame({'Genre': genre_series, 'Salary': salary_series})
        protected_attribute = ['Genre']
        output_column = 'Salary'
        output_column_values = [10, 20]
        result_dataframe = disparate_impact.return_disparate_impact(test_dataframe, protected_attribute,
                                                                    output_column_values, output_column)

        self.assertTrue(result_dataframe['Disparate Impact'][0] == 0.8
                        and result_dataframe['Disparate Impact'][1] == 1.2)
