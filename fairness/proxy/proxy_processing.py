import pandas as pd
from proxy_detection import return_proxy_variables


def _return_proxy_protected_attribute(proxy_variables: pd.DataFrame,
                                      protected_attributes: list) -> pd.DataFrame:
    """This method returns a dataframe containing the proxy variables for each sensitive attribute

    Args:
        proxy_variables (pd.DataFrame): the dataframe of the proxy variables (antecedent, consequent, confidence)
        protected_attributes (list): the list of the protected attributes

    Returns:
        pd.DataFrame: _description_
    """
    sensitive_antecedent = []
    sensitive_consequent = []
    for index, proxy_row in proxy_variables.iterrows():
        for consequent in proxy_row['Consequent']:
            for sensitive_attribute in protected_attributes:
                if str(consequent).startswith(sensitive_attribute):
                    sensitive_antecedent.append(proxy_row['Antecedent'])
                    sensitive_consequent.append(consequent)

    dataframe = pd.DataFrame(
        {'Antecedent': pd.Series(sensitive_antecedent), 'Consequent': pd.Series(sensitive_consequent)})

    return dataframe


def proxy_fixing(original_dataset: pd.DataFrame, protected_attributes: list) -> pd.DataFrame:
    """This method returns a dataset with proxy variables founded in the original dataset analyzed.
    In case these proxies lead to unfairness the proxies are deleted

    Args: original_dataset (pd.DataFrame): the dataset on which the proxy variable have to be deleted if they lead to
    unfairness
    protected_attributes (list): the list of protected attribute on which perform the proxy analysis

    Returns:
        pd.DataFrame: returns the dataframe in which the proxies do not lead to fairness
    """
    proxy_variables = return_proxy_variables(original_dataset, 0.8)
    dataset = original_dataset
    proxy_variables_for_sensitive_attributes = _return_proxy_protected_attribute(proxy_variables,
                                                                                 protected_attributes)

    for index, row in proxy_variables_for_sensitive_attributes.iterrows():
        for antecedent in row['Antecedent']:
            consequent = row['Consequent']

            disparate_impact_value = _compute_disparate_impact_for_proxy(antecedent, consequent,
                                                                         original_dataset)
            if not 0.8 < disparate_impact_value < 1.25:
                dataset = _remove_proxy_from_dataset(original_dataset, antecedent)

            else:
                continue

    return dataset


def _compute_disparate_impact_for_proxy(antecedent, consequent,
                                        original_dataset: pd.DataFrame) -> float:
    """
    This method compute the disparate impact assuming antecedent (the proxy) as attribute and the consequent (the protected
    value) as output
    :param antecedent: the proxy value in the form "PROXY = VALUE"
    :param consequent: the protected value in the form "PROTECTED ATTRIBUTE = VALUE"
    :param original_dataset: the dataset on which perform the computation
    :return: returns the disparate impact value between the proxy and teh protected attribute computed on the dataset
    """
    proxy = antecedent.split(' = ')[0]
    print(type(proxy))
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
    """
    This method computes the disparate impact value starting from the parameters
    :param dataset: the dataset on which compute the disparate impact
    :param proxy: the proxy attribute needed to compute the disparate impact value
    :param proxy_value: the value of the proxy attribute
    :param protected_column: the protected attribute needed to compute the disparate impact value
    :param protected_value: the value of the protected attribute
    :param privileged_group: a boolean variable that establish if have been computed the probability on
    privileged / unprivileged group needed to return the disparate impact value
    :return:
    """
    if privileged_group is True:
        proxy_columns_data = dataset[dataset[proxy] == proxy_value]
        return len(proxy_columns_data.loc[proxy_columns_data[protected_column] == protected_value]) / len(
            proxy_columns_data)
    else:
        proxy_columns_data = dataset[dataset[proxy] != proxy_value]
        return len(proxy_columns_data.loc[proxy_columns_data[protected_column] == protected_value]) / len(
            proxy_columns_data)


def _remove_proxy_from_dataset(original_dataset: pd.DataFrame, antecedent: str) -> pd.DataFrame:
    """This method removes the proxy columns from the original dataset

    Args:
        original_dataset (pd.DataFrame): the dataset from which the proxies have to be removed
        antecedent (str): the proxy value that has to be removed from the dataset

    Returns:
        pd.DataFrame: returns a new dataframe without the proxy column
    """
    dataset = original_dataset.drop(columns=[antecedent.split(' = ')[0]], axis=1, inplace=False)

    return dataset


def _proxy_format_to_column(row: pd.Series) -> list:
    """This function converts the information related to the proxy into the column name

    Args:
        row (pd.Series): a series that needs to be converted in a list containing only the proxy attributes without the
        values

    Returns:
        list: _description_
    """
    result = []
    for element in row:
        result.append(element.split(' = ')[0])

    return result
