from abc import ABC, abstractmethod

import pandas as pd


class GNDataValidator(ABC):
    @abstractmethod
    def validate(self, geomagnetic_df) -> None:
        raise NotImplementedError()


class GNDataValidatorImpl(GNDataValidator):
    # def validate
    def validate(self, geomagnetic_df: pd.DataFrame) -> None:
        pass
