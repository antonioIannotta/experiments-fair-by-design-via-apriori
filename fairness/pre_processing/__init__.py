import pandas as pd
from sklearn.preprocessing import LabelEncoder


def fix_attributes(dataset: pd.DataFrame, attributes: list) -> pd.DataFrame:
    """
    This method converts a specific attribute from numerical/categorical into a binary one
    Args:
        dataset: the dataset on which we want to compute the attribute fixing
        attributes: the list of attributes to fix

    Returns:
        A dataset in which the specified attributes are converted into binary ones
    """
    for attribute in attributes:
        protected_attribute_value = []
        if len(dataset[attribute].values) == 2:
            max_value = dataset[attribute].max()
            for index, row in dataset.iterrows():
                if row[attribute] == max_value:
                    protected_attribute_value.append(1)
                else:
                    protected_attribute_value.append(0)
        else:
            threshold_value = (dataset[attribute].min() + dataset[attribute].max()) / 2
            for index, row in dataset.iterrows():
                if row[attribute] > threshold_value:
                    protected_attribute_value.append(1)
                else:
                    protected_attribute_value.append(0)

        dataset[attribute] = pd.Series(protected_attribute_value)
    return dataset


def remove_columns_from_dataset(dataset: pd.DataFrame, columns_to_drop: list) -> pd.DataFrame:
    """
    This method removes the specified columns from the specified dataset
    Args:
        dataset: The dataset from which to remove the specified columns
        columns_to_drop: The specified columns to remove

    Returns:
        The dataset without the specified columns

    """
    new_dataframe = dataset.drop(columns=[column for column in columns_to_drop])
    return new_dataframe


def categorical_to_numeric_converter(dataset: pd.DataFrame) -> pd.DataFrame:
    """
    This method converts the categorical attribute into numerical one
    Args:
        dataset: The dataset on which perform the computation

    Returns:
        Returns the dataset on which every categorical attribute has been converted into a numerical one

    """
    categorical_columns = [column for column in dataset.columns if dataset[column].dtype == "O"]
    label_encoder = LabelEncoder()
    for column in categorical_columns:
        dataset[column] = label_encoder.fit_transform(dataset[column])

    return dataset
