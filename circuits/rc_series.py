# circuits/rc_series.py
from circuits.base_circuit import BaseCircuit
from components import Resistor, Capacitor, Switch
from sources import Source


class RCSeries(BaseCircuit):
    """
    Topología RC en serie.

    Esquema:
        tierra(0) ─── Vs ─── nodo1 ─── SW ─── nodo2 ─── R ─── nodo3 ─── C ─── tierra(0)

    Con el switch abierto el circuito está en reposo.
    Al cerrarse en t_close la fuente empieza a cargar el capacitor
    a través de la resistencia.
    """

    def __init__(
        self, resistor: Resistor, capacitor: Capacitor, source: Source, switch: Switch
    ):
        if not isinstance(resistor, Resistor):
            raise TypeError(f"Se esperaba Resistor, se recibió: {type(resistor)}")
        if not isinstance(capacitor, Capacitor):
            raise TypeError(f"Se esperaba Capacitor, se recibió: {type(capacitor)}")

        self._resistor = resistor
        self._capacitor = capacitor

        super().__init__(source, switch)

    # ── Propiedades ──────────────────────────────────────────────

    @property
    def resistor(self) -> Resistor:
        return self._resistor

    @property
    def capacitor(self) -> Capacitor:
        return self._capacitor

    # ── Implementación de _assign_nodes ──────────────────────────

    def _assign_nodes(self) -> None:

        self._source.node_pos = 2
        self._source.node_neg = 1

        self._switch.node_pos = 1
        self._switch.node_neg = 0

        self._resistor.node_pos = 2
        self._resistor.node_neg = 3

        self._capacitor.node_pos = 3
        self._capacitor.node_neg = 0

        self._node_count = 3
        self._elements = [self._resistor, self._capacitor]


def __repr__(self) -> str:
    return (
        f"RCSeries ["
        f"R={self._resistor.resistance}Ω, "
        f"C={self._capacitor.capacitance}F, "
        f"V={self._source.voltage}V]"
    )
