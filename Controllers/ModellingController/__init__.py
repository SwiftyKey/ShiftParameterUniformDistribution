from Models.Generators import ARandomNumberGenerator
from Models.Modelling import ModellingParameters, Modelling
from Models.Estimations import IEstimation


class ModellingController:
    def __init__(self,
                 generator: ARandomNumberGenerator,
                 estimations: list[IEstimation],
                 M: int,
                 N: int,
                 truthValue: float):
        self._modelling = Modelling(ModellingParameters(generator,
                                                        estimations,
                                                        M,
                                                        N,
                                                        truthValue))

    def EstimateMSE(self):
        return self._modelling.EstimateMSE()

    def GetSamples(self):
        return self._modelling.GetSamples()

    def Run(self):
        return self._modelling.Run()
