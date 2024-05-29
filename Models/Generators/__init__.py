from abc import ABC, abstractmethod
from Models.RandomVariables import IRandomVariable, UniformRandomVariable

import numpy as np


class ARandomNumberGenerator(ABC):
    def __init__(self, randomVariable: IRandomVariable):
        self._randomVariable = randomVariable

    @abstractmethod
    def Get(self, N: int) -> np.array:
        pass


class SimpleRandomNumberGenerator(ARandomNumberGenerator):
    def __init__(self, randomVariable: IRandomVariable):
        super().__init__(randomVariable)

    def Get(self, N: int) -> np.array:
        us = np.random.uniform(0, 1, N)
        return np.vectorize(self._randomVariable.Quantile)(us)


class TukeyGenerator(ARandomNumberGenerator):
    def __init__(self, basicRandomVariable: IRandomVariable = UniformRandomVariable,
                 emissionsType: IRandomVariable = UniformRandomVariable,
                 symmetric: bool = True,
                 emissionsShare: float = 0.1):
        super().__init__(basicRandomVariable)
        self._emissionsType = emissionsType
        self._symmetric = symmetric
        self._emissionsShare = emissionsShare

    def _GenerateEmissions(self, a: float, b: float, N: int) -> np.array:
        rv = UniformRandomVariable(a, b)
        us = np.random.uniform(a, b, int(N * self._emissionsShare))
        return np.vectorize(rv.Quantile)(us)

    def _SymmetricalEmissionsSample(self, N: int) -> np.array:
        if self._emissionsType is UniformRandomVariable:
            location = self._randomVariable.GetLocation()
            a = np.random.randint(-abs(int(location) + 1) * 5, int(location))
            a = -1
            b = 2 * location - a
            print(a, b)
            return self._GenerateEmissions(a, b, N)
        else:
            raise TypeError

    def _AsymmetricalEmissionsSample(self, N: int) -> np.array:
        if self._emissionsType is UniformRandomVariable:
            scale = self._randomVariable.GetScale()
            a = 5
            b = a + scale
            return self._GenerateEmissions(a, b, N)
        else:
            raise TypeError

    def Get(self, N: int) -> np.array:
        emissionsSample = list()

        match self._symmetric:
            case True:
                emissionsSample = self._SymmetricalEmissionsSample(N)
            case False:
                emissionsSample = self._AsymmetricalEmissionsSample(N)

        sample = SimpleRandomNumberGenerator(self._randomVariable).Get(int((1 - self._emissionsShare) * N))
        sample1 = np.append(sample, emissionsSample)
        return sample1
