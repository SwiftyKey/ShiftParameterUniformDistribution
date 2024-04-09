from Models.RandomVariables import IRandomVariable


class RandomVariablesController:
    def __init__(self, randomVariableType: IRandomVariable, *args):
        self._randomVariable = randomVariableType(*args)

    def PDF(self, *args) -> float:
        return self._randomVariable.PDF(*args)

    def CDF(self, *args) -> float:
        return self._randomVariable.CDF(*args)

    def Quantile(self, *args) -> float:
        return self._randomVariable.Quantile(*args)

    @staticmethod
    def GetParametersName(randomVariableType: IRandomVariable) -> tuple:
        return randomVariableType.GetParametersName()

    @staticmethod
    def GetAllRandomVariableTypes() -> list:
        return IRandomVariable.__subclasses__()

    def GetRandomVariable(self) -> IRandomVariable:
        return self._randomVariable
