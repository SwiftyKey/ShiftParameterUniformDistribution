from Models.SmoothedRandomVariable import SmoothedRandomVariable


class SmoothedRandomVariableController:
    def __init__(self, sample):
        self._smoothedRandomVariable = SmoothedRandomVariable(sample)

    def PDF(self, x: float) -> float:
        return self._smoothedRandomVariable.PDF(x)

    def CDF(self, x: float) -> float:
        return self._smoothedRandomVariable.CDF(x)

    def GetBandwidth(self) -> float:
        return self._smoothedRandomVariable.GetBandwidth()

    @staticmethod
    def GetParametersName() -> tuple:
        return SmoothedRandomVariable.GetParametersName()
