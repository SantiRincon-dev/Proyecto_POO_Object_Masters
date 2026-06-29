# tests/test_solver.py
import pytest
import numpy as np
from components import Resistor, Capacitor, Inductor, Switch
from sources import DCVoltageSource
from circuits import RCSeries, RLSeries
from simulation import Solver, SimResult


def make_solver_rc_series(R=1000, C=1e-6, V=5.0, t_end=None, dt=None):
    r = Resistor(resistance=R, label="R1")
    c = Capacitor(capacitance=C, initial_voltage=0.0, label="C1")
    src = DCVoltageSource(voltage=V, label="Vs")
    sw = Switch(t_close=0.0, label="SW1")
    circuit = RCSeries(resistor=r, capacitor=c, source=src, switch=sw)
    tau = R * C
    t_end = t_end or 5 * tau
    dt = dt or tau / 1000
    return Solver(circuit=circuit, t_start=0.0, t_end=t_end, dt=dt), tau, V


def make_solver_rl_series(R=100, L=0.01, V=5.0, t_end=None, dt=None):
    r = Resistor(resistance=R, label="R1")
    l = Inductor(inductance=L, initial_current=0.0, label="L1")
    src = DCVoltageSource(voltage=V, label="Vs")
    sw = Switch(t_close=0.0, label="SW1")
    circuit = RLSeries(resistor=r, inductor=l, source=src, switch=sw)
    tau = L / R
    t_end = t_end or 5 * tau
    dt = dt or tau / 1000
    return Solver(circuit=circuit, t_start=0.0, t_end=t_end, dt=dt), tau, V


class TestSolverInstanciacion:
    def test_instanciacion_correcta(self):
        solver, _, _ = make_solver_rc_series()
        assert solver is not None

    def test_t_end_menor_t_start_lanza_error(self):
        r = Resistor(resistance=1000, label="R1")
        c = Capacitor(capacitance=1e-6, label="C1")
        src = DCVoltageSource(voltage=5.0, label="Vs")
        sw = Switch(t_close=0.0, label="SW1")
        circuit = RCSeries(resistor=r, capacitor=c, source=src, switch=sw)
        with pytest.raises(ValueError):
            Solver(circuit=circuit, t_start=0.01, t_end=0.001, dt=1e-6)

    def test_dt_negativo_lanza_error(self):
        r = Resistor(resistance=1000, label="R1")
        c = Capacitor(capacitance=1e-6, label="C1")
        src = DCVoltageSource(voltage=5.0, label="Vs")
        sw = Switch(t_close=0.0, label="SW1")
        circuit = RCSeries(resistor=r, capacitor=c, source=src, switch=sw)
        with pytest.raises(ValueError):
            Solver(circuit=circuit, t_start=0.0, t_end=0.01, dt=-1e-6)


class TestSolverRC:
    def test_retorna_sim_result(self):
        solver, _, _ = make_solver_rc_series()
        result = solver.solve()
        assert isinstance(result, SimResult)

    def test_voltaje_capacitor_valor_final(self):
        """
        En t = 5*tau el capacitor debe estar al 99.3% de Vs.
        Solución analítica: Vc(t) = Vs * (1 - e^(-t/tau))
        """
        solver, tau, V = make_solver_rc_series()
        result = solver.solve()
        Vc_final = result.get_voltage("C1")[-1]
        Vc_analitico = V * (1 - np.exp(-5))  # t = 5*tau
        assert Vc_final == pytest.approx(Vc_analitico, rel=0.01)

    def test_voltaje_capacitor_en_un_tau(self):
        """
        En t = tau el capacitor debe estar al 63.2% de Vs.
        """
        solver, tau, V = make_solver_rc_series()
        result = solver.solve()
        idx_tau = int(len(result.time) / 5)  # tau = t_end/5
        Vc_tau = result.get_voltage("C1")[idx_tau]
        Vc_analitico = V * (1 - np.exp(-1))
        assert Vc_tau == pytest.approx(Vc_analitico, rel=0.02)

    def test_corriente_inicial_rc(self):
        """
        En t=0 la corriente debe ser Vs/R (capacitor como cortocircuito).
        """
        solver, tau, V = make_solver_rc_series(R=1000, V=5.0)
        result = solver.solve()
        I_inicial = result.get_current("R1")[0]
        assert I_inicial == pytest.approx(V / 1000, rel=0.01)

    def test_voltaje_resistor_mas_capacitor_igual_fuente(self):
        """
        KVL: V_R + V_C = Vs en todo momento.
        """
        solver, _, V = make_solver_rc_series()
        result = solver.solve()
        V_R = result.get_voltage("R1")
        V_C = result.get_voltage("C1")
        V_total = V_R + V_C
        assert np.allclose(V_total, V, atol=0.01)

    def test_labels_correctos(self):
        solver, _, _ = make_solver_rc_series()
        result = solver.solve()
        assert "R1" in result.labels
        assert "C1" in result.labels
        assert "Vs" in result.labels


class TestSolverRL:
    def test_corriente_inductor_valor_final(self):
        """
        En t = 5*tau la corriente debe ser al 99.3% de Vs/R.
        Solución analítica: I(t) = (Vs/R) * (1 - e^(-t/tau))
        """
        solver, tau, V = make_solver_rl_series(R=100, L=0.01, V=5.0)
        result = solver.solve()
        I_final = result.get_current("L1")[-1]
        I_analitico = (V / 100) * (1 - np.exp(-5))
        assert I_final == pytest.approx(I_analitico, rel=0.01)

    def test_corriente_inductor_en_un_tau(self):
        """
        En t = tau la corriente debe ser al 63.2% de Vs/R.
        """
        solver, tau, V = make_solver_rl_series(R=100, L=0.01, V=5.0)
        result = solver.solve()
        idx_tau = int(len(result.time) / 5)
        I_tau = result.get_current("L1")[idx_tau]
        I_analitico = (V / 100) * (1 - np.exp(-1))
        assert I_tau == pytest.approx(I_analitico, rel=0.02)

    def test_kvl_rl_serie(self):
        """
        KVL: V_R + V_L = Vs en todo momento.
        """
        solver, _, V = make_solver_rl_series()
        result = solver.solve()
        V_R = result.get_voltage("R1")
        V_L = result.get_voltage("L1")
        V_total = V_R + V_L
        assert np.allclose(V_total, V, atol=0.05)


class TestSolverSimResult:
    def test_tiempo_correcto(self):
        solver, tau, _ = make_solver_rc_series()
        result = solver.solve()
        assert result.t_start == pytest.approx(0.0)
        assert result.t_end == pytest.approx(5 * tau, rel=0.01)

    def test_get_power(self):
        solver, _, _ = make_solver_rc_series()
        result = solver.solve()
        P = result.get_power("R1")
        assert len(P) == len(result.time)
        assert P[0] >= 0

    def test_summary_retorna_string(self):
        solver, _, _ = make_solver_rc_series()
        result = solver.solve()
        s = result.summary()
        assert isinstance(s, str)
        assert "R1" in s
        assert "C1" in s

    def test_label_inexistente_lanza_error(self):
        solver, _, _ = make_solver_rc_series()
        result = solver.solve()
        with pytest.raises(KeyError):
            result.get_voltage("X99")
