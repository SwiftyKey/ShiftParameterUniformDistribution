from abc import ABC, abstractmethod
from Models.RandomVariables import IRandomVariable

import numpy as np


class ARandomNumberGenerator(ABC):
    def __init__(self, randomVariable: IRandomVariable):
        self.randomVariable = randomVariable

    @abstractmethod
    def Get(self, n: int) -> np.array:
        pass


class SimpleRandomNumberGenerator(ARandomNumberGenerator):
    def __init__(self, randomVariable: IRandomVariable):
        super().__init__(randomVariable)

    def Get(self, n: int) -> np.array:
        us = np.random.uniform(0, 1, n)
        return np.vectorize(self.randomVariable.Quantile)(us)
