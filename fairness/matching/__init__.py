from fairness.fairness_metric.disparate_impact import DisparateImpact
from fairness.pre_processing import *
from fairness.proxy.proxy_processing import proxy_fixing


def compute(dataset: pd.DataFrame, protected_attributes: list, output_column: str, confidence_threshold: float = 0.8) -> pd.DataFrame:
    """
    This method compute the transformation of the dataset. It looks for proxy and, in case these ones are not founded it
    removes the protected attributes.
    """
    cnt = 0
    fixed_dataset = fix_protected_attributes(dataset, protected_attributes)
    fairness_evaluation = DisparateImpact().fairness_evaluation(fixed_dataset, protected_attributes, output_column)
    while fairness_evaluation == 'unfair':
        cnt += 1
        print(cnt)
        proxy_fixed_dataset = proxy_fixing(fixed_dataset, protected_attributes)
        if len(fixed_dataset.columns) == len(proxy_fixed_dataset.columns):
            proxy_fixed_dataset = remove_columns_from_dataset(proxy_fixed_dataset, protected_attributes)
            fairness_evaluation = 'fair'
        else:
            protected_attributes = []
            for attr in protected_attributes:
                if attr in dataset.columns:
                    protected_attributes.append(attr)
            fairness_evaluation = DisparateImpact().fairness_evaluation(proxy_fixed_dataset, protected_attributes, output_column)

    return proxy_fixed_dataset
