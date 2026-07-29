from gui.circuit_factory import CircuitFactory
from gui.config import SimulationConfig
from simulation import Solver


class SimulationRunner:
    def __init__(self, circuit_factory: CircuitFactory | None = None):
        self._circuit_factory = circuit_factory or CircuitFactory()

    def run(self, config: SimulationConfig):
        circuit = self._circuit_factory.create(config)
        solver = Solver(
            circuit=circuit,
            t_start=config.t_start,
            t_end=config.t_end,
            dt=config.dt,
        )
        return solver.solve()

