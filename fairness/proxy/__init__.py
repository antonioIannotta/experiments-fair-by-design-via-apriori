import pandas as pd


def proxy_detection(dataset: pd.DataFrame, protected_attributes: list) -> list:
    pass


def compute_disparate_impact_to_detect_proxy(attribute: pd.Series, protected_attribute: pd.Series) -> float:
    pass


def check_values_type_for_attribute(dataset: pd.DataFrame, variable: str) -> str:
    result = ""
    for value in dataset[variable]:
        if isinstance(value, int):
            result = 'Discrete'
        else:
            result = "Continuous"
            return result

    return result


def _compute_disparate_impact_for_proxy(attribute: str, protected_attribute: str,
                                        dataset: pd.DataFrame) -> str:
    if check_values_type_for_attribute(dataset, attribute) == 'Discrete':
        most_frequent_value = return_most_frequent_value(dataset, attribute)
        protected_attribute_values_list = dataset[protected_attribute].values
        for protected_attribute_value in protected_attribute_values_list:
            unprivileged_probability = _compute_probability_discrete_scenario(dataset, attribute, most_frequent_value,
                                                                              protected_attribute,
                                                                              protected_attribute_value, False)

            privileged_probability = _compute_probability_discrete_scenario(dataset, attribute, most_frequent_value,
                                                                            protected_attribute,
                                                                            protected_attribute_value, True)

            if (unprivileged_probability / privileged_probability) <= 0.8 or (unprivileged_probability / privileged_probability) >= 1.25:
                return 'PROXY'
            else:
                continue
    else:
        pass
         #TODO THIS

    """
    unprivileged_probability = _compute_probability(original_dataset, proxy, proxy_value, protected_column,
                                                    protected_value, False)
    privileged_probability = _compute_probability(original_dataset, proxy, proxy_value, protected_column,
                                                  protected_value, True)

    if unprivileged_probability == 0.0:
        return 0.0
    else:
        return unprivileged_probability / privileged_probability
    """
    return 'NOT PROXY'


def return_most_frequent_value(dataset: pd.DataFrame, attribute: str) -> int:
    unique_values = dataset[attribute].values.unique()
    most_frequent_value = 0
    max_frequency = 0
    unique_values_dict = {}
    for value in unique_values:
        frequency_value = dataset[dataset[attribute] == value].count()
        if frequency_value >= max_frequency:
            max_frequency = frequency_value
            most_frequent_value = value

    return most_frequent_value


def _compute_probability_discrete_scenario(dataset: pd.DataFrame, proxy, proxy_value, protected_column, protected_value,
                                           privileged_group: bool) -> float:
    if privileged_group is True:
        proxy_columns_data = dataset[dataset[proxy] == proxy_value]
        return len(proxy_columns_data.loc[proxy_columns_data[protected_column] == protected_value]) / len(
            proxy_columns_data)
    else:
        proxy_columns_data = dataset[dataset[proxy] != proxy_value]
        return len(proxy_columns_data.loc[proxy_columns_data[protected_column] == protected_value]) / len(
            proxy_columns_data)
