# circuits/base_circuit.py
from abc import ABC, abstractmethod
from components import Switch
from sources import Source


class BaseCircuit(ABC):
    """
    Clase base abstracta para todas las topologías de circuito.

    Define la interfaz común y contiene la lista de elementos
    que el solver usa para ensamblar la matriz MNA.

    Cada subclase implementa _assign_nodes() donde define
    cómo están conectados sus componentes entre sí, asignando
    los nodos correspondientes a cada elemento.

    Convención de nodos:
        - El nodo 0 siempre es tierra (ground)
        - Los nodos 1, 2, 3... son los nodos internos del circuito
    """

    def __init__(self, source: Source, switch: Switch):
        if not isinstance(source, Source):
            raise TypeError(
                f"source debe ser una instancia de Source, se recibió: {type(source)}"
            )
        if not isinstance(switch, Switch):
            raise TypeError(
                f"switch debe ser una instancia de Switch, se recibió: {type(switch)}"
            )

        self._source = source
        self._switch = switch
        self._elements = []
        self._node_count = 0
        self._ground_node = 0

        self._assign_nodes()

    # ── Propiedades ──────────────────────────────────────────────

    @property
    def source(self) -> Source:
        return self._source

    @property
    def switch(self) -> Switch:
        return self._switch

    @property
    def node_count(self) -> int:
        return self._node_count

    @property
    def ground_node(self) -> int:
        return self._ground_node

    # ── Métodos abstractos ────────────────────────────────────────

    @abstractmethod
    def _assign_nodes(self) -> None:
        """
        Asigna los nodos a cada componente del circuito y
        construye la lista de elementos.

        Debe:
            1. Asignar node_pos y node_neg a cada componente
            2. Asignar node_pos y node_neg a la fuente y al switch
            3. Poblar self._elements con los componentes pasivos
            4. Actualizar self._node_count con el número de nodos
               sin contar tierra
        """
        pass

    # ── Métodos concretos ─────────────────────────────────────────

    def get_elements(self) -> list:
        """
        Retorna la lista de componentes pasivos del circuito.
        El solver itera sobre esta lista para ensamblar la matriz.
        """
        return self._elements

    def get_sources(self) -> list:
        """
        Retorna la lista de fuentes del circuito.
        Incluye siempre la fuente principal y el switch.
        """
        return [self._source, self._switch]

    def get_all(self) -> list:
        """
        Retorna todos los elementos del circuito incluyendo
        componentes pasivos y fuente, excluyendo el switch
        ya que no aporta información relevante a los resultados.
        """
        return self._elements + [self._source]

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__} ["
            f"nodos={self._node_count}, "
            f"elementos={len(self._elements)}, "
            f"fuente={self._source}]"
        )
