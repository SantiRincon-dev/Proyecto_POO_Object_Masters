# simulation/sim_result.py
import numpy as np


class SimResult:
    """
    Almacena y organiza los resultados de una simulación.

    Contiene los vectores de tiempo, voltaje y corriente
    para cada elemento del circuito, y provee métodos
    para consultar y resumir los resultados.

    Parámetros:
        time     : np.ndarray — vector de tiempo en segundos
        voltages : dict       — {label: np.ndarray} voltajes por elemento
        currents : dict       — {label: np.ndarray} corrientes por elemento
    """

    def __init__(self, time: np.ndarray, voltages: dict, currents: dict):
        if not isinstance(time, np.ndarray):
            raise TypeError(f"time debe ser un np.ndarray, se recibió: {type(time)}")
        if not isinstance(voltages, dict):
            raise TypeError(f"voltages debe ser un dict, se recibió: {type(voltages)}")
        if not isinstance(currents, dict):
            raise TypeError(f"currents debe ser un dict, se recibió: {type(currents)}")

        self._time = time
        self._voltages = voltages
        self._currents = currents

    # ── Propiedades ──────────────────────────────────────────────

    @property
    def time(self) -> np.ndarray:
        return self._time

    @property
    def voltages(self) -> dict:
        return self._voltages

    @property
    def currents(self) -> dict:
        return self._currents

    @property
    def labels(self) -> list:
        """Lista de etiquetas de los elementos en el resultado."""
        return list(self._voltages.keys())

    @property
    def t_end(self) -> float:
        """Tiempo final de la simulación."""
        return float(self._time[-1])

    @property
    def t_start(self) -> float:
        """Tiempo inicial de la simulación."""
        return float(self._time[0])

    @property
    def dt(self) -> float:
        """Paso de tiempo de la simulación."""
        if len(self._time) < 2:
            return 0.0
        return float(self._time[1] - self._time[0])

    # ── Métodos de consulta ───────────────────────────────────────

    def get_voltage(self, label: str) -> np.ndarray:
        """
        Retorna el vector de voltaje de un elemento por su etiqueta.

        Parámetros:
            label : str — etiqueta del elemento

        Retorna:
            np.ndarray con el voltaje en cada paso de tiempo
        """
        if label not in self._voltages:
            raise KeyError(
                f"No se encontró el elemento '{label}'. "
                f"Elementos disponibles: {self.labels}"
            )
        return self._voltages[label]

    def get_current(self, label: str) -> np.ndarray:
        """
        Retorna el vector de corriente de un elemento por su etiqueta.

        Parámetros:
            label : str — etiqueta del elemento

        Retorna:
            np.ndarray con la corriente en cada paso de tiempo
        """
        if label not in self._currents:
            raise KeyError(
                f"No se encontró el elemento '{label}'. "
                f"Elementos disponibles: {self.labels}"
            )
        return self._currents[label]

    def get_power(self, label: str) -> np.ndarray:
        """
        Calcula la potencia instantánea de un elemento: P = V * I.

        Parámetros:
            label : str — etiqueta del elemento

        Retorna:
            np.ndarray con la potencia en cada paso de tiempo
        """
        return self.get_voltage(label) * self.get_current(label)

    # ── Métodos de resumen ────────────────────────────────────────

    def summary(self) -> str:
        """
        Genera un resumen de los resultados de la simulación.

        Retorna:
            str con los valores máximos, mínimos y finales
            de voltaje y corriente por elemento.
        """
        lines = []
        lines.append("=" * 52)
        lines.append("         RESUMEN DE SIMULACIÓN")
        lines.append("=" * 52)
        lines.append(f"  Tiempo: {self.t_start:.4f}s → {self.t_end:.4f}s")
        lines.append(f"  Paso:   {self.dt:.2e}s")
        lines.append(f"  Pasos:  {len(self._time)}")
        lines.append("-" * 52)

        for label in self.labels:
            v = self._voltages[label]
            i = self._currents[label]
            lines.append(f"\n  [{label}]")
            lines.append(
                f"  Voltaje  → max: {v.max():.4f}V  "
                f"min: {v.min():.4f}V  "
                f"final: {v[-1]:.4f}V"
            )
            lines.append(
                f"  Corriente→ max: {i.max():.4f}A  "
                f"min: {i.min():.4f}A  "
                f"final: {i[-1]:.4f}A"
            )

        lines.append("\n" + "=" * 52)
        return "\n".join(lines)

    def to_dataframe(self):
        """
        Convierte los resultados a un DataFrame de pandas.
        Útil para exportar o analizar los datos externamente.

        Retorna:
            pandas.DataFrame con columnas:
            time, V_label1, I_label1, V_label2, I_label2, ...
        """
        try:
            import pandas as pd
        except ImportError:
            raise ImportError(
                "pandas no está instalado. Instálalo con: pip install pandas"
            )

        data = {"time": self._time}
        for label in self.labels:
            data[f"V_{label}"] = self._voltages[label]
            data[f"I_{label}"] = self._currents[label]

        return pd.DataFrame(data)

    # ── Representación ────────────────────────────────────────────

    def __repr__(self) -> str:
        return (
            f"SimResult ["
            f"t={self.t_start:.4f}s → {self.t_end:.4f}s, "
            f"dt={self.dt:.2e}s, "
            f"elementos={self.labels}]"
        )
