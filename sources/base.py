# sources/base.py
from abc import ABC, abstractmethod
import numpy as np


class Source(ABC):
    """
    Clase base abstracta para todas las fuentes del circuito.

    A diferencia de CircuitElement, las fuentes introducen
    una variable extra en el vector solución x — la corriente
    que entrega la fuente (I_s) — porque imponen un voltaje
    entre dos nodos y no se pueden representar directamente
    como una conductancia.

    El índice de esa variable extra es current_var_idx, y es
    asignado por el solver antes de ensamblar la matriz.
    """

    def __init__(self, node_pos: int, node_neg: int, label: str = ""):
        self._node_pos = node_pos
        self._node_neg = node_neg
        self._label = label
        self._current_var_idx = None

    # ── Propiedades ──────────────────────────────────────────────

    @property
    def node_pos(self) -> int:
        return self._node_pos

    @node_pos.setter
    def node_pos(self, value: int):
        if not isinstance(value, int) or value < 0:
            raise ValueError(
                f"node_pos debe ser un entero no negativo, se recibió: {value}"
            )
        self._node_pos = value

    @property
    def node_neg(self) -> int:
        return self._node_neg

    @node_neg.setter
    def node_neg(self, value: int):
        if not isinstance(value, int) or value < 0:
            raise ValueError(
                f"node_neg debe ser un entero no negativo, se recibió: {value}"
            )
        self._node_neg = value

    @property
    def label(self) -> str:
        return self._label

    @label.setter
    def label(self, value: str):
        self._label = str(value)

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

    # ── Métodos abstractos ────────────────────────────────────────

    @abstractmethod
    def stamp(self, G: np.ndarray, b: np.ndarray, node_map: dict, **kwargs) -> None:
        """
        Estampa la contribución de la fuente en G y b.

        Parámetros:
            G        : Matriz del sistema (n x n)
            b        : Vector del sistema (n,)
            node_map : Diccionario {numero_nodo: indice_en_matriz}
            **kwargs : Parámetros adicionales según la fuente
        """
        pass

    @abstractmethod
    def get_current(self, x: np.ndarray) -> float:
        """
        Retorna la corriente entregada por la fuente.
        Se lee directamente de x[current_var_idx].
        """
        pass

    @abstractmethod
    def get_voltage(self, x: np.ndarray) -> float:
        """
        Retorna el voltaje de la fuente.
        """
        pass

    # ── Validación de current_var_idx ─────────────────────────────

    def _check_current_var_idx(self):
        """Verifica que current_var_idx haya sido asignado por el solver."""
        if self._current_var_idx is None:
            raise RuntimeError(
                f"La fuente {self._label} no tiene current_var_idx asignado. "
                "El solver debe asignarlo antes de llamar stamp()."
            )

    # ── Representación ────────────────────────────────────────────

    def __repr__(self) -> str:
        label = f" ({self._label})" if self._label else ""
        return (
            f"{self.__class__.__name__}{label} "
            f"[n+={self._node_pos}, n-={self._node_neg}]"
        )
