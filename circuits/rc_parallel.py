# circuits/rc_parallel.py
from circuits.base_circuit import BaseCircuit
from components import Resistor, Capacitor, Switch
from sources import Source


class RCParallel(BaseCircuit):
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
        """
        Topología:
            tierra(0) ─ Vs(0→1) ─ SW(1→2) ─┬─ R(2→0) ─┬─ tierra(0)
                                          └─ C(2→0) ─┘
        """
        self._source.node_pos = 2
        self._source.node_neg = 1

        self._switch.node_pos = 1
        self._switch.node_neg = 0

        self._resistor.node_pos = 2
        self._resistor.node_neg = 0

        self._capacitor.node_pos = 2
        self._capacitor.node_neg = 0

        self._node_count = 2
        self._elements = [self._resistor, self._capacitor]

    def __repr__(self) -> str:
        return (
            f"RCParallel ["
            f"R={self._resistor.resistance}Ω, "
            f"C={self._capacitor.capacitance}F, "
            f"V={self._source.get_voltage}V]"
        )
