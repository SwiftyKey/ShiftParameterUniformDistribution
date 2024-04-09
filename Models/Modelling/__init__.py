from Models.Generators import ARandomNumberGenerator
from Models.Estimations import *

import numpy as np


class Modelling(ABC):
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

        # Здесь будут храниться выборки оценок
        self._estimationsSample = np.zeros((self._M, len(self._estimations)), dtype=np.float64)

    # Метод, оценивающий квадрат смещения оценок
    def EstimateBiasSqr(self):
        return np.array([(Mean().Value(self._estimationsSample[:, i]) - self._truthValue) ** 2 for i in
                         range(len(self._estimations))])

    # Метод, оценивающий дисперсию оценок
    def EstimateVariance(self):
        return np.array([Variance().Value(self._estimationsSample[:, i]) for i in range(len(self._estimations))])

    # Метод, оценивающий СКО оценок
    def EstimateMSE(self):
        return self.EstimateBiasSqr() + self.EstimateVariance()

    def GetSamples(self):
        return self._estimationsSample

    def GetSample(self):
        return self._generator.Get(self._N)

    def Run(self):
        for i in range(self._M):
            sample = self.GetSample()
            self._estimationsSample[i, :] = [estimation.Value(sample) for estimation in self._estimations]
