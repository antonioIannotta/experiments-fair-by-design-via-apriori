import pandas as pd
from fairness.fairness_metric.disparate_impact import *


def return_proxy_variables(dataset: pd.DataFrame, variables: list, protected_attributes: list) -> list:
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


"""
def _compute_disparate_impact_for_proxy(antecedent, consequent,
                                        original_dataset: pd.DataFrame) -> float:
    proxy = antecedent.split(' = ')[0]
    proxy_value = int(antecedent.split(' = ')[1])
    protected_column = consequent.split(' = ')[0]
    protected_value = int(consequent.split(' = ')[1])

    unprivileged_probability = _compute_probability(original_dataset, proxy, proxy_value, protected_column,
                                                    protected_value, False)
    privileged_probability = _compute_probability(original_dataset, proxy, proxy_value, protected_column,
                                                  protected_value, True)

    if unprivileged_probability == 0.0:
        return 0.0
    else:
        return unprivileged_probability / privileged_probability


def _compute_probability(dataset: pd.DataFrame, proxy, proxy_value, protected_column, protected_value,
                         privileged_group: bool) -> float:
    if privileged_group is True:
        proxy_columns_data = dataset[dataset[proxy] == proxy_value]
        return len(proxy_columns_data.loc[proxy_columns_data[protected_column] == protected_value]) / len(
            proxy_columns_data)
    else:
        proxy_columns_data = dataset[dataset[proxy] != proxy_value]
        return len(proxy_columns_data.loc[proxy_columns_data[protected_column] == protected_value]) / len(
            proxy_columns_data)

"""
