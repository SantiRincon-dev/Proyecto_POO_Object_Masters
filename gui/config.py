from dataclasses import dataclass


@dataclass(frozen=True)
class SimulationConfig:
    circuit_type: str
    resistance: float
    capacitance: float
    inductance: float
    source_voltage: float
    switch_close_time: float
    initial_capacitor_voltage: float
    initial_inductor_current: float
    t_start: float
    t_end: float
    dt: float

