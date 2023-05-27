from fairness.fairness_metric.disparate_impact import DisparateImpact
from fairness.pre_processing import *
from fairness.proxy.proxy_processing import proxy_fixing


def compute(dataset: pd.DataFrame, protected_attributes: list, confidence_threshold: float) -> pd.DataFrame:
    dataset = fix_protected_attributes(dataset, protected_attributes)
    while DisparateImpact().fairness_evaluation(dataset, protected_attributes) == 'unfair':
        dataset = proxy_fixing(dataset, protected_attributes)

    return dataset
