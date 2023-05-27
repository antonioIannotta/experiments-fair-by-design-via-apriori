from fairness.fairness_metric.disparate_impact import DisparateImpact
from fairness.pre_processing import *
from fairness.proxy.proxy_processing import proxy_fixing


def compute(dataset: pd.DataFrame, protected_attributes: list, output_column: str, confidence_threshold: float = 0.8) -> pd.DataFrame:
    """
    This method compute the transformation of the dataset. It looks for proxy and, in case these ones are not founded it
    removes the protected attributes.
    """
    dataset = fix_protected_attributes(dataset, protected_attributes)
    while DisparateImpact().fairness_evaluation(dataset, protected_attributes, output_column) == 'unfair':
        proxy_fixed_dataset = proxy_fixing(dataset, protected_attributes)
        if dataset.columns == proxy_fixed_dataset.columns:
            dataset = remove_columns_from_dataset(dataset, protected_attributes)
            return dataset
        else:
            dataset = proxy_fixed_dataset
