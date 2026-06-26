# circuits/rlc_series.py
from circuits.base_circuit import BaseCircuit
from components import Resistor, Inductor, Capacitor, Switch
from sources import Source


class RLCSeries(BaseCircuit):
    def __init__(
        self,
        resistor: Resistor,
        inductor: Inductor,
        capacitor: Capacitor,
        source: Source,
        switch: Switch,
    ):
        if not isinstance(resistor, Resistor):
            raise TypeError(f"Se esperaba Resistor, se recibió: {type(resistor)}")
        if not isinstance(inductor, Inductor):
            raise TypeError(f"Se esperaba Inductor, se recibió: {type(inductor)}")
        if not isinstance(capacitor, Capacitor):
            raise TypeError(f"Se esperaba Capacitor, se recibió: {type(capacitor)}")

        self._resistor = resistor
        self._inductor = inductor
        self._capacitor = capacitor

        super().__init__(source, switch)

    @property
    def resistor(self) -> Resistor:
        return self._resistor

    @property
    def inductor(self) -> Inductor:
        return self._inductor

    @property
    def capacitor(self) -> Capacitor:
        return self._capacitor

    def _assign_nodes(self) -> None:
        self._switch.node_pos = 2
        self._switch.node_neg = 1

        self._resistor.node_pos = 2
        self._resistor.node_neg = 3

        self._inductor.node_pos = 3
        self._inductor.node_neg = 4

        self._capacitor.node_pos = 4
        self._capacitor.node_neg = 0

        self._source.node_pos = 1
        self._source.node_neg = 0

        self._node_count = 4
        self._elements = [self._resistor, self._inductor, self._capacitor, self._switch]

    def __repr__(self) -> str:
        return (
            f"RLCSeries ["
            f"R={self._resistor.resistance}Ω, "
            f"L={self._inductor.inductance}H, "
            f"C={self._capacitor.capacitance}F, "
            f"V={self._source.get_voltage}V]"
        )
