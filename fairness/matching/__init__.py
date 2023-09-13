from fairness.fairness_metric.fairness_evaluation import fairness_evaluation
from fairness.pre_processing import *
from fairness.proxy.proxy_processing import proxy_fixing


def conscious_fairness_through_unawareness(dataset: pd.DataFrame, protected_attributes: list,
                                           output_column_values: list,
                                           output_column: str, columns_to_drop=None) -> pd.DataFrame:
    """
    This method perform the search and removal of both proxy and protected attributes from the dataset
    returning a new fair dataset
    Args:
        dataset: the original dataset
        protected_attributes: the list of protected attributes
        output_column_values: the possible values for output columns
        output_column: the output column
        columns_to_drop: the list of column to drop

    Returns:
        the dataset without both proxies and protected attributes
    """
    if columns_to_drop is None:
        columns_to_drop = []
    numerical_dataset = categorical_to_numeric_converter(dataset)
    final_dataset = remove_columns_from_dataset(numerical_dataset, columns_to_drop)
    fixed_dataset = fix_protected_attributes(final_dataset, protected_attributes)
    evaluation = fairness_evaluation(fixed_dataset, protected_attributes,
                                     output_column_values, output_column)
    while evaluation == 'unfair':
        proxy_fixed_dataset = proxy_fixing(fixed_dataset, protected_attributes)
        if len(fixed_dataset.columns) == len(proxy_fixed_dataset.columns):
            fixed_dataset = remove_columns_from_dataset(proxy_fixed_dataset, protected_attributes)
            evaluation = 'fair'
        else:
            fixed_dataset = proxy_fixed_dataset
            new_protected_attributes = []
            for attr in protected_attributes:
                if attr in fixed_dataset.columns:
                    new_protected_attributes.append(attr)
            evaluation = fairness_evaluation(fixed_dataset, new_protected_attributes,
                                             output_column_values, output_column)

    return fixed_dataset
