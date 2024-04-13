from abc import ABC, abstractmethod

import numpy as np


class IRandomVariable(ABC):
    @abstractmethod
    def PDF(self, x: float) -> float:
        pass

    @abstractmethod
    def CDF(self, x: float) -> float:
        pass

    @abstractmethod
    def Quantile(self, alpha: float) -> float:
        pass

    @abstractmethod
    def GetLocation(self) -> float:
        pass

    @abstractmethod
    def GetScale(self) -> float:
        pass

    @staticmethod
    @abstractmethod
    def GetParametersName() -> tuple:
        pass


class UniformRandomVariable(IRandomVariable):
    def __init__(self, leftBoundary: float, rightBoundary: float):
        super().__init__()
        self._leftBoundary = leftBoundary
        self._rightBoundary = rightBoundary
        self._location = (leftBoundary + rightBoundary) / 2
        self._scale = rightBoundary - leftBoundary

    def PDF(self, x: float) -> float:
        return 1 / (self._rightBoundary - self._leftBoundary) if self._leftBoundary <= x <= self._rightBoundary else 0

    def CDF(self, x: float) -> float:
        if x < self._leftBoundary:
            return 0

        if self._leftBoundary <= x < self._rightBoundary:
            return (x - self._leftBoundary) / (self._rightBoundary - self._leftBoundary)

        return 1

    def Quantile(self, alpha: float) -> float:
        return self._leftBoundary + (self._rightBoundary - self._leftBoundary) * alpha

    def GetLocation(self) -> float:
        return self._location

    def GetScale(self) -> float:
        return self._scale

    @staticmethod
    def GetParametersName() -> tuple:
        return "a", "b"


class NonParametricRandomVariable(IRandomVariable):
    @staticmethod
    def _HeavisideFunction(x) -> bool:
        return x > 0

    def __init__(self, sourceSample: np.array):
        super().__init__()
        self._sample = sorted(sourceSample)

    def PDF(self, x: float) -> float:
        if x in self._sample:
            return float('inf')
        return 0

    def CDF(self, x: float) -> float:
        return np.mean(np.vectorize(NonParametricRandomVariable._HeavisideFunction)(x - self._sample))

    def Quantile(self, alpha: float) -> float:
        return self._sample[int(alpha * len(self._sample))]

    def GetLocation(self) -> float:
        raise NotImplementedError

    def GetScale(self) -> float:
        raise NotImplementedError

    def GetParametersName(self) -> tuple:
        raise NotImplementedError
