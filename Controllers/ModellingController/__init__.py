from Models.Modelling import ModellingParameters, Modelling


class ModellingController:
    def __init__(self, parameters: ModellingParameters):
        self._modelling = Modelling(parameters)

    def EstimateMSE(self):
        return self._modelling.EstimateMSE()

    def GetSamples(self):
        return self._modelling.GetSamples()

    def Run(self):
        return self._modelling.Run()
