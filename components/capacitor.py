# components/capacitor.py
import numpy as np
from components.base import CircuitElement


class Capacitor(CircuitElement):
    """
    Modelo de un capacitor ideal.

    En MNA el capacitor se discretiza usando la aproximación de Euler
    hacia atrás, convirtiéndose en una conductancia equivalente geq = C/dt
    más una fuente de corriente Ieq = geq * V(t-1) que representa
    la energía almacenada del paso anterior.

    Stamp:
                 nodo_pos      nodo_neg
    nodo_pos  [ +C/dt          -C/dt  ]   [ +Ieq ]
    nodo_neg  [ -C/dt          +C/dt  ]   [ -Ieq ]

    Donde Ieq = (C/dt) * V(t-1)
    """

    def __init__(
        self,
        capacitance: float,
        initial_voltage: float = 0.0,
        label: str = "",
        node_pos: int = 0,
        node_neg: int = 0,
    ):
        if capacitance <= 0:
            raise ValueError(
                f"La capacitancia debe ser positiva, se recibió: {capacitance}"
            )
        super().__init__(node_pos, node_neg, label)
        self._capacitance = capacitance
        self._initial_voltage = initial_voltage
        self._V_prev = initial_voltage

    # ── Propiedades ──────────────────────────────────────────────

    @property
    def capacitance(self) -> float:
        return self._capacitance

    @capacitance.setter
    def capacitance(self, value: float):
        if value <= 0:
            raise ValueError(f"La capacitancia debe ser positiva, se recibió: {value}")
        self._capacitance = value

    @property
    def initial_voltage(self) -> float:
        return self._initial_voltage

    @initial_voltage.setter
    def initial_voltage(self, value: float):
        self._initial_voltage = value

    @property
    def V_prev(self) -> float:
        """Voltaje en el paso de tiempo anterior. Usado internamente por el solver."""
        return self._V_prev

    @V_prev.setter
    def V_prev(self, value: float):
        self._V_prev = value

    # ── Métodos abstractos implementados ─────────────────────────

    def stamp(self, G: np.ndarray, b: np.ndarray, node_map: dict, **kwargs) -> None:
        """
        Estampa la conductancia equivalente geq = C/dt en G
        y la corriente equivalente Ieq = geq * V(t-1) en b.

        Parámetros adicionales en kwargs:
            dt : float — paso de tiempo en segundos (obligatorio)
        """
        dt = kwargs.get("dt")
        if dt is None:
            raise ValueError("El capacitor requiere 'dt' en stamp().")
        if dt <= 0:
            raise ValueError(f"dt debe ser positivo, se recibió: {dt}")

        i = node_map[self._node_pos]
        j = node_map[self._node_neg]

        geq = self._capacitance / dt
        Ieq = geq * self._V_prev

        if i is not None:
            G[i][i] += geq
            if j is not None:
                G[i][j] -= geq

        if j is not None:
            G[j][j] += geq
            if i is not None:
                G[j][i] -= geq

        if i is not None:
            b[i] += Ieq
        if j is not None:
            b[j] -= Ieq

    def get_current(self, x: np.ndarray, node_map: dict, **kwargs) -> float:
        """
        Calcula la corriente del capacitor: I = geq * V(t) - Ieq.

        Parámetros adicionales en kwargs:
            dt : float — paso de tiempo en segundos (obligatorio)
        """
        dt = kwargs.get("dt")
        if dt is None:
            raise ValueError("El capacitor requiere 'dt' en get_current().")

        V = self.get_voltage(x, node_map)
        geq = self._capacitance / dt
        Ieq = geq * self._V_prev
        return geq * V - Ieq

    def update_state(self, x: np.ndarray, node_map: dict) -> None:
        """
        Actualiza V_prev con el voltaje del paso actual.
        El solver llama este método al final de cada paso de tiempo.
        """
        self._V_prev = self.get_voltage(x, node_map)

    def reset(self) -> None:
        """Reinicia el capacitor a su condición inicial."""
        self._V_prev = self._initial_voltage

    # ── Representación ────────────────────────────────────────────

    def __repr__(self) -> str:
        label = f" ({self._label})" if self._label else ""
        return (
            f"Capacitor{label} [C={self._capacitance}F, "
            f"V0={self._initial_voltage}V, "
            f"n+={self._node_pos}, n-={self._node_neg}]"
        )
