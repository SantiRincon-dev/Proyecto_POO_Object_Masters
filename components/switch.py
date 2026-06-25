# components/switch.py
import numpy as np
from components.base import CircuitElement


class Switch(CircuitElement):
    """
    Modelo de un switch ideal controlado por tiempo.

    Antes de t_close el switch está abierto — no estampa nada en G,
    equivalente a un circuito abierto (resistencia infinita).

    En t >= t_close el switch se cierra — estampa una conductancia
    muy alta (g_closed) entre sus nodos, equivalente a un cable ideal.

    Esta estrategia es preferible a reconectar nodos dinámicamente
    porque mantiene el tamaño de la matriz constante durante toda
    la simulación.
    """

    G_CLOSED = 1e12  # Conductancia cuando está cerrado [S]
    # Suficientemente alta para aproximar un cortocircuito
    # sin causar problemas numéricos

    def __init__(
        self,
        t_close: float = 0.0,
        label: str = "",
        node_pos: int = 0,
        node_neg: int = 0,
    ):
        if t_close < 0:
            raise ValueError(f"t_close debe ser no negativo, se recibió: {t_close}")
        super().__init__(node_pos, node_neg, label)
        self._t_close = t_close
        self._closed = False

    # ── Propiedades ──────────────────────────────────────────────

    @property
    def t_close(self) -> float:
        return self._t_close

    @t_close.setter
    def t_close(self, value: float):
        if value < 0:
            raise ValueError(f"t_close debe ser no negativo, se recibió: {value}")
        self._t_close = value

    @property
    def closed(self) -> bool:
        """Estado actual del switch. Solo lectura."""
        return self._closed

    # ── Métodos ──────────────────────────────────────────────────

    def is_closed(self, t: float) -> bool:
        """
        Determina si el switch está cerrado en el instante t.
        Actualiza el estado interno _closed.

        Parámetros:
            t : float — tiempo actual de la simulación en segundos

        Retorna:
            True si t >= t_close, False en caso contrario
        """
        self._closed = t >= self._t_close
        return self._closed

    def stamp(self, G: np.ndarray, b: np.ndarray, node_map: dict, **kwargs) -> None:
        """
        Si el switch está cerrado estampa G_CLOSED como conductancia.
        Si está abierto no estampa nada — circuito abierto.

        Parámetros adicionales en kwargs:
            t : float — tiempo actual de la simulación (obligatorio)
        """
        t = kwargs.get("t")
        if t is None:
            raise ValueError("El switch requiere 't' en stamp().")

        if not self.is_closed(t):
            return

        i = node_map[self._node_pos]
        j = node_map[self._node_neg]
        g = self.G_CLOSED

        G[i][i] += g
        G[j][j] += g
        G[i][j] -= g
        G[j][i] -= g

    def get_current(self, x: np.ndarray, node_map: dict, **kwargs) -> float:
        """
        Calcula la corriente a través del switch.

        Si está abierto la corriente es 0.
        Si está cerrado se calcula como I = G_CLOSED * V,
        que al ser G_CLOSED muy alta aproxima el comportamiento
        de un cable ideal donde V ≈ 0.
        """
        if not self._closed:
            return 0.0
        V = self.get_voltage(x, node_map)
        return V * self.G_CLOSED

    def get_voltage(self, x: np.ndarray, node_map: dict) -> float:
        """
        Voltaje a través del switch.

        Si está abierto el voltaje puede ser cualquier valor
        (lo impone el resto del circuito).
        Si está cerrado el voltaje debería ser ≈ 0V
        por la alta conductancia.
        """
        i = node_map[self._node_pos]
        j = node_map[self._node_neg]
        return float(x[i] - x[j])

    def reset(self) -> None:
        """Reinicia el switch a su estado abierto."""
        self._closed = False

    # ── Representación ────────────────────────────────────────────

    def __repr__(self) -> str:
        label = f" ({self._label})" if self._label else ""
        estado = "cerrado" if self._closed else "abierto"
        return (
            f"Switch{label} [t_close={self._t_close}s, "
            f"estado={estado}, "
            f"n+={self._node_pos}, n-={self._node_neg}]"
        )
