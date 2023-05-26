import pandas as pd
import numpy as np


class DisparateImpact:

    def bias_detection(self, dataset: pd.DataFrame, protected_attributes: list) -> pd.DataFrame:
        """
        This method check the disparate impact for each sensitive attributes in the dataset and returns a dataframe in
        which a column is the series of attributes and a column is the disparate impact value for each attribute
        Args:
            dataset: pd.DataFrame: it is the original dataset on which perform the bias detection
            protected_attributes: list: it is the list of the protected attributes on which to compute the disparate
            impact value

        Returns:
            pd.Dataframe

        """
        return self.return_disparate_impact(dataset, protected_attributes)

    # This method evaluates the fairness starting from the result of the check method.
    def fairness_evaluation(self, dataset: pd.DataFrame, protected_attributes: list) -> str:
        """
        This method perform an evaluation of the fairness of a given dataset according to the Disparate Impact metric
        :param dataset: this is the dataset on which to be labelled as fair or unfair
        :param protected_attributes: the list of the protected attributes on which compute the disparate impact value
        :return: return 'fair' if the dataset is fair, unfair 'otherwise'
        """
        bias_analysis_dataframe = self.bias_detection(dataset, protected_attributes)
        return_value = 'unfair'
        for value in bias_analysis_dataframe['Disparate Impact'].values:
            if value <= 0.80 or value >= 1.25:
                return_value = 'unfair'
            else:
                return_value = 'fair'

        return return_value

    # This method returns the sensitive attributes into the dataframe.
    # (Only in this previous have been considered sensitive attributes the ones with only 2 possible values)
    #def return_sensitive_attributes(self, dataset: pd.DataFrame):
    #    sensitive_attributes = []
    #    for attr in dataset.columns[:len(dataset.columns) - 1]:
    #        unique_values = self.return_unique_values_for_attribute(attr, dataset)
    #        if len(unique_values) == 2:
    #            sensitive_attributes.append(attr)
    #        else:
    #            continue
    #
    #    return sensitive_attributes

    # This method return the value that each attribute can have.
    #def return_unique_values_for_attribute(self, attribute, dataset: pd.DataFrame):
    #    unique_values = []
    #    for value in dataset[attribute][1:].values:
    #        if value not in unique_values:
    #            unique_values.append(value)
    #        else:
    #            continue
    #
    #    return unique_values

    # This method takes the sensitive attributes and returns a dataset in which the values of each sensitive attribute is
    # either 1 or 0
    #def columns_normalization_max_min(self, dataset: pd.DataFrame, sensitive_attributes) -> pd.DataFrame:
    #    for attribute in sensitive_attributes:
    #        unique_values = self.return_unique_values_for_attribute(attribute, dataset)
    #        dataset[attribute].replace({max(unique_values): 1, min(unique_values): 0}, inplace=True)
    #
    #    return dataset

    def return_disparate_impact(self, dataset: pd.DataFrame, protected_attributes: list) -> pd.DataFrame:
        """
        This method returns a dataframe in which, for each protected attribute is related the correspondent
        Disparate Impact value
        :param dataset: the dataset on which the disparate impact value must be computed
        :param protected_attributes: set of protected attributes for which the disparate impact value must be
        computed
        :return:
        """
        attribute_series = pd.Series(protected_attributes)
        disparate_impact_array = []
        for attribute in protected_attributes:
            unprivileged_probability = self.compute_disparate_impact(dataset, attribute, 0,
                                                                     dataset.columns[len(dataset.columns) - 1], 1)
            privileged_probability = self.compute_disparate_impact(dataset, attribute, 1,
                                                                   dataset.columns[len(dataset.columns) - 1], 1)
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