import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np

from tkinter import ttk

from Controllers.GeneratorsController import GeneratorsController, TukeyGeneratorController
from Controllers.RandomVariablesController import RandomVariablesController
from Controllers.SmoothedRandomVariableController import SmoothedRandomVariableController
from Controllers.ModellingController import ModellingController

from Models.RandomVariables import NonParametricRandomVariable
from Models.Estimations import HodgesLehman, HalfSumOfOrdinalStatistics


class MainWindow:
    def __init__(self):
        self._randomVariableController = None
        self._nonParametricRandomVariableController = None
        self._generatorController = None
        self._nonParametricGeneratorController = None
        self._estimationController = None
        self._smoothedRandomVariableController = None
        self._modellingRandomVariableController = None

        self._window = tk.Tk()
        self._window.title("Оценка параметра сдвига")

        self._emission = tk.IntVar(value=0)

        self._noEmissionsRadiobutton = ttk.Radiobutton(text="Без выбросов", value=0,
                                                       variable=self._emission, state="ACTIVE")
        self._noEmissionsRadiobutton.grid(column=1, row=4, padx=10, pady=10)

        self._symmetricEmissionsRadiobutton = ttk.Radiobutton(text="С симметричными выбросами",
                                                              value=1, variable=self._emission)
        self._symmetricEmissionsRadiobutton.grid(column=1, row=5, padx=10, pady=10)

        self._asymmetricEmissionsRadiobutton = ttk.Radiobutton(text="С асимметричными выбросами",
                                                               value=2, variable=self._emission)
        self._asymmetricEmissionsRadiobutton.grid(column=1, row=6, padx=10, pady=10)

        self._sampleLengthLabel = ttk.Label(self._window, text="N:")
        self._sampleLengthLabel.grid(column=1, row=1, padx=10, pady=10)

        self._sampleLengthEntry = ttk.Entry(self._window)
        self._sampleLengthEntry.grid(column=2, row=1, padx=10, pady=10)

        self._calculateButton = ttk.Button(self._window, text="Рассчитать", command=self._Calculate)
        self._calculateButton.grid(column=1, row=7, padx=10, columnspan=2)

    def _Calculate(self):
        a = 0
        b = 1
        n = int(self._sampleLengthEntry.get())
        points = n * 2
        orderLevels = [0, 0.1, 0.2, 0.3, 0.4, 0.5]

        self._randomVariableController = RandomVariablesController(a, b)
        self._generatorController = GeneratorsController(self._randomVariableController.GetRandomVariable())
        sample = self._generatorController.Get(n)
        self._nonParametricRandomVariableController = RandomVariablesController(
            sample, randomVariableType=NonParametricRandomVariable)

        match self._emission.get():
            case 0:
                self._nonParametricGeneratorController = GeneratorsController(
                    self._randomVariableController.GetRandomVariable())
                print("\n\nБез выбросов\n")
            case 1:
                self._nonParametricGeneratorController = TukeyGeneratorController(
                    self._randomVariableController.GetRandomVariable())
                print("\n\nС симметричными выбросами\n")
            case 2:
                self._nonParametricGeneratorController = TukeyGeneratorController(
                    self._randomVariableController.GetRandomVariable(), symmetric=False)
                print("\n\nС асимметричными выбросами\n")

        self._modellingRandomVariableController = ModellingController(
            self._nonParametricGeneratorController.GetGenerator(),
            [HalfSumOfOrdinalStatistics(orderLevel) for orderLevel in orderLevels],
            2 * n,
            n,
            self._randomVariableController.GetLocation())
        self._modellingRandomVariableController.Run()

        self._BuildPlot(points,
                        orderLevels,
                        self._modellingRandomVariableController.GetSamples(),
                        2)
        print("Оценка оптимального порядка")

        minHalfSumMSE = min(
            zip(orderLevels, self._modellingRandomVariableController.EstimateMSE()),
            key=lambda x: x[1])

        self._modellingRandomVariableController = ModellingController(
            self._nonParametricGeneratorController.GetGenerator(),
            [HodgesLehman(), HalfSumOfOrdinalStatistics(minHalfSumMSE[0])],
            2 * n,
            n,
            self._randomVariableController.GetLocation())

        self._modellingRandomVariableController.Run()

        self._BuildPlot(points,
                        ("Оценка Ходжеса-Лемана", "Полусумма порядковых статистик"),
                        self._modellingRandomVariableController.GetSamples())
        print("\nОценка параметра положения")

        self._modellingRandomVariableController.EstimateMSE()
        print(self._modellingRandomVariableController._modelling.GetConfInterval())
        print(min(self._modellingRandomVariableController._modelling.GetConfInterval(), key=lambda x: x[1] - x[0]))

        plt.show()

    def Run(self):
        self._window.mainloop()

    def _BuildPlot(self, points: int, legend: tuple, samples: np.array, plotIndex=1):
        plt.subplot(1, 2, plotIndex)

        for i in range(samples.shape[1]):
            sample = samples[:, i]
            x = np.linspace(min(sample), max(sample), points)
            self._smoothedRandomVariableController = SmoothedRandomVariableController(sample)
            y = np.vectorize(self._smoothedRandomVariableController.PDF)(x)
            plt.plot(x, y)

        plt.legend(legend)


if __name__ == "__main__":
    app = MainWindow()
    app.Run()
