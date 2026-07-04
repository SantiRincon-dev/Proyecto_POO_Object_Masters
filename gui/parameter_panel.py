import tkinter as tk
from tkinter import ttk

from gui.circuit_factory import CircuitFactory
from gui.config import SimulationConfig


class ParameterPanel(ttk.LabelFrame):
    DEFAULTS = {
        "resistance": "1000",
        "capacitance": "1e-6",
        "inductance": "0.01",
        "source_voltage": "5.0",
        "switch_close_time": "0.0",
        "initial_capacitor_voltage": "0.0",
        "initial_inductor_current": "0.0",
        "t_start": "0.0",
        "t_end": "0.005",
        "dt": "1e-6",
    }

    LABELS = {
        "resistance": "Resistencia R [ohm]",
        "capacitance": "Capacitancia C [F]",
        "inductance": "Inductancia L [H]",
        "source_voltage": "Fuente DC [V]",
        "switch_close_time": "Cierre switch [s]",
        "initial_capacitor_voltage": "Voltaje inicial C [V]",
        "initial_inductor_current": "Corriente inicial L [A]",
        "t_start": "Tiempo inicial [s]",
        "t_end": "Tiempo final [s]",
        "dt": "Paso dt [s]",
    }

    def __init__(self, master, on_simulate, on_clear, on_change=None):
        super().__init__(master, text="Parámetros", padding=12)
        self._on_simulate = on_simulate
        self._on_clear = on_clear
        self._on_change = on_change
        self._entries = {}
        self._circuit_type = tk.StringVar(value=CircuitFactory.RC_SERIES)

        self._build()

    def _build(self):
        ttk.Label(self, text="Circuito").grid(row=0, column=0, sticky="w", pady=4)
        circuit_combo = ttk.Combobox(
            self,
            textvariable=self._circuit_type,
            values=CircuitFactory.CIRCUIT_TYPES,
            state="readonly",
        )
        circuit_combo.grid(row=0, column=1, sticky="ew", pady=4)
        circuit_combo.bind("<<ComboboxSelected>>", self._handle_change)

        for row, key in enumerate(self.DEFAULTS, start=1):
            ttk.Label(self, text=self.LABELS[key]).grid(row=row, column=0, sticky="w", pady=4)
            entry = ttk.Entry(self)
            entry.insert(0, self.DEFAULTS[key])
            entry.grid(row=row, column=1, sticky="ew", pady=4)
            entry.bind("<KeyRelease>", self._handle_change)
            entry.bind("<FocusOut>", self._handle_change)
            self._entries[key] = entry

        button_frame = ttk.Frame(self)
        button_frame.grid(row=len(self.DEFAULTS) + 1, column=0, columnspan=2, sticky="ew", pady=(12, 0))
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

        ttk.Button(button_frame, text="Simular", command=self._on_simulate).grid(
            row=0, column=0, sticky="ew", padx=(0, 4)
        )
        ttk.Button(button_frame, text="Limpiar", command=self._on_clear).grid(
            row=0, column=1, sticky="ew", padx=(4, 0)
        )

        self.columnconfigure(1, weight=1)

    def get_config(self) -> SimulationConfig:
        values = {}
        for key, entry in self._entries.items():
            raw_value = entry.get().strip()
            if raw_value == "":
                raise ValueError(f"El campo '{self.LABELS[key]}' no puede estar vacío.")
            try:
                values[key] = float(raw_value)
            except ValueError as exc:
                raise ValueError(f"El campo '{self.LABELS[key]}' debe ser numérico.") from exc

        return SimulationConfig(circuit_type=self._circuit_type.get(), **values)

    def get_preview_data(self) -> dict:
        values = {"circuit_type": self._circuit_type.get()}
        for key, entry in self._entries.items():
            values[key] = entry.get().strip()
        return values

    def reset(self):
        self._circuit_type.set(CircuitFactory.RC_SERIES)
        for key, entry in self._entries.items():
            entry.delete(0, tk.END)
            entry.insert(0, self.DEFAULTS[key])
        self._notify_change()

    def _handle_change(self, _event=None):
        self._notify_change()

    def _notify_change(self):
        if self._on_change is not None:
            self._on_change(self.get_preview_data())
