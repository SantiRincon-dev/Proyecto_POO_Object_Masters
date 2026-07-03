from tkinter import ttk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


class PlotPanel(ttk.LabelFrame):
    def __init__(self, master):
        super().__init__(master, text="Gráfica", padding=8)
        self._canvas = None
        self._toolbar = None
        self._figure = None

        self._empty_label = ttk.Label(self, text="Ejecute una simulación para ver la gráfica.")
        self._empty_label.pack(expand=True)

    def show_result(self, result):
        self.clear()
        self._empty_label.pack_forget()
        self._figure = self._build_figure(result)
        self._canvas = FigureCanvasTkAgg(self._figure, master=self)
        self._canvas.draw()

        canvas_widget = self._canvas.get_tk_widget()
        canvas_widget.pack(fill="both", expand=True)

        self._toolbar = NavigationToolbar2Tk(self._canvas, self, pack_toolbar=False)
        self._toolbar.update()
        self._toolbar.pack(fill="x")

    def clear(self):
        if self._canvas is not None:
            self._canvas.get_tk_widget().destroy()
            self._canvas = None
        if self._toolbar is not None:
            self._toolbar.destroy()
            self._toolbar = None
        if self._figure is not None:
            plt.close(self._figure)
            self._figure = None
        self._empty_label.pack_forget()
        self._empty_label.pack(expand=True)

    def _build_figure(self, result):
        labels = result.labels
        figure, axes = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
        ax_voltage, ax_current = axes

        for label in labels:
            ax_voltage.plot(result.time, result.get_voltage(label), label=label, linewidth=1.8)
            ax_current.plot(result.time, result.get_current(label), label=label, linewidth=1.8)

        ax_voltage.set_title("Voltaje vs Tiempo")
        ax_voltage.set_ylabel("Voltaje [V]")
        ax_voltage.grid(True)
        ax_voltage.legend(loc="best")

        ax_current.set_title("Corriente vs Tiempo")
        ax_current.set_xlabel("Tiempo [s]")
        ax_current.set_ylabel("Corriente [A]")
        ax_current.grid(True)
        ax_current.legend(loc="best")

        figure.tight_layout()
        return figure
