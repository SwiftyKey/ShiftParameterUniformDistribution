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
        return statistics.median(sorted(HodgesLehman._WalshAverages(sample)))


class HalfSumOfOrdinalStatistics(IEstimation):
    def __init__(self, orderLevel: float):
        self._orderLevel = orderLevel

    def Value(self, sample: list) -> float:
        n = len(sample)
        sortedSample = sorted(sample)
        return (sortedSample[int(self._orderLevel * n)] + sortedSample[int((1 - self._orderLevel) * n) - 1]) / 2


class Variance(IEstimation):
    def Value(self, sample: list) -> float:
        return statistics.variance(sample)


class Mean(IEstimation):
    def Value(self, sample: list) -> float:
        return statistics.mean(sample)
