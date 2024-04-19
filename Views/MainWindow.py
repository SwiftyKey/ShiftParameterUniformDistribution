import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np

from tkinter import ttk

from Controllers.GeneratorsController import GeneratorsController, TukeyGeneratorController
from Controllers.EstimationsController import EstimationsController
from Controllers.RandomVariablesController import RandomVariablesController
from Controllers.SmoothedRandomVariableController import SmoothedRandomVariableController
from Controllers.ModellingController import ModellingController

from Models.Generators import TukeyGenerator
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

        self._emission = tk.IntVar()

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

        self._leftBoundaryLabel = ttk.Label(self._window, text="a: ")
        self._leftBoundaryLabel.grid(column=1, row=2, padx=10, pady=10)

        self._leftBoundaryEntry = ttk.Entry(self._window)
        self._leftBoundaryEntry.grid(column=2, row=2, padx=10, pady=10)

        self._rightBoundaryLabel = ttk.Label(self._window, text="b: ")
        self._rightBoundaryLabel.grid(column=1, row=3, padx=10, pady=10)

        self._rightBoundaryEntry = ttk.Entry(self._window)
        self._rightBoundaryEntry.grid(column=2, row=3, padx=10, pady=10)

        self._calculateButton = ttk.Button(self._window, text="Рассчитать", command=self.Calculate)
        self._calculateButton.grid(column=1, row=7, padx=10, columnspan=2)

    def Calculate(self):
        a = float(self._leftBoundaryEntry.get())
        b = float(self._rightBoundaryEntry.get())
        n = int(self._sampleLengthEntry.get())

        self._randomVariableController = RandomVariablesController(a, b)
        self._generatorController = GeneratorsController(self._randomVariableController.GetRandomVariable())
        sample = self._generatorController.Get(n)
        self._nonParametricRandomVariableController = RandomVariablesController(
            sample, randomVariableType=NonParametricRandomVariable)

        match self._emission:
            case 0:
                self._nonParametricGeneratorController = GeneratorsController(
                    self._nonParametricRandomVariableController.GetRandomVariable())
                print("Без выбросов")
            case 1:
                self._nonParametricGeneratorController = TukeyGeneratorController(
                    self._nonParametricRandomVariableController.GetRandomVariable())
                print("С симметричными выбросами")
            case 2:
                self._nonParametricGeneratorController = TukeyGeneratorController(
                    self._nonParametricRandomVariableController.GetRandomVariable(), symmetric=False)
                print("С асимметричными выбросами")

        self._modellingRandomVariableController = ModellingController(
            self._nonParametricGeneratorController.GetGenerator(),
            [HodgesLehman, HalfSumOfOrdinalStatistics],
            2 * n,
            n,
            self._randomVariableController.GetLocation())

        self._modellingRandomVariableController.Run()

        samples = self._modellingRandomVariableController.GetSamples()
        point = 100

    def Run(self):
        self._window.mainloop()

    @staticmethod
    def BuildPlot(xs, ys, colors, plotIndex=0):
        plt.subplot(2, 1, plotIndex + 1)
        for x, y, color in zip(xs, ys, colors):
            plt.plot(x, y, color)


if __name__ == "__main__":
    app = MainWindow()
    app.Run()
