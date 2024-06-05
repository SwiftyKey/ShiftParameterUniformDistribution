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

    def GetConfInterval(self, alpha=0.9) -> np.array:
        down = int(self._M * (1 - alpha) / 2)
        up = self._M - down - 1
        sortedSample = np.sort(self._estimationsSample, axis=0)
        reduceSample = np.apply_along_axis(lambda sample: sample[down:up], 0, sortedSample)
        confInterval = [[reduceSample[0, 0], reduceSample[-1, 0]],
                        [reduceSample[0, 1], reduceSample[-1, 1]]]
        return confInterval

    def _PrintMSE(self, biasSqr: np.array, variance: np.array, mse: np.array):
        for i in range(len(mse)):
            print(f"{biasSqr[i]:.10f}", end="	")
            print(f"{variance[i]:.10f}", end="	")
            print(f"{mse[i]:.10f}")

    # Метод, оценивающий СКО оценок
    def EstimateMSE(self) -> np.array:
        biasSqr = self._EstimateBiasSqr()
        variance = self._EstimateVariance()
        mse = biasSqr + variance
        self._PrintMSE(biasSqr, variance, mse)
        return mse

    def GetSamples(self):
        return self._estimationsSample

    def Run(self):
        for i in range(self._M):
            sample = self._GetSample()
            self._estimationsSample[i, :] = [estimation.Value(sample) for estimation in self._estimations]
