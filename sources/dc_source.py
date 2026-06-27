# sources/dc_source.py
import numpy as np
from sources.base import Source


class DCVoltageSource(Source):
    """
    Modelo de una fuente de tensión DC ideal.

    Impone un voltaje fijo entre node_pos y node_neg.
    En MNA introduce una variable extra I_s (current_var_idx)
    que representa la corriente entregada por la fuente.

    Stamp (k = current_var_idx):
                 nodo_pos   nodo_neg     k
    nodo_pos  [    0          0         +1  ]   [  0  ]
    nodo_neg  [    0          0         -1  ]   [  0  ]
    k         [   +1         -1          0  ]   [  Vs ]
    """

    def __init__(
        self, voltage: float, label: str = "", node_pos: int = 0, node_neg: int = 0
    ):
        if voltage < 0:
            raise ValueError(
                f"El voltaje DC debe ser no negativo, se recibió: {voltage}"
            )
        super().__init__(node_pos, node_neg, label)
        self._voltage = voltage

    # ── Propiedades ──────────────────────────────────────────────

    @property
    def voltage(self) -> float:
        return self._voltage

    @voltage.setter
    def voltage(self, value: float):
        if value < 0:
            raise ValueError(f"El voltaje DC debe ser no negativo, se recibió: {value}")
        self._voltage = value

    # ── Métodos abstractos implementados ─────────────────────────

    def stamp(self, G: np.ndarray, b: np.ndarray, node_map: dict, **kwargs) -> None:
        """
        Estampa la fuente DC en G y b.
        La fila k impone la restricción V[node_pos] - V[node_neg] = Vs.
        """
        self._check_current_var_idx()

        i = node_map[self._node_pos]
        j = node_map[self._node_neg]
        k = self._current_var_idx

        if i is not None:
            G[i][k] += 1
            G[k][i] += 1

        if j is not None:
            G[j][k] -= 1
            G[k][j] -= 1

        b[k] += self._voltage

    def get_current(self, x: np.ndarray, node_map: dict = None, **kwargs) -> float:
        self._check_current_var_idx()
        return -float(x[self._current_var_idx])

    def get_voltage(self, x: np.ndarray = None, node_map: dict = None) -> float:
        return float(self._voltage)

    # ── Representación ────────────────────────────────────────────

    def __repr__(self) -> str:
        label = f" ({self._label})" if self._label else ""
        return (
            f"DCVoltageSource{label} [V={self._voltage}V, "
            f"n+={self._node_pos}, n-={self._node_neg}]"
        )
