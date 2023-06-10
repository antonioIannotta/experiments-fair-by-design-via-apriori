import pandas as pd
import numpy as np


class DisparateImpact:

    def bias_detection(self, dataset: pd.DataFrame, protected_attributes: list, output_column: pd.Series) -> pd.DataFrame:
        """
        This method check the disparate impact for each sensitive attributes in the dataset and returns a dataframe in
        which a column is the series of attributes and a column is the disparate impact value for each attribute
        Args:
            dataset: pd.DataFrame: it is the original dataset on which perform the bias detection
            protected_attributes: list: it is the list of the protected attributes on which to compute the disparate
            impact value
            output_columng: pd.Series: it is the output column needed to compute the disparate impact value

        Returns:
            pd.Dataframe

        """
        return self.return_disparate_impact(dataset, protected_attributes, output_column)

    # This method evaluates the fairness starting from the result of the check method.
    def fairness_evaluation(self, dataset: pd.DataFrame, protected_attributes: list, output_column: pd.Series) -> str:
        """
        This method perform an evaluation of the fairness of a given dataset according to the Disparate Impact metric
        :param dataset: this is the dataset on which to be labelled as fair or unfair
        :param protected_attributes: the list of the protected attributes on which compute the disparate impact value
        :param output_column: the column of the dataset that represents the output
        :return: return 'fair' if the dataset is fair, unfair 'otherwise'
        """
        bias_analysis_dataframe = self.bias_detection(dataset, protected_attributes, output_column)
        return_value = 'unfair'
        for value in bias_analysis_dataframe['Disparate Impact'].values:
            if value <= 0.80 or value >= 1.25:
                return_value = 'unfair'
                break
            else:
                return_value = 'fair'

        return return_value

    def return_disparate_impact(self, dataset: pd.DataFrame, protected_attributes: list, 
                                output_column: str) -> pd.DataFrame:
        """
        This method returns a dataframe in which, for each protected attribute is related the correspondent
        Disparate Impact value
        :param dataset: the dataset on which the disparate impact value must be computed
        :param protected_attributes: set of protected attributes for which the disparate impact value must be
        computed
        :param output_column: the output column needed to compute the disparate impact value
        :return:
        """
        attribute_series = pd.Series(protected_attributes)
        disparate_impact_array = []
        for attribute in protected_attributes:
            unprivileged_probability = self.compute_disparate_impact(dataset, attribute, 0,
                                                                     output_column, 1)
            
            privileged_probability = self.compute_disparate_impact(dataset, attribute, 1,
                                                                   output_column, 1)
            
            disparate_impact = unprivileged_probability / privileged_probability
            disparate_impact_array.append(disparate_impact)

        disparate_impact_series = pd.Series(np.array(disparate_impact_array))
        disparate_impact_dataframe = pd.DataFrame(
            {"Attribute": attribute_series, "Disparate Impact": disparate_impact_series})
        return disparate_impact_dataframe

    # This method compute the disparate impact for a specific attribute
    def compute_disparate_impact(self, dataset: pd.DataFrame, protected_attribute, protected_attribute_value,
                                 output_column, output_value) -> float:
        """
        This method computes the disparate impact value starting from the parameters
        :param dataset: the dataset needed to perform the computation
        :param protected_attribute: the protected attribute on which compute the disparate impact
        :param protected_attribute_value: the value of the protected attribute
        :param output_column: the output of interest
        :param output_value: the value of the output of interest
        :return:
        """
        attribute_columns_data = dataset[dataset[protected_attribute] == protected_attribute_value]
        return len(attribute_columns_data[attribute_columns_data[output_column] == output_value]) / len(
            attribute_columns_data)
