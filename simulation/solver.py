# simulation/solver.py
import numpy as np
from simulation.sim_result import SimResult
from circuits.base_circuit import BaseCircuit
from components import Capacitor, Inductor, Switch


class Solver:
    """
    Ensambla y resuelve el sistema MNA para un circuito dado.

    Para circuitos puramente resistivos resuelve un sistema
    algebraico lineal con numpy. Para circuitos con capacitores
    o inductores resuelve una EDO paso a paso en el tiempo
    usando el método de Euler hacia atrás.

    Parámetros:
        circuit : BaseCircuit — topología del circuito a simular
        t_start : float       — tiempo inicial en segundos
        t_end   : float       — tiempo final en segundos
        dt      : float       — paso de tiempo en segundos
    """

    def __init__(self, circuit: BaseCircuit, t_start: float, t_end: float, dt: float):
        if not isinstance(circuit, BaseCircuit):
            raise TypeError(
                f"circuit debe ser una instancia de BaseCircuit, se recibió: {type(circuit)}"
            )
        if t_start < 0:
            raise ValueError(f"t_start debe ser no negativo, se recibió: {t_start}")
        if t_end <= t_start:
            raise ValueError(f"t_end debe ser mayor que t_start, se recibió: {t_end}")
        if dt <= 0:
            raise ValueError(f"dt debe ser positivo, se recibió: {dt}")
        if dt >= (t_end - t_start):
            raise ValueError("dt debe ser menor que el intervalo de simulación.")

        self._circuit = circuit
        self._t_start = t_start
        self._t_end = t_end
        self._dt = dt

    # ── Propiedades ──────────────────────────────────────────────

    @property
    def circuit(self) -> BaseCircuit:
        return self._circuit

    @property
    def t_start(self) -> float:
        return self._t_start

    @property
    def t_end(self) -> float:
        return self._t_end

    @property
    def dt(self) -> float:
        return self._dt

    # ── Métodos privados ──────────────────────────────────────────

    def _has_dynamic_elements(self) -> bool:
        """Verifica si el circuito tiene capacitores o inductores."""
        return any(
            isinstance(e, (Capacitor, Inductor)) for e in self._circuit.get_elements()
        )

    def _assign_current_var_indices(self) -> int:
        """
        Asigna current_var_idx a la fuente y a los inductores.
        Retorna el tamaño total del sistema (nodos + variables extra).

        Las variables extra van después de los voltajes nodales:
            x = [V1, V2, ..., Vn, Is, IL1, IL2, ...]
        """
        n = self._circuit.node_count
        idx = n

        # Fuente de voltaje
        source = self._circuit.source
        source.current_var_idx = idx
        idx += 1

        # Inductores
        for element in self._circuit.get_elements():
            if isinstance(element, Inductor):
                element.current_var_idx = idx
                idx += 1

        return idx

    def _build_mna_matrix(self, t: float, node_map: dict, dt: float = None) -> tuple:
        """
        Construye la matriz G y el vector b para el instante t.
        """
        size = self._system_size
        G = np.zeros((size, size))
        b = np.zeros(size)

        for element in self._circuit.get_elements():
            if isinstance(element, Switch):
                element.stamp(G, b, node_map, t=t)
            elif isinstance(element, (Capacitor, Inductor)):
                element.stamp(G, b, node_map, dt=dt)
            else:
                element.stamp(G, b, node_map)

        self._circuit.source.stamp(G, b, node_map)

        return G, b

    def _build_node_map(self) -> dict:
        """
        Construye el mapa de nodos excluyendo tierra.
        Los nodos van del 1 al node_count, mapeados a índices 0, 1, 2...
        Las variables extra (Is, IL) van después.
        """
        node_map = {}
        for node in range(1, self._circuit.node_count + 1):
            node_map[node] = node - 1  # nodo 1 → índice 0, nodo 2 → índice 1, etc.
        node_map[0] = None  # tierra no tiene índice
        return node_map

    def _reset_elements(self) -> None:
        """Reinicia todos los elementos a su condición inicial."""
        for element in self._circuit.get_elements():
            if hasattr(element, "reset"):
                element.reset()
        if hasattr(self._circuit.switch, "reset"):
            self._circuit.switch.reset()

    def _update_states(self, x: np.ndarray, node_map: dict) -> None:
        """
        Actualiza el estado interno de capacitores e inductores
        al final de cada paso de tiempo.
        """
        for element in self._circuit.get_elements():
            if hasattr(element, "update_state"):
                element.update_state(x, node_map)

    # ── Métodos públicos ──────────────────────────────────────────

    def solve_transient(self) -> SimResult:
        self._reset_elements()
        self._system_size = self._assign_current_var_indices()
        node_map = self._build_node_map()

        # DEBUG — borrar después
        print(f"node_count: {self._circuit.node_count}")
        print(f"system_size: {self._system_size}")
        print(f"node_map: {node_map}")

        time_steps = np.arange(self._t_start, self._t_end, self._dt)
        solutions = []

        for t in time_steps:
            G, b = self._build_mna_matrix(t=t, node_map=node_map, dt=self._dt)
            try:
                x = np.linalg.solve(G, b)
            except np.linalg.LinAlgError:
                raise RuntimeError(
                    f"La matriz del sistema es singular en t={t:.6f}s. "
                    "Verifique la topología del circuito."
                )
            solutions.append(x)
            self._update_states(x, node_map)

        voltages, currents = self._extract_results(solutions, node_map)
        return SimResult(time=time_steps, voltages=voltages, currents=currents)

    def solve_dc(self) -> SimResult:
        self._system_size = self._assign_current_var_indices()
        node_map = self._build_node_map()

        G, b = self._build_mna_matrix(t=0, node_map=node_map)
        try:
            x = np.linalg.solve(G, b)
        except np.linalg.LinAlgError:
            raise RuntimeError(
                "La matriz del sistema es singular. "
                "Verifique que el circuito no tenga nodos flotantes."
            )

        time = np.array([0.0])
        voltages, currents = self._extract_results([x], node_map)
        return SimResult(time=time, voltages=voltages, currents=currents)

    def solve(self) -> SimResult:
        """
        Punto de entrada principal. Detecta automáticamente
        si el circuito requiere análisis transitorio o DC puro.
        """
        if self._has_dynamic_elements():
            return self.solve_transient()
        else:
            return self.solve_dc()

    def _extract_results(self, solutions: list, node_map: dict) -> tuple:
        """
        Extrae voltajes y corrientes de cada elemento
        a partir de la lista de vectores solución.

        Retorna:
            voltages : dict {label: np.ndarray}
            currents : dict {label: np.ndarray}
        """
        voltages = {}
        currents = {}

        all_elements = self._circuit.get_all()

        for element in all_elements:
            label = element.label if element.label else element.__class__.__name__

            v_list = []
            i_list = []

            for x in solutions:
                try:
                    v = element.get_voltage(x, node_map)
                except Exception:
                    v = 0.0
                try:
                    i = element.get_current(x, node_map, dt=self._dt)
                except Exception:
                    i = 0.0

                v_list.append(v)
                i_list.append(i)

            voltages[label] = np.array(v_list)
            currents[label] = np.array(i_list)

        return voltages, currents

    def __repr__(self) -> str:
        return (
            f"Solver ["
            f"t={self._t_start}s → {self._t_end}s, "
            f"dt={self._dt}s, "
            f"circuito={self._circuit.__class__.__name__}]"
        )
