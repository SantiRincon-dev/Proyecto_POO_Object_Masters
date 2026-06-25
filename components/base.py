# components/base.py
from abc import ABC, abstractmethod
import numpy as np


class CircuitElement(ABC):
    """
    Clase base abstracta para todos los elementos del circuito.
    Define la interfaz común que deben implementar resistores,
    capacitores, inductores y switches.

    El convenio de signos es:
        - La corriente fluye de node_pos hacia node_neg
        - El voltaje es V[node_pos] - V[node_neg]
    """

    def __init__(self, node_pos: int, node_neg: int, label: str = ""):
        self._node_pos = node_pos
        self._node_neg = node_neg
        self._label = label

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

    # ── Métodos abstractos ────────────────────────────────────────

    @abstractmethod
    def stamp(self, G: np.ndarray, b: np.ndarray, node_map: dict, **kwargs) -> None:
        """
        Estampa la contribución del elemento en la matriz G y el vector b.

        Parámetros:
            G        : Matriz de conductancias del sistema (n x n)
            b        : Vector de fuentes del sistema (n,)
            node_map : Diccionario {numero_nodo: indice_en_matriz}
            **kwargs : Parámetros adicionales según el elemento
                       (dt, V_prev para capacitor; dt, I_prev para inductor)
        """
        pass

    @abstractmethod
    def get_current(self, x: np.ndarray, node_map: dict, **kwargs) -> float:
        """
        Calcula la corriente que atraviesa el elemento dado el vector solución x.

        Parámetros:
            x        : Vector solución del sistema [V1, V2, ..., Is1, ...]
            node_map : Diccionario {numero_nodo: indice_en_matriz}
            **kwargs : Parámetros adicionales según el elemento

        Retorna:
            Corriente en amperios (positiva de node_pos a node_neg)
        """
        pass

    # ── Método concreto (igual para todos) ───────────────────────

    def get_voltage(self, x: np.ndarray, node_map: dict) -> float:
        """
        Calcula el voltaje entre node_pos y node_neg dado el vector solución x.

        Parámetros:
            x        : Vector solución del sistema
            node_map : Diccionario {numero_nodo: indice_en_matriz}

        Retorna:
            Voltaje en voltios (V[node_pos] - V[node_neg])
        """
        i = node_map[self._node_pos]
        j = node_map[self._node_neg]
        return float(x[i] - x[j])

    # ── Representación ────────────────────────────────────────────

    def __repr__(self) -> str:
        label = f" ({self._label})" if self._label else ""
        return f"{self.__class__.__name__}{label} [n+={self._node_pos}, n-={self._node_neg}]"
