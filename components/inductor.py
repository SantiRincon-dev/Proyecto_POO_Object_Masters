# components/inductor.py
import numpy as np
from components.base import CircuitElement


class Inductor(CircuitElement):
    """
    Modelo de un inductor ideal.

    A diferencia del capacitor, el inductor no puede representarse
    como una conductancia equivalente simple porque su variable natural
    es la corriente y no el voltaje. Por esto MNA introduce una variable
    extra I_L en el vector solución x, similar a como lo hace la fuente
    de voltaje.

    Con la aproximación de Euler hacia atrás:
        V(t) = L * (I_L(t) - I_L(t-1)) / dt

    Reordenando:
        V(t) - (L/dt) * I_L(t) = -(L/dt) * I_L(t-1)

    Stamp (k = current_var_idx):
                 nodo_pos   nodo_neg     k
    nodo_pos  [    0          0         +1  ]   [      0       ]
    nodo_neg  [    0          0         -1  ]   [      0       ]
    k         [   +1         -1       -L/dt ]   [ -(L/dt)*I(t-1) ]
    """

    def __init__(
        self,
        inductance: float,
        initial_current: float = 0.0,
        label: str = "",
        node_pos: int = 0,
        node_neg: int = 0,
    ):
        if inductance <= 0:
            raise ValueError(
                f"La inductancia debe ser positiva, se recibió: {inductance}"
            )
        super().__init__(node_pos, node_neg, label)
        self._inductance = inductance
        self._initial_current = initial_current
        self._I_prev = initial_current
        self._current_var_idx = None

    # ── Propiedades ──────────────────────────────────────────────

    @property
    def inductance(self) -> float:
        return self._inductance

    @inductance.setter
    def inductance(self, value: float):
        if value <= 0:
            raise ValueError(f"La inductancia debe ser positiva, se recibió: {value}")
        self._inductance = value

    @property
    def initial_current(self) -> float:
        return self._initial_current

    @initial_current.setter
    def initial_current(self, value: float):
        self._initial_current = value

    @property
    def current_var_idx(self) -> int:
        return self._current_var_idx

    @current_var_idx.setter
    def current_var_idx(self, value: int):
        if not isinstance(value, int) or value < 0:
            raise ValueError(
                f"current_var_idx debe ser un entero no negativo, se recibió: {value}"
            )
        self._current_var_idx = value

    @property
    def I_prev(self) -> float:
        """Corriente en el paso de tiempo anterior. Usado internamente por el solver."""
        return self._I_prev

    @I_prev.setter
    def I_prev(self, value: float):
        self._I_prev = value

    # ── Métodos abstractos implementados ─────────────────────────

    def stamp(self, G: np.ndarray, b: np.ndarray, node_map: dict, **kwargs) -> None:
        """
        Estampa la contribución del inductor en G y b.
        Requiere que current_var_idx haya sido asignado por el solver.

        Parámetros adicionales en kwargs:
            dt : float — paso de tiempo en segundos (obligatorio)
        """
        if self._current_var_idx is None:
            raise RuntimeError(
                f"El inductor {self._label} no tiene current_var_idx asignado. "
                "El solver debe asignarlo antes de llamar stamp()."
            )

        dt = kwargs.get("dt")
        if dt is None:
            raise ValueError("El inductor requiere 'dt' en stamp().")
        if dt <= 0:
            raise ValueError(f"dt debe ser positivo, se recibió: {dt}")

        i = node_map[self._node_pos]
        j = node_map[self._node_neg]
        k = self._current_var_idx

        if i is not None:
            G[i][k] += 1
            G[k][i] += 1

        if j is not None:
            G[j][k] -= 1
            G[k][j] -= 1

        G[k][k] -= self._inductance / dt
        b[k] -= (self._inductance / dt) * self._I_prev

    def get_current(self, x: np.ndarray, node_map: dict, **kwargs) -> float:
        """
        La corriente del inductor es directamente la variable extra I_L
        almacenada en x[current_var_idx].
        """
        if self._current_var_idx is None:
            raise RuntimeError(
                f"El inductor {self._label} no tiene current_var_idx asignado."
            )
        return float(x[self._current_var_idx])

    def get_voltage(self, x: np.ndarray, node_map: dict) -> float:
        i = node_map[self._node_pos]
        j = node_map[self._node_neg]
        Vi = float(x[i]) if i is not None else 0.0
        Vj = float(x[j]) if j is not None else 0.0
        return Vi - Vj

    def update_state(self, x: np.ndarray, node_map: dict) -> None:
        """
        Actualiza I_prev con la corriente del paso actual.
        El solver llama este método al final de cada paso de tiempo.
        """
        self._I_prev = self.get_current(x, node_map)

    def reset(self) -> None:
        """Reinicia el inductor a su condición inicial."""
        self._I_prev = self._initial_current

    # ── Representación ────────────────────────────────────────────

    def __repr__(self) -> str:
        label = f" ({self._label})" if self._label else ""
        return (
            f"Inductor{label} [L={self._inductance}H, "
            f"I0={self._initial_current}A, "
            f"n+={self._node_pos}, n-={self._node_neg}]"
        )
