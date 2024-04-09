from Models.Estimations import IEstimation


class EstimationsController:
    @staticmethod
    def GetEstimationTypes():
        return {_type.__name__: _type for _type in IEstimation.__subclasses__()}

    def __init__(self, *args, estimationType: IEstimation):
        self._estimation = estimationType(*args)

    def Value(self, x: float) -> float:
        return self._estimation.Value(x)
