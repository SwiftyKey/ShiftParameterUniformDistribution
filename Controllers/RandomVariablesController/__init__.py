from Models.RandomVariables import IRandomVariable, UniformRandomVariable


class RandomVariablesController:
    def __init__(self, *args, randomVariableType: IRandomVariable = UniformRandomVariable):
        self._randomVariable = randomVariableType(*args)

    def PDF(self, *args) -> float:
        return self._randomVariable.PDF(*args)

    def CDF(self, *args) -> float:
        return self._randomVariable.CDF(*args)

    def Quantile(self, *args) -> float:
        return self._randomVariable.Quantile(*args)

    def GetLocation(self) -> float:
        return self._randomVariable.GetLocation()

    def GetScale(self) -> float:
        return self._randomVariable.GetScale()

    @staticmethod
    def GetParametersName(randomVariableType: IRandomVariable) -> tuple:
        return randomVariableType.GetParametersName()

    @staticmethod
    def GetAllRandomVariableTypes() -> list:
        return IRandomVariable.__subclasses__()

    def GetRandomVariable(self) -> IRandomVariable:
        return self._randomVariable
