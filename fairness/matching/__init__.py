from fairness.fairness_metric.fairness_evaluation import fairness_evaluation
from fairness.pre_processing import *
from fairness.proxy import *


def conscious_fairness_through_unawareness(dataset: pd.DataFrame, protected_attributes: list,
                                           output_column_values: list,
                                           output_column: str, columns_to_drop=None,
                                           confidence_threshold: float = 0.8) -> pd.DataFrame:
    """
    This method performs the proxy and protected attributes removal
    Args:
        dataset:
        protected_attributes:
        output_column_values:
        output_column:
        columns_to_drop:
        confidence_threshold:

    Returns:
        The new fair dataset
    """
    if columns_to_drop is None:
        columns_to_drop = []

    numerical_dataset = categorical_to_numeric_converter(dataset)
    final_dataset = remove_columns_from_dataset(numerical_dataset, columns_to_drop)
    fixed_dataset = fix_attributes(final_dataset, protected_attributes)
    fairness_eval = fairness_evaluation(fixed_dataset, protected_attributes, output_column_values, output_column)

    while fairness_eval == 'unfair':
        proxy_list = proxy_detection(dataset, protected_attributes)
        proxy_fixed_dataset = dataset.drop(columns=proxy_list)
        if len(fixed_dataset.columns) == len(proxy_fixed_dataset.columns):
            fixed_dataset = remove_columns_from_dataset(proxy_fixed_dataset, protected_attributes)
            fairness_eval = 'fair'
        else:
            fixed_dataset = proxy_fixed_dataset
            new_protected_attributes = []
            for protected_attribute in protected_attributes:
                if protected_attribute in fixed_dataset.columns:
                    new_protected_attributes.append(protected_attribute)

            fairness_eval = fairness_evaluation(fixed_dataset, new_protected_attributes, output_column_values,
                                                output_column)

    return fixed_dataset
