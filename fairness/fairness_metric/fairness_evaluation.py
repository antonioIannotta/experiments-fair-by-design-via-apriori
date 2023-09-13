import pandas as pd
import numpy as np


def fairness_evaluation(dataset: pd.DataFrame, protected_attributes: list, output_column_values: list,
                        output_column: str) -> str:
    """
    This method perform an analysis of the dataset in order to establish if it's either fair or unfair
    Args:
        dataset: the dataset on which perform the computation to establish the fairness/unfairness
        protected_attributes: the list of protected attributes that are fundamental in order to compute the value needed
        for the DI metric
        output_column_values: the values of the output column that are needed in order to establish the
        DI value for each possible output value
        output_column: the output column

    Returns:
    'fair' or 'unfair'
    """
    bias_analysis_dataframe = return_disparate_impact_for_fairness_evaluation(dataset, protected_attributes,
                                                                              output_column_values,
                                                                              output_column)
    return_value = 'unfair'
    for value in bias_analysis_dataframe['Disparate Impact'].values:
        if value <= 0.80 or value >= 1.25:
            return_value = 'unfair'
            break
        else:
            return_value = 'fair'

    return return_value


def return_privileged_unprivileged_protected_attribute_value(dataset: pd.DataFrame, attribute: str, param: str) -> int:
    """

    Args:
        dataset: the dataset needed to perform the computation about the most and less frequent value for a
        specific variable
        attribute: the variable on which compute the frequency of its values
        param: variable used to specify if there's interest for either privileged or unprivileged value

    Returns: returns the most frequent value if the interest is for the privileged group, otherwise it returns the
    less frequent value for the unprivileged group
    """
    unique_values = dataset[attribute].unique().tolist()
    value_frequency = []
    print(unique_values)
    if param == 'unprivileged':
        for value in unique_values:
            value_frequency.append(dataset[attribute].values.tolist().count(value))
        index = value_frequency.index(min(value_frequency))
        return unique_values[index]
    else:
        for value in unique_values:
            value_frequency.append(dataset[attribute].values.tolist().count(value))
        index = value_frequency.index(max(value_frequency))
        return unique_values[index]


def return_disparate_impact_for_fairness_evaluation(dataset: pd.DataFrame, protected_attributes: list,
                                                    output_column_values: list, output_column: str) -> pd.DataFrame:
    """

    Args:
        dataset: the dataset on which compute the disparate impact value
        protected_attributes: the list of protected attributes for the ones there's an interest about their DI value
        output_column_values: the list of possible values for the output column
        output_column: the output column

    Returns: this method returns the disparate impact value computed on the dataset for a specific attribute and a
    specific output column

    """
    attribute_array = []
    disparate_impact_array = []
    disparate_impact_dataframe = pd.DataFrame()
    for output_value in output_column_values:
        for attribute in protected_attributes:
            attribute_array.append(attribute)
            unprivileged_protected_attribute_value = (
                return_privileged_unprivileged_protected_attribute_value(dataset, attribute, 'unprivileged'))
            privileged_protected_attribute_value = (
                return_privileged_unprivileged_protected_attribute_value(dataset, attribute, 'privileged'))

            unprivileged_probability = compute_probability(dataset, attribute, unprivileged_protected_attribute_value,
                                                           output_column, output_value)

            privileged_probability = compute_probability(dataset, attribute, privileged_protected_attribute_value,
                                                         output_column, output_value)

            disparate_impact = unprivileged_probability / privileged_probability
            disparate_impact_array.append(disparate_impact)

        attribute_series = pd.Series(attribute_array)
        disparate_impact_series = pd.Series(np.array(disparate_impact_array))
        disparate_impact_dataframe = pd.DataFrame(
            {"Attribute": attribute_series, "Disparate Impact": disparate_impact_series})

    return disparate_impact_dataframe


def compute_probability(dataset: pd.DataFrame, protected_attribute, protected_attribute_value,
                        output_column, output_value) -> float:
    """

    Args:
        dataset:
        protected_attribute:
        protected_attribute_value:
        output_column:
        output_value:

    Returns:
        this method computes the probability for a specific value in order to be further used to compute the DI value
    """
    attribute_columns_data = dataset[dataset[protected_attribute] == protected_attribute_value]
    return len(attribute_columns_data[attribute_columns_data[output_column] == output_value]) / len(
        attribute_columns_data)