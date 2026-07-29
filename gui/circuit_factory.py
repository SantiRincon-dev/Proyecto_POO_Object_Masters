from components import Capacitor, Inductor, Resistor, Switch
from sources import DCVoltageSource
from circuits import (
    CustomCircuit,
    RCParallel,
    RCSeries,
    RLParallel,
    RLSeries,
    RLCParallel,
    RLCSeries,
)
from gui.config import SimulationConfig


class CircuitFactory:
    RC_SERIES = "RC Serie"
    RC_PARALLEL = "RC Paralelo"
    RL_SERIES = "RL Serie"
    RL_PARALLEL = "RL Paralelo"
    RLC_SERIES = "RLC Serie"
    RLC_PARALLEL = "RLC Paralelo"
    CUSTOM = "Circuito Personalizado"

    CIRCUIT_TYPES = [
        RC_SERIES,
        RC_PARALLEL,
        RL_SERIES,
        RL_PARALLEL,
        RLC_SERIES,
        RLC_PARALLEL,
        CUSTOM,
    ]

    def create(self, config: SimulationConfig):
        resistor = Resistor(resistance=config.resistance, label="R1")
        capacitor = Capacitor(
            capacitance=config.capacitance,
            initial_voltage=config.initial_capacitor_voltage,
            label="C1",
        )
        inductor = Inductor(
            inductance=config.inductance,
            initial_current=config.initial_inductor_current,
            label="L1",
        )
        source = DCVoltageSource(voltage=config.source_voltage, label="Vs")
        switch = Switch(t_close=config.switch_close_time, label="SW1")

        if config.circuit_type == self.RC_SERIES:
            return RCSeries(resistor=resistor, capacitor=capacitor, source=source, switch=switch)
        if config.circuit_type == self.RC_PARALLEL:
            return RCParallel(resistor=resistor, capacitor=capacitor, source=source, switch=switch)
        if config.circuit_type == self.RL_SERIES:
            return RLSeries(resistor=resistor, inductor=inductor, source=source, switch=switch)
        if config.circuit_type == self.RL_PARALLEL:
            return RLParallel(resistor=resistor, inductor=inductor, source=source, switch=switch)
        if config.circuit_type == self.RLC_SERIES:
            return RLCSeries(
                resistor=resistor,
                inductor=inductor,
                capacitor=capacitor,
                source=source,
                switch=switch,
            )
        if config.circuit_type == self.RLC_PARALLEL:
            return RLCParallel(
                resistor=resistor,
                inductor=inductor,
                capacitor=capacitor,
                source=source,
                switch=switch,
            )
        if config.circuit_type == self.CUSTOM:
            return CustomCircuit(
                resistor=resistor,
                capacitor=capacitor,
                inductor=inductor,
                source=source,
                switch=switch,
            )

        raise ValueError(f"Tipo de circuito no soportado: {config.circuit_type}")

