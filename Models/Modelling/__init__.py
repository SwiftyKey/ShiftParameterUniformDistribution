from Models.Generators import ARandomNumberGenerator
from Models.Estimations import *

import numpy as np


class ModellingParameters:
    def __init__(self,
                 generator: ARandomNumberGenerator,
                 estimations: list[IEstimation],
                 M: int,
                 N: int,
                 truthValue: float):
        self._generator = generator
        self._estimations = estimations
        self._M = M
        self._N = N
        self._truthValue = truthValue

    def Get(self) -> tuple:
        return self._generator, self._estimations, self._M, self._N, self._truthValue


class Modelling:
    def __init__(self, parameters: ModellingParameters):
        self._generator, self._estimations, self._M, self._N, self._truthValue = parameters.Get()

        # Здесь будут храниться выборки оценок
        self._estimationsSample = np.zeros((self._M, len(self._estimations)), dtype=np.float64)

    # Метод, оценивающий квадрат смещения оценок
    def _EstimateBiasSqr(self) -> np.array:
        return np.array([(Mean().Value(self._estimationsSample[:, i]) - self._truthValue) ** 2 for i in
                         range(len(self._estimations))])

    # Метод, оценивающий дисперсию оценок
    def _EstimateVariance(self) -> np.array:
        return np.array([Variance().Value(self._estimationsSample[:, i]) for i in range(len(self._estimations))])

    def _GetSample(self) -> np.array:
        return self._generator.Get(self._N)

    # Метод, оценивающий СКО оценок
    def EstimateMSE(self) -> np.array:
        return self._EstimateBiasSqr() + self._EstimateVariance()

    def GetSamples(self):
        return self._estimationsSample

    def Run(self):
        for i in range(self._M):
            sample = self._GetSample()
            self._estimationsSample[i, :] = [estimation.Value(sample) for estimation in self._estimations]
