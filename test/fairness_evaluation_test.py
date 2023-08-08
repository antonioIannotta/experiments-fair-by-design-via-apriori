import unittest
import pandas as pd
from fairness.fairness_metric.disparate_impact import DisparateImpact


class FairnessEvaluationTest(unittest.TestCase):

    def test_fairness_evaluation_1(self):
        disparate_impact = DisparateImpact()

        genre_series = pd.Series([0, 1, 0, 0, 1, 0, 0])
        salary_series = pd.Series([10, 20, 20, 20, 10, 20, 10])

        test_dataframe = pd.DataFrame({'Genre': genre_series, 'Salary': salary_series})
        protected_attribute = ['Genre']
        output_column = 'Salary'
        output_column_values = [10, 20]

        fairness_eval = disparate_impact.fairness_evaluation(test_dataframe, protected_attribute,
                                                             output_column_values, output_column)

        self.assertEquals(fairness_eval, 'unfair')

    def test_fairness_evaluation_2(self):
        disparate_impact = DisparateImpact()

        genre_series = pd.Series([0, 0, 1, 1, 0, 0, 1, 1])
        salary_series = pd.Series([10, 20, 20, 10, 10, 20, 10, 20])

        test_dataframe = pd.DataFrame({'Genre': genre_series, 'Salary': salary_series})
        protected_attribute = ['Genre']
        output_column = 'Salary'
        output_column_values = [10, 20]

        fairness_eval = disparate_impact.fairness_evaluation(test_dataframe, protected_attribute,
                                                             output_column_values, output_column)

        self.assertEquals(fairness_eval, 'fair')
