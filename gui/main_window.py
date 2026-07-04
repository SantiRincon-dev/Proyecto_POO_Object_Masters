import tkinter as tk
from tkinter import messagebox, ttk

from gui.circuit_preview import CircuitPreviewPanel
from gui.parameter_panel import ParameterPanel
from gui.plot_panel import PlotPanel
from gui.results_panel import ResultsPanel
from gui.simulation_runner import SimulationRunner


class MainWindow(ttk.Frame):
    def __init__(self, master, simulation_runner: SimulationRunner | None = None):
        super().__init__(master, padding=12)
        self._simulation_runner = simulation_runner or SimulationRunner()
        self._latest_result = None

        self._build()

    def _build(self):
        self._parameters = ParameterPanel(
            self,
            on_simulate=self._simulate,
            on_clear=self._clear,
            on_change=self._update_circuit_preview,
        )
        self._circuit_preview = CircuitPreviewPanel(self)
        self._results = ResultsPanel(self)
        self._plot_panel = PlotPanel(self)

        self._parameters.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=(0, 12))
        self._plot_panel.grid(row=0, column=1, sticky="nsew")
        self._circuit_preview.grid(row=0, column=2, sticky="nsew", padx=(12, 0))
        self._results.grid(row=1, column=1, columnspan=2, sticky="nsew", pady=(12, 0))

        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=3)
        self.rowconfigure(1, weight=2)
        self._update_circuit_preview(self._parameters.get_preview_data())

    def _simulate(self):
        try:
            config = self._parameters.get_config()
            result = self._simulation_runner.run(config)
        except Exception as exc:
            self._results.show_error(str(exc))
            messagebox.showerror("Error de simulación", str(exc))
            return

        self._latest_result = result
        self._results.show_summary(result.summary())
        self._plot_panel.show_result(result)

    def _clear(self):
        self._parameters.reset()
        self._results.clear()
        self._plot_panel.clear()
        self._latest_result = None

    def _update_circuit_preview(self, preview_data: dict):
        self._circuit_preview.show_preview(preview_data)


def create_main_window(root: tk.Tk) -> MainWindow:
    root.title("Simulador de Circuitos")
    root.geometry("1300x720")
    root.minsize(900, 600)
    window = MainWindow(root)
    window.pack(fill="both", expand=True)
    return window
