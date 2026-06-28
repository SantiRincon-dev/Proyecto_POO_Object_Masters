# main.py
from components import Resistor, Capacitor, Inductor, Switch
from sources import DCVoltageSource
from circuits import (
    RCSeries,
    RCParallel,
    RLSeries,
    RLParallel,
    RLCSeries,
    RLCParallel,
    CustomCircuit,
)
from simulation import Solver
from plotting import Plotter


def simulate_rc_series():
    print("\n" + "=" * 52)
    print("         SIMULACIÓN RC SERIE")
    print("=" * 52)

    r = Resistor(resistance=1000, label="R1")
    c = Capacitor(capacitance=1e-6, initial_voltage=0.0, label="C1")
    src = DCVoltageSource(voltage=5.0, label="Vs")
    sw = Switch(t_close=0.0, label="SW1")

    circuit = RCSeries(resistor=r, capacitor=c, source=src, switch=sw)

    # Tiempo de simulación: 5 * tau = 5 * RC = 5 * 1000 * 1e-6 = 5ms
    tau = r.resistance * c.capacitance
    t_end = 5 * tau
    dt = tau / 1000

    solver = Solver(circuit=circuit, t_start=0.0, t_end=t_end, dt=dt)
    result = solver.solve()

    print(result.summary())

    plotter = Plotter(result=result)
    plotter.plot_all()


def simulate_rc_parallel():
    print("\n" + "=" * 52)
    print("         SIMULACIÓN RC PARALELO")
    print("=" * 52)

    r = Resistor(resistance=1000, label="R1")
    c = Capacitor(capacitance=1e-6, initial_voltage=0.0, label="C1")
    src = DCVoltageSource(voltage=5.0, label="Vs")
    sw = Switch(t_close=0.0, label="SW1")

    circuit = RCParallel(resistor=r, capacitor=c, source=src, switch=sw)

    tau = r.resistance * c.capacitance
    t_end = 5 * tau
    dt = tau / 1000

    solver = Solver(circuit=circuit, t_start=0.0, t_end=t_end, dt=dt)
    result = solver.solve()

    print(result.summary())

    plotter = Plotter(result=result)
    plotter.plot_all()


def simulate_rl_series():
    print("\n" + "=" * 52)
    print("         SIMULACIÓN RL SERIE")
    print("=" * 52)

    r = Resistor(resistance=100, label="R1")
    l = Inductor(inductance=0.01, initial_current=0.0, label="L1")
    src = DCVoltageSource(voltage=5.0, label="Vs")
    sw = Switch(t_close=0.0, label="SW1")

    circuit = RLSeries(resistor=r, inductor=l, source=src, switch=sw)

    # Tiempo de simulación: 5 * tau = 5 * L/R
    tau = l.inductance / r.resistance
    t_end = 5 * tau
    dt = tau / 1000

    solver = Solver(circuit=circuit, t_start=0.0, t_end=t_end, dt=dt)
    result = solver.solve()

    print(result.summary())

    plotter = Plotter(result=result)
    plotter.plot_all()


def simulate_rl_parallel():
    print("\n" + "=" * 52)
    print("         SIMULACIÓN RL PARALELO")
    print("=" * 52)

    r = Resistor(resistance=100, label="R1")
    l = Inductor(inductance=0.01, initial_current=0.0, label="L1")
    src = DCVoltageSource(voltage=5.0, label="Vs")
    sw = Switch(t_close=0.0, label="SW1")

    circuit = RLParallel(resistor=r, inductor=l, source=src, switch=sw)

    tau = l.inductance / r.resistance
    t_end = 5 * tau
    dt = tau / 1000

    solver = Solver(circuit=circuit, t_start=0.0, t_end=t_end, dt=dt)
    result = solver.solve()

    print(result.summary())

    plotter = Plotter(result=result)
    plotter.plot_all()


def simulate_rlc_series():
    print("\n" + "=" * 52)
    print("         SIMULACIÓN RLC SERIE")
    print("=" * 52)

    r = Resistor(resistance=100, label="R1")
    l = Inductor(inductance=0.01, initial_current=0.0, label="L1")
    c = Capacitor(capacitance=1e-6, initial_voltage=0.0, label="C1")
    src = DCVoltageSource(voltage=5.0, label="Vs")
    sw = Switch(t_close=0.0, label="SW1")

    circuit = RLCSeries(resistor=r, inductor=l, capacitor=c, source=src, switch=sw)

    # Para RLC serie: omega_0 = 1/sqrt(LC)
    import numpy as np

    omega_0 = 1 / np.sqrt(l.inductance * c.capacitance)
    t_end = 10 * np.pi / omega_0
    dt = t_end / 10000

    solver = Solver(circuit=circuit, t_start=0.0, t_end=t_end, dt=dt)
    result = solver.solve()

    print(result.summary())

    plotter = Plotter(result=result)
    plotter.plot_all()


def simulate_rlc_parallel():
    print("\n" + "=" * 52)
    print("         SIMULACIÓN RLC PARALELO")
    print("=" * 52)

    r = Resistor(resistance=100, label="R1")
    l = Inductor(inductance=0.01, initial_current=0.0, label="L1")
    c = Capacitor(capacitance=1e-6, initial_voltage=0.0, label="C1")
    src = DCVoltageSource(voltage=5.0, label="Vs")
    sw = Switch(t_close=0.0, label="SW1")

    circuit = RLCParallel(resistor=r, inductor=l, capacitor=c, source=src, switch=sw)

    import numpy as np

    omega_0 = 1 / np.sqrt(l.inductance * c.capacitance)
    t_end = 10 * np.pi / omega_0
    dt = t_end / 10000

    solver = Solver(circuit=circuit, t_start=0.0, t_end=t_end, dt=dt)
    result = solver.solve()

    print(result.summary())

    plotter = Plotter(result=result)
    plotter.plot_all()


def simulate_custom():
    resistor = Resistor(resistance=1000, label="R1")
    capacitor = Capacitor(capacitance=1e-6, initial_voltage=0.0, label="C1")
    inductor = Inductor(inductance=0.01, initial_current=0.0, label="L1")
    src = DCVoltageSource(voltage=5.0, label="Vs")
    sw = Switch(t_close=0.0, label="SW1")

    circuit = CustomCircuit(
        resistor=resistor, capacitor=capacitor, inductor=inductor, source=src, switch=sw
    )

    solver = Solver(circuit=circuit, t_start=0.0, t_end=0.01, dt=1e-6)
    result = solver.solve()

    print(result.summary())

    plotter = Plotter(result=result)
    plotter.plot_all()


if __name__ == "__main__":
    print("Seleccione la simulación a ejecutar:")
    print("  1. RC Serie")
    print("  2. RC Paralelo")
    print("  3. RL Serie")
    print("  4. RL Paralelo")
    print("  5. RLC Serie")
    print("  6. RLC Paralelo")
    print("  7. Circuito Personalizado")
    print("  0. Todas")

    opcion = input("\nOpción: ").strip()

    simulaciones = {
        "1": simulate_rc_series,
        "2": simulate_rc_parallel,
        "3": simulate_rl_series,
        "4": simulate_rl_parallel,
        "5": simulate_rlc_series,
        "6": simulate_rlc_parallel,
        "7": simulate_custom,
    }

    if opcion == "0":
        for fn in simulaciones.values():
            fn()
    elif opcion in simulaciones:
        simulaciones[opcion]()
    else:
        print("Opción no válida.")
