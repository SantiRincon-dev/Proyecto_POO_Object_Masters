# components/resistor.py
import numpy as np
from components.base import CircuitElement


class Resistor(CircuitElement):
    """
    Modelo de una resistencia ideal.

    En MNA la resistencia aporta su conductancia g = 1/R
    directamente a la matriz G. No aporta nada al vector b
    porque no es una fuente independiente.

    Stamp:
             nodo_pos   nodo_neg
    nodo_pos [  +g        -g   ]
    nodo_neg [  -g        +g   ]
    """

    def __init__(
        self, resistance: float, label: str = "", node_pos: int = 0, node_neg: int = 0
    ):
        if resistance <= 0:
            raise ValueError(
                f"La resistencia debe ser positiva, se recibió: {resistance}"
            )
        super().__init__(node_pos, node_neg, label)
        self._resistance = resistance

    # ── Propiedades ──────────────────────────────────────────────

    @property
    def resistance(self) -> float:
        return self._resistance

    @resistance.setter
    def resistance(self, value: float):
        if value <= 0:
            raise ValueError(f"La resistencia debe ser positiva, se recibió: {value}")
        self._resistance = value

    @property
    def conductance(self) -> float:
        """Conductancia g = 1/R en siemens. Solo lectura."""
        return 1.0 / self._resistance

    # ── Métodos abstractos implementados ─────────────────────────

    def stamp(self, G: np.ndarray, b: np.ndarray, node_map: dict, **kwargs) -> None:
        """
        Estampa la conductancia g = 1/R en la matriz G.
        No modifica b porque la resistencia no es una fuente.
        """
        i = node_map[self._node_pos]
        j = node_map[self._node_neg]
        g = self.conductance

        if i is not None:
            G[i][i] += g
            if j is not None:
                G[i][j] -= g

        if j is not None:
            G[j][j] += g
            if i is not None:
                G[j][i] -= g

    def get_current(self, x: np.ndarray, node_map: dict, **kwargs) -> float:
        """
        Calcula la corriente por la ley de Ohm: I = V / R = g * V.

        La corriente es positiva cuando fluye de node_pos a node_neg.
        """
        V = self.get_voltage(x, node_map)
        return V * self.conductance

    # ── Representación ────────────────────────────────────────────

    def __repr__(self) -> str:
        label = f" ({self._label})" if self._label else ""
        return (
            f"Resistor{label} [R={self._resistance}Ω, "
            f"n+={self._node_pos}, n-={self._node_neg}]"
        )
