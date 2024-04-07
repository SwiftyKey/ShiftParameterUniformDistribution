import math

from Models.RandomVariables import IRandomVariable
from Models.Estimations import IEstimation

import numpy as np


class SmoothedRandomVariable(IRandomVariable, IEstimation):
    @staticmethod
    def _dk(x: float) -> float:
        return -x * SmoothedRandomVariable._k(x)

    @staticmethod
    def _k(x: float) -> float:
        return math.exp(-0.5 * x * x) / math.sqrt(2 * math.pi)

    @staticmethod
    def _K(x: float) -> float:
        if x <= 0:
            return 0.852 * math.exp(-math.pow((-x + 1.5774) / 2.0637, 2.34))
        return 1 - 0.852 * math.exp(-math.pow((x + 1.5774) / 2.0637, 2.34))

    @staticmethod
    def _CalculateOptimalBandwidth(arr: np.array, eps=0.01) -> float:
        def iteration(prev_h: float):
            result = 0
            size = len(arr)

            for i in range(size):
                numerator = 0
                denominator = 0

                for j in range(size):
                    if i != j:
                        numerator += SmoothedRandomVariable._dk((arr[i] - arr[j]) / prev_h) * (arr[i] - arr[j])
                        denominator += SmoothedRandomVariable._k((arr[i] - arr[j]) / prev_h)

                if denominator != 0:
                    result += numerator / denominator

            return -result / size

        prev_h = 0.1
        cur_h = iteration(prev_h)

        while abs(cur_h - prev_h) <= eps:
            cur_h, prev_h = iteration(prev_h), cur_h

        return cur_h

    def __init__(self, sample: np.array):
        self._sample = sample
        self._bandwidth = SmoothedRandomVariable._CalculateOptimalBandwidth(sample)

    def PDF(self, x: float) -> float:
        return np.mean([SmoothedRandomVariable._k((x - y) / self._bandwidth) for y in self._sample]) / self._bandwidth

    def CDF(self, x: float) -> np.ndarray:
        return np.mean([SmoothedRandomVariable._K((x - y) / self._bandwidth) for y in self._sample])

    def Quantile(self, alpha: float) -> float:
        raise NotImplementedError

    def Value(self, value: float):
        raise NotImplementedError

    def GetBandwidth(self) -> float:
        return self._bandwidth

    @staticmethod
    def GetParametersName() -> tuple:
        return ("bandwidth",)
