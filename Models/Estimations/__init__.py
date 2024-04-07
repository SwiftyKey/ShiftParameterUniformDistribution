from abc import ABC, abstractmethod

import statistics


class IEstimation(ABC):
    @abstractmethod
    def Value(self, sample: list) -> float:
        pass


class HodgesLehman(IEstimation):
    @staticmethod
    def _WalshAverages(sample: list):
        return [(sample[i] + sample[j]) / 2 for i in range(len(sample)) for j in range(i)]

    def Value(self, sample: list) -> float:
        sortedWalshAverages = sorted(HodgesLehman._WalshAverages(sample))
        return statistics.median(sortedWalshAverages)


class HalfSumOfOrdinalStatistics(IEstimation):
    def __init__(self, orderLevel: float):
        self._orderLevel = orderLevel

    def Value(self, sample: list) -> float:
        n = len(sample)
        return (sample[int(self._orderLevel * n)] + sample[int((1 - self._orderLevel) * n)]) / 2


class Variance(IEstimation):
    def Value(self, sample: list) -> float:
        return statistics.variance(sample)
