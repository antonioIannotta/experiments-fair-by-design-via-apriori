import unittest
import pandas as pd
from fairness.fairness_metric.fairness_evaluation import DisparateImpact


class ProbabilityComputationTest(unittest.TestCase):

    def test_probability_1(self):
        disparate_impact = DisparateImpact()
        genre_series = pd.Series([0, 1, 0, 0, 1, 0, 0])
        salary_series = pd.Series([10, 20, 20, 20, 10, 20, 10])

        test_dataframe = pd.DataFrame({
            'Genre': genre_series,
            'Salary': salary_series
        })

        protected_attribute = 'Genre'
        protected_attribute_value = 0
        output_column = 'Salary'
        output_column_value = 10

        computed_disparate_impact = disparate_impact.compute_probability(test_dataframe, protected_attribute,
                                                                              protected_attribute_value, output_column,
                                                                              output_column_value)

        self.assertEquals(0.4, computed_disparate_impact)

    def test_compute_probability_2(self):
        disparate_impact = DisparateImpact()
        genre_series = pd.Series([0, 1, 0, 0, 1, 0, 0])
        salary_series = pd.Series([10, 20, 20, 20, 10, 20, 10])

        test_dataframe = pd.DataFrame({
            'Genre': genre_series,
            'Salary': salary_series
        })

        protected_attribute = 'Genre'
        protected_attribute_value = 0
        output_column = 'Salary'
        output_column_value = 20

        computed_disparate_impact = disparate_impact.compute_probability(test_dataframe, protected_attribute,
                                                                              protected_attribute_value, output_column,
                                                                              output_column_value)

        self.assertEquals(0.6, computed_disparate_impact)

    def test_compute_probability_3(self):
        disparate_impact = DisparateImpact()
        genre_series = pd.Series([0, 1, 0, 0, 1, 0, 0])
        salary_series = pd.Series([10, 20, 20, 20, 10, 20, 10])

        test_dataframe = pd.DataFrame({
            'Genre': genre_series,
            'Salary': salary_series
        })

        protected_attribute = 'Genre'
        protected_attribute_value = 1
        output_column = 'Salary'
        output_column_value = 10

        computed_disparate_impact = disparate_impact.compute_probability(test_dataframe, protected_attribute,
                                                                              protected_attribute_value, output_column,
                                                                              output_column_value)

        self.assertEquals(0.5, computed_disparate_impact)

    def test_compute_probability_4(self):

        disparate_impact = DisparateImpact()
        genre_series = pd.Series([0, 1, 0, 0, 1, 0, 0])
        salary_series = pd.Series([10, 20, 20, 20, 10, 20, 10])

        test_dataframe = pd.DataFrame({
            'Genre': genre_series,
            'Salary': salary_series
        })

        protected_attribute = 'Genre'
        protected_attribute_value = 1
        output_column = 'Salary'
        output_column_value = 20

        computed_disparate_impact = disparate_impact.compute_probability(test_dataframe, protected_attribute,
                                                                              protected_attribute_value, output_column,
                                                                              output_column_value)

        self.assertEquals(0.5, computed_disparate_impact)
