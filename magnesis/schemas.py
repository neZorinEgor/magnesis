from dataclasses import dataclass
from typing import Union

import numpy as np
from numpy.typing import NDArray


@dataclass(kw_only=True, slots=True)
class GeomagnesisResult:
    """Результаты инференса геомагнитной модели"""

    dst_ci_lower: NDArray
    dst_ci_upper: NDArray
    ae_ci_lower: NDArray
    ae_ci_upper: NDArray
    dst_labels: NDArray
    dst_preds: NDArray
    ae_labels: NDArray
    ae_preds: NDArray
    dst_rmse: Union[float, np.float64]
    ae_rmse: Union[float, np.float64]
    dst_std: Union[float, np.float64]
    ae_std: Union[float, np.float64]
