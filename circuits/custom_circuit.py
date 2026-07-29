# circuits/custom_circuit.py
from circuits.base_circuit import BaseCircuit
from components import Resistor, Switch, Capacitor, Inductor
from sources import Source


class CustomCircuit(BaseCircuit):
    """
    Circuito personalizado — modifica los componentes y _assign_nodes
    según la topología que quieras simular.

    """

    def __init__(
        self,
        resistor: Resistor,
        capacitor: Capacitor,
        inductor: Inductor,
        source: Source,
        switch: Switch,
    ):
        self._resistor = resistor
        self._capacitor = capacitor
        self._inductor = inductor
        super().__init__(source, switch)

    @property
    def resistor(self) -> Resistor:
        return self._resistor

    @property
    def capacitor(self) -> Capacitor:
        return self._capacitor

    @property
    def inductor(self) -> Inductor:
        return self._inductor

    def _assign_nodes(self) -> None:
        self._source.node_pos = 2
        self._source.node_neg = 1

        self._switch.node_pos = 1
        self._switch.node_neg = 0

        self._resistor.node_pos = 2
        self._resistor.node_neg = 3

        self._capacitor.node_pos = 3
        self._capacitor.node_neg = 0

        self._inductor.node_pos = 3
        self._inductor.node_neg = 0

        self._node_count = 3
        self._elements = [self._resistor, self._capacitor, self._inductor]
