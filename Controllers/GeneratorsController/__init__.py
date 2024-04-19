from Models.Generators import ARandomNumberGenerator, SimpleRandomNumberGenerator, TukeyGenerator
from Models.RandomVariables import IRandomVariable, UniformRandomVariable


class GeneratorsController:
    def __init__(self, randomVariable: IRandomVariable = UniformRandomVariable,
                 generatorType: ARandomNumberGenerator = SimpleRandomNumberGenerator):
        self._generator = generatorType(randomVariable)
        self._sample = None

    def Get(self, N: int) -> list:
        if not self._sample:
            self._sample = self._generator.Get(N)
        return self._sample

    def GetGenerator(self) -> ARandomNumberGenerator:
        return self._generator


class TukeyGeneratorController:
    def __init__(self, basicRandomVariable: IRandomVariable = UniformRandomVariable,
                 emissionsType: IRandomVariable = UniformRandomVariable,
                 symmetric: bool = True,
                 emissionsShare: float = 0.1):
        self._generator = TukeyGenerator(basicRandomVariable, emissionsType, symmetric, emissionsShare)
        self._sample = None

    def Get(self, N: int) -> list:
        if not self._sample:
            self._sample = self._generator.Get(N)
        return self._sample

    def GetGenerator(self) -> ARandomNumberGenerator:
        return self._generator
