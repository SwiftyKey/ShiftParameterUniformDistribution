from Models.Generators import ARandomNumberGenerator, SimpleRandomNumberGenerator
from Models.RandomVariables import IRandomVariable


class GeneratorsController:
    def __init__(self, randomVariable: IRandomVariable,
                 generatorType: ARandomNumberGenerator = SimpleRandomNumberGenerator):
        self._generator = generatorType(randomVariable)
        self._sample = None

    def Get(self, n: int):
        if not self._sample:
            self._sample = self._generator.Get(n)
        return self._sample
