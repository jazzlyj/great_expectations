import logging
from typing import Dict, Optional

import numpy as np

from great_expectations.rule_based_profiler.domain import Domain
from great_expectations.rule_based_profiler.estimators.numeric_range_estimation_result import (
    NumericRangeEstimationResult,
)
from great_expectations.rule_based_profiler.estimators.numeric_range_estimator import (
    NumericRangeEstimator,
)
from great_expectations.rule_based_profiler.helpers.util import (
    build_numeric_range_estimation_result,
    datetime_semantic_domain_type,
)
from great_expectations.rule_based_profiler.parameter_container import (
    ParameterContainer,
)
from great_expectations.util import convert_ndarray_to_datetime_dtype_best_effort
from great_expectations.validator.computed_metric import MetricValue

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ExactNumericRangeEstimator(NumericRangeEstimator):
    """
    Implements deterministic, incorporating entire observed value range, computation.
    """

    def __init__(
        self,
    ) -> None:
        super().__init__(
            name="exact",
            configuration=None,
        )

    def _get_numeric_range_estimate(
        self,
        metric_values: np.ndarray,
        domain: Domain,
        variables: Optional[ParameterContainer] = None,
        parameters: Optional[Dict[str, ParameterContainer]] = None,
    ) -> NumericRangeEstimationResult:
        datetime_detected: bool = datetime_semantic_domain_type(domain=domain)
        metric_values_converted: np.ndaarray
        (
            _,
            _,
            metric_values_converted,
        ) = convert_ndarray_to_datetime_dtype_best_effort(
            data=metric_values,
            datetime_detected=datetime_detected,
            parse_strings_as_datetimes=True,
            fuzzy=False,
        )
        min_value: MetricValue = np.amin(a=metric_values_converted)
        max_value: MetricValue = np.amax(a=metric_values_converted)
        return build_numeric_range_estimation_result(
            metric_values=metric_values_converted,
            min_value=min_value,
            max_value=max_value,
        )
