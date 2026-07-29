# circuits/rl_series.py
from circuits.base_circuit import BaseCircuit
from components import Resistor, Inductor, Switch
from sources import Source


class RLSeries(BaseCircuit):
    def __init__(
        self, resistor: Resistor, inductor: Inductor, source: Source, switch: Switch
    ):
        if not isinstance(resistor, Resistor):
            raise TypeError(f"Se esperaba Resistor, se recibió: {type(resistor)}")
        if not isinstance(inductor, Inductor):
            raise TypeError(f"Se esperaba Inductor, se recibió: {type(inductor)}")

        self._resistor = resistor
        self._inductor = inductor

        super().__init__(source, switch)

    @property
    def resistor(self) -> Resistor:
        return self._resistor

    @property
    def inductor(self) -> Inductor:
        return self._inductor

    def _assign_nodes(self) -> None:
        self._switch.node_pos = 1
        self._switch.node_neg = 0

        self._resistor.node_pos = 2
        self._resistor.node_neg = 3

        self._inductor.node_pos = 3
        self._inductor.node_neg = 0

        self._source.node_pos = 2
        self._source.node_neg = 1

        self._node_count = 3
        self._elements = [self._resistor, self._inductor]

    def __repr__(self) -> str:
        return (
            f"RLSeries ["
            f"R={self._resistor.resistance}Ω, "
            f"L={self._inductor.inductance}H, "
            f"V={self._source.get_voltage}V]"
        )
