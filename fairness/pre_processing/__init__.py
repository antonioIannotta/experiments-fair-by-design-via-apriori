import pandas as pd
from sklearn.preprocessing import LabelEncoder


def fix_protected_attributes(dataset: pd.DataFrame, protected_attributes: list) -> pd.DataFrame:
    """
    This method fixes the protected attributes in the dataset converting them into binary ones
    :param dataset: the dataset on which the protected attributes have to be fixed
    :param protected_attributes: the protected attributes that have to be fixed
    :return: returns the dataset with the protected attributes fixed
    """
    for protected_attribute in protected_attributes:
        mean_protected_attribute = dataset[protected_attribute].mean()
        for index, row in dataset.iterrows():
            if row[protected_attribute] > mean_protected_attribute:
                row[protected_attribute] = 1
            else:
                row[protected_attribute] = 0

    return dataset


def remove_columns_from_dataset(dataset: pd.DataFrame, columns_to_drop: list) -> pd.DataFrame:
    """
    The method removes the specified columns from the specified dataset
    :param dataset: the dataset from which the columns have to be dropped
    :param columns_to_drop: the columns to drop
    :return: returns a new dataset without the specified columns
    """
    new_dataframe = dataset.drop(columns=[column for column in columns_to_drop])
    return new_dataframe

def categorical_to_numeric_converter(dataset: pd.DataFrame) -> pd.DataFrame:
    """
    The method converts each categorical column into a numerical one
    :param dataset: the dataset on which pervorm the convertion
    :return: returns a dataset with all numerical attributes
    """
    categorical_columns = [column for column in dataset.columns if dataset[column].dtype=="O"]
    label_encoder = LabelEncoder()
    for column in categorical_columns:
        dataset[column] = label_encoder.fit_transform(dataset[column])

    return dataset
