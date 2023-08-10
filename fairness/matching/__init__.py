from fairness.fairness_metric.disparate_impact import fairness_evaluation
from fairness.pre_processing import *
from fairness.proxy.proxy_processing import proxy_fixing


def conscious_fairness_through_unawareness(dataset: pd.DataFrame, protected_attributes: list,
                                           output_column_values: list,
                                           output_column: str, columns_to_drop=None,
                                           confidence_threshold: float = 0.8) -> pd.DataFrame:
    """
    This method compute the transformation of the dataset. It looks for proxy and, in case these ones are not founded it
    removes the protected attributes.
    """
    if columns_to_drop is None:
        columns_to_drop = []
    cnt = 0
    numerical_dataset = categorical_to_numeric_converter(dataset)
    final_dataset = remove_columns_from_dataset(numerical_dataset, columns_to_drop)
    fixed_dataset = fix_protected_attributes(final_dataset, protected_attributes)
    fairness_eval = fairness_evaluation(fixed_dataset, protected_attributes, output_column_values, output_column)
    print(fairness_eval)
    while fairness_eval == 'unfair':
        proxy_fixed_dataset = proxy_fixing(fixed_dataset, protected_attributes)
        if len(fixed_dataset.columns) == len(proxy_fixed_dataset.columns):
            fixed_dataset = remove_columns_from_dataset(proxy_fixed_dataset, protected_attributes)
            fairness_eval = 'fair'
        else:
            fixed_dataset = proxy_fixed_dataset
            new_protected_attributes = []
            for attr in protected_attributes:
                if attr in fixed_dataset.columns:
                    new_protected_attributes.append(attr)
            fairness_eval = fairness_evaluation(fixed_dataset, new_protected_attributes, output_column_values,
                                                output_column)

    return fixed_dataset
